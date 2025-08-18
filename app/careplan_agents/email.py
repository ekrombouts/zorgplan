import os
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool


@function_tool
def send_careplan_email(
    subject: str, html_body: str, recipient_email: str = "ekrombouts@gmail.com"
) -> Dict[str, str]:
    """Verstuur een email met het zorgplan"""
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
        from_email = Email("ekrombouts@live.com")  # verified sender
        to_email = To(recipient_email)
        content = Content("text/html", html_body)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.send(mail)
        print("Email response", response.status_code)
        return {
            "status": "success",
            "message": f"Zorgplan verstuurd naar {recipient_email}",
        }
    except Exception as e:
        print(f"Email error: {e}")
        return {"status": "error", "message": str(e)}


INSTRUCTIONS = """
Je bent een zorgcoördinator die zorgplannen omzet naar nette HTML emails.

Je ontvangt een volledig zorgplan en moet dit omzetten naar:
1. Een passende onderwerpregel
2. Een goed geformatteerde HTML email die professioneel oogt

De email moet:
- Professioneel en overzichtelijk zijn
- Gebruik maken van HTML opmaak (headings, lijsten, styling)
- Geschikt zijn voor versturen naar zorgteam/familie
- Alle belangrijke informatie bevatten uit het zorgplan

Zorg voor een warme maar professionele toon die past bij de zorgverlening.
"""

email_agent = Agent(
    name="EmailAgent",
    instructions=INSTRUCTIONS,
    tools=[send_careplan_email],
    model="gpt-4o-mini",
)
