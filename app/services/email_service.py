import httpx
from app.core.config import BREVO_API_KEY, BREVO_SENDER_EMAIL, BREVO_SENDER_NAME

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _build_email_html(code: str) -> str:
    digits = "  ".join(list(code))
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verifica tu cuenta de Codexar</title>
</head>
<body style="margin:0;padding:0;background-color:#0a0a0e;font-family:'Courier New',monospace;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0a0a0e;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="100%" style="max-width:480px;" cellpadding="0" cellspacing="0">

          <!-- Card -->
          <tr>
            <td style="background:#111118;border:1px solid rgba(0,255,204,0.15);border-radius:16px;overflow:hidden;">

              <!-- Top accent line -->
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="height:2px;background:linear-gradient(90deg,transparent,#00ffcc,transparent);"></td>
                </tr>
              </table>

              <!-- Content -->
              <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 40px 36px;">

                <!-- Brand -->
                <tr>
                  <td align="center" style="padding-bottom:6px;">
                    <span style="font-family:'Courier New',monospace;font-size:1.8rem;font-weight:800;letter-spacing:-1px;color:#ffffff;">
                      Codex<span style="color:#00ffcc;">ar</span>
                    </span>
                  </td>
                </tr>

                <!-- Subtitle -->
                <tr>
                  <td align="center" style="padding-bottom:28px;">
                    <p style="margin:0;font-family:'Courier New',monospace;font-size:0.75rem;letter-spacing:2px;text-transform:uppercase;color:#52536a;">
                      Verifica tu cuenta
                    </p>
                  </td>
                </tr>

                <!-- Divider -->
                <tr>
                  <td style="height:1px;background:rgba(255,255,255,0.05);margin-bottom:28px;">&nbsp;</td>
                </tr>

                <!-- Message -->
                <tr>
                  <td style="padding:20px 0 24px;">
                    <p style="margin:0;font-family:'Courier New',monospace;font-size:0.85rem;color:#a0a0b8;line-height:1.7;text-align:center;">
                      Alguien (esperamos que seas tú) ha solicitado crear<br>
                      una cuenta en <span style="color:#00ffcc;">Codexar</span>.<br><br>
                      Introduce el siguiente código en la app.<br>
                      <span style="color:#ff5555;">Expira en <strong>5 minutos</strong>.</span>
                    </p>
                  </td>
                </tr>

                <!-- Code block -->
                <tr>
                  <td align="center" style="padding-bottom:28px;">
                    <div style="display:inline-block;background:rgba(0,255,204,0.06);border:1px solid rgba(0,255,204,0.25);border-radius:12px;padding:20px 36px;">
                      <span style="font-family:'Courier New',monospace;font-size:2.4rem;font-weight:700;letter-spacing:12px;color:#00ffcc;display:block;text-align:center;">
                        {code}
                      </span>
                    </div>
                  </td>
                </tr>

                <!-- Divider -->
                <tr>
                  <td style="height:1px;background:rgba(255,255,255,0.05);">&nbsp;</td>
                </tr>

                <!-- Footer note -->
                <tr>
                  <td style="padding-top:20px;">
                    <p style="margin:0;font-family:'Courier New',monospace;font-size:0.72rem;color:#3a3a52;text-align:center;line-height:1.6;">
                      Si no has solicitado esto, ignora este mensaje.<br>
                      Nadie tiene acceso a tu cuenta sin el código.
                    </p>
                  </td>
                </tr>

              </table>
            </td>
          </tr>

          <!-- Bottom brand -->
          <tr>
            <td align="center" style="padding-top:24px;">
              <p style="margin:0;font-family:'Courier New',monospace;font-size:0.7rem;color:#2a2a3a;letter-spacing:1px;">
                © 2025 CODEXAR — Competitive Programming Platform
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


async def send_verification_email(to_email: str, code: str) -> bool:
    payload = {
        "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": "🔐 Tu código de verificación — Codexar",
        "htmlContent": _build_email_html(code),
    }
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(BREVO_API_URL, json=payload, headers=headers)
        print(f"[Brevo] status={response.status_code} body={response.text}")
        return response.status_code in (200, 201)
