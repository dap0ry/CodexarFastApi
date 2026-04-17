"""
subscriptions.py — Codexar Stripe subscription system
Plans: plus (€0.99/mo), max (€9.99/mo)
"""
import logging
from datetime import datetime, timezone

import stripe
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

import app.core.database as database
from app.core.config import (
    STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
    STRIPE_PLUS_PRICE_ID, STRIPE_MAX_PRICE_ID, STRIPE_PUBLISHABLE_KEY
)
from app.core.security import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

stripe.api_key = STRIPE_SECRET_KEY

PLAN_PRICE_MAP = {
    "plus": STRIPE_PLUS_PRICE_ID,
    "max":  STRIPE_MAX_PRICE_ID,
}


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _get_user_by_email(email: str) -> dict:
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


async def _set_user_plan(email: str, plan: str | None):
    """Update user's subscription_plan field. plan=None means free."""
    await database.db.users.update_one(
        {"email": email},
        {"$set": {"subscription_plan": plan}}
    )


async def _remove_boost(boosted_username: str):
    """Strip plus_boosted plan from a friend when Max user cancels."""
    await database.db.users.update_one(
        {"username": boosted_username, "subscription_plan": "plus_boosted"},
        {"$set": {"subscription_plan": None, "is_boosted_by": None}}
    )


# ── Create checkout session ────────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan: str
    success_url: str
    cancel_url: str


@router.post("/create-checkout")
async def create_checkout(body: CheckoutRequest, email: str = Depends(get_current_user)):
    if body.plan not in PLAN_PRICE_MAP:
        raise HTTPException(status_code=400, detail="Plan inválido. Usa 'plus' o 'max'.")

    price_id = PLAN_PRICE_MAP[body.plan]
    if not price_id:
        raise HTTPException(status_code=503, detail="Suscripciones no configuradas aún.")

    user = await _get_user_by_email(email)

    # Reuse existing Stripe customer if available
    sub_doc = await database.db.subscriptions.find_one({"email": email})
    customer_id = sub_doc.get("stripe_customer_id") if sub_doc else None

    try:
        kwargs = dict(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=body.success_url,
            cancel_url=body.cancel_url,
            metadata={"email": email, "plan": body.plan},
            subscription_data={"metadata": {"email": email, "plan": body.plan}},
        )
        if customer_id:
            kwargs["customer"] = customer_id
        else:
            kwargs["customer_email"] = email

        session = stripe.checkout.Session.create(**kwargs)
        return {"url": session.url}
    except stripe.error.StripeError as e:
        logger.error("Stripe checkout error: %s", str(e))
        raise HTTPException(status_code=500, detail="Error creando sesión de pago.")


# ── Customer portal (manage / cancel) ────────────────────────────────────────

