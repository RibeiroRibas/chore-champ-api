import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import FileSystemLoader, Environment

from src.infra.decorators.logger import logging
from src.domain.errors.base_error import BaseError
from src.domain.errors.internal_error import InternalError
from src.infra.http.errors.codes.infra_error_codes import InfraErrorCodes


@logging(show_args=True, show_return=True)
def send(template_str: str, email: str, subject: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('SMTP_MAIL_FROM')
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(template_str, "html"))

        with smtplib.SMTP(os.getenv('SMTP_MAIL_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(os.getenv('SMTP_MAIL_USERNAME'), os.getenv('SMTP_MAIL_PASSWORD'))
            server.sendmail(os.getenv('SMTP_MAIL_FROM'), str(email), msg.as_string())

    except Exception as error:
        if isinstance(error, BaseError):
            raise error
        raise InternalError(code=InfraErrorCodes.SEND_EMAIL_ERROR.code())

def send_temp_password(email: str, temp_password: str) -> None:
    """Envia e-mail com senha temporária (para membros da família)."""
    rendered = render_template(
        message_variables={"temp_password": temp_password},
        template_name="send_temp_password_template.html",
    )
    send(template_str=rendered, email=email, subject="Sua senha de acesso - ChoreChamp")


def render_template(message_variables: dict, template_name: str) -> str:
    try:
        env = Environment(loader=FileSystemLoader(f'./src/templates'))
        template = env.get_template(template_name)
        return template.render(message_variables)
    except Exception:
        raise InternalError(code=InfraErrorCodes.RENDER_TEMPLATE_ERROR.code())
