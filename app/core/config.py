import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET is not set in environment variables. Please check your .env file.")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL", "noreply@codexar.dev")
BREVO_SENDER_NAME = "Codexar"
ALLOWED_ORIGINS        = os.getenv("ALLOWED_ORIGINS", "*")
STRIPE_SECRET_KEY      = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET  = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PLUS_PRICE_ID   = os.getenv("STRIPE_PLUS_PRICE_ID", "")
STRIPE_MAX_PRICE_ID    = os.getenv("STRIPE_MAX_PRICE_ID", "")

# Judge0 code execution
# Priority: self-hosted (JUDGE0_SELF_URL) > RapidAPI (JUDGE0_KEY) > public CE
JUDGE0_SELF_URL = os.getenv("JUDGE0_SELF_URL", "")  # e.g. http://host.docker.internal:2358
JUDGE0_KEY      = os.getenv("JUDGE0_KEY", "")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DB_NAME = "Codexar"

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in environment variables. Please check your .env file.")