@router.post("/portal")
async def customer_portal(return_url: str, email: str = Depends(get_current_user)):
    sub_doc = await database.db.subscriptions.find_one({"email": email})
    if not sub_doc or not sub_doc.get("stripe_customer_id"):
        raise HTTPException(status_code=404, detail="No tienes una suscripción activa.")
    try:
        session = stripe.billing_portal.Session.create(
            customer=sub_doc["stripe_customer_id"],
            return_url=return_url,
        )
        return {"url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail="Error abriendo portal de cliente.")


# ── Get current subscription status ──────────────────────────────────────────

@router.get("/status")
async def get_status(email: str = Depends(get_current_user)):
    sub_doc = await database.db.subscriptions.find_one({"email": email}, {"_id": 0})
    if not sub_doc or sub_doc.get("status") not in ("active", "trialing"):
        return {"plan": None, "status": "none"}
    return {
        "plan":           sub_doc.get("plan"),
        "status":         sub_doc.get("status"),
        "expires_at":     sub_doc.get("expires_at"),
        "boosted_friend": sub_doc.get("boosted_friend"),
    }


# ── Boost a friend (Max plan only) ───────────────────────────────────────────

class BoostRequest(BaseModel):
    friend_username: str


@router.post("/boost-friend")
async def boost_friend(body: BoostRequest, email: str = Depends(get_current_user)):
    user = await _get_user_by_email(email)

    if user.get("subscription_plan") != "max":
        raise HTTPException(status_code=403, detail="Solo los usuarios Max pueden dar boost.")

    sub_doc = await database.db.subscriptions.find_one({"email": email})
    if sub_doc and sub_doc.get("boosted_friend"):
        raise HTTPException(status_code=400, detail="Ya tienes un amigo con boost activo. Retíralo primero.")

    # Verify they are friends
    friends_emails = user.get("friends", [])
    friend = await database.db.users.find_one({"username": body.friend_username})
    if not friend:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    if friend.get("email") not in friends_emails:
        raise HTTPException(status_code=403, detail="Solo puedes dar boost a un amigo.")
    if friend.get("subscription_plan") in ("plus", "max"):
        raise HTTPException(status_code=400, detail="Ese usuario ya tiene una suscripción de pago.")

    # Apply boost
    await database.db.users.update_one(
        {"username": body.friend_username},
        {"$set": {"subscription_plan": "plus_boosted", "is_boosted_by": user.get("username")}}
    )
    await database.db.subscriptions.update_one(
        {"email": email},
        {"$set": {"boosted_friend": body.friend_username}}
    )
    return {"message": f"Boost aplicado a {body.friend_username}"}


@router.delete("/boost-friend")
async def remove_boost_friend(email: str = Depends(get_current_user)):
    sub_doc = await database.db.subscriptions.find_one({"email": email})
    if not sub_doc or not sub_doc.get("boosted_friend"):
        raise HTTPException(status_code=404, detail="No hay ningún boost activo.")

    boosted = sub_doc["boosted_friend"]
    await _remove_boost(boosted)
    await database.db.subscriptions.update_one(
        {"email": email},
        {"$set": {"boosted_friend": None}}
    )
    return {"message": f"Boost retirado de {boosted}"}


# ── Stripe Webhook ────────────────────────────────────────────────────────────

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload    = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")

    etype = event["type"]
    data  = event["data"]["object"]

    # ── checkout.session.completed ────────────────────────────────────────────
    if etype == "checkout.session.completed":
        meta        = data.get("metadata", {})
        email       = meta.get("email")
        plan        = meta.get("plan")
        customer_id = data.get("customer")
        sub_id      = data.get("subscription")

        if not email or not plan:
            return {"ok": True}

        # Fetch subscription to get period end
        try:
            sub = stripe.Subscription.retrieve(sub_id)
            expires_at = datetime.fromtimestamp(sub["current_period_end"], tz=timezone.utc)
        except Exception:
            expires_at = None

        await database.db.subscriptions.update_one(
            {"email": email},
            {"$set": {
                "email":                  email,
                "plan":                   plan,
                "status":                 "active",
                "stripe_customer_id":     customer_id,
                "stripe_subscription_id": sub_id,
                "started_at":             datetime.utcnow(),
                "expires_at":             expires_at,
            }},
            upsert=True
        )
        await _set_user_plan(email, plan)
        logger.info("Subscription activated: %s -> %s", email, plan)

    # ── invoice.paid (renewal) ────────────────────────────────────────────────
    elif etype == "invoice.paid":
        sub_id = data.get("subscription")
        if sub_id:
            try:
                sub        = stripe.Subscription.retrieve(sub_id)
                expires_at = datetime.fromtimestamp(sub["current_period_end"], tz=timezone.utc)
                meta       = sub.get("metadata", {})
                email      = meta.get("email")
                if email:
                    await database.db.subscriptions.update_one(
                        {"email": email},
                        {"$set": {"status": "active", "expires_at": expires_at}}
                    )
            except Exception as e:
                logger.warning("invoice.paid error: %s", e)

    # ── customer.subscription.updated ────────────────────────────────────────
    elif etype == "customer.subscription.updated":
        meta   = data.get("metadata", {})
        email  = meta.get("email")
        status = data.get("status")  # active, past_due, canceled, etc.
        if email:
            new_status = "active" if status in ("active", "trialing") else "expired"
            await database.db.subscriptions.update_one(
                {"email": email},
                {"$set": {"status": new_status}}
            )
            if new_status != "active":
                sub_doc = await database.db.subscriptions.find_one({"email": email})
                if sub_doc and sub_doc.get("boosted_friend"):
                    await _remove_boost(sub_doc["boosted_friend"])
                    await database.db.subscriptions.update_one(
                        {"email": email}, {"$set": {"boosted_friend": None}}
                    )
                await _set_user_plan(email, None)

    # ── customer.subscription.deleted ────────────────────────────────────────
    elif etype == "customer.subscription.deleted":
        meta  = data.get("metadata", {})
        email = meta.get("email")
        if email:
            sub_doc = await database.db.subscriptions.find_one({"email": email})
            if sub_doc and sub_doc.get("boosted_friend"):
                await _remove_boost(sub_doc["boosted_friend"])
            await database.db.subscriptions.update_one(
                {"email": email},
                {"$set": {"status": "cancelled", "boosted_friend": None}}
            )
            await _set_user_plan(email, None)
            logger.info("Subscription cancelled: %s", email)

    # ── invoice.payment_failed ────────────────────────────────────────────────
    elif etype == "invoice.payment_failed":
        sub_id = data.get("subscription")
        if sub_id:
            try:
                sub   = stripe.Subscription.retrieve(sub_id)
                email = sub.get("metadata", {}).get("email")
                if email:
                    await database.db.subscriptions.update_one(
                        {"email": email}, {"$set": {"status": "past_due"}}
                    )
            except Exception as e:
                logger.warning("payment_failed error: %s", e)

    return {"ok": True}


# ── Public key endpoint ───────────────────────────────────────────────────────

@router.get("/public-key")
async def get_public_key():
    return {"publishable_key": STRIPE_PUBLISHABLE_KEY}
