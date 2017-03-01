import logging
import smtplib

from ..conf import settings


logger = logging.getLogger(__name__)


def post_smtp(conf, report, notifier_conf, **kwargs):
    logger.info("Executing SMTP notifier")
    credentials = settings().creds['smtp']
    user = credentials['user']
    password = credentials['password']
    host = credentials['host']
    port = credentials['port']
    recipients = notifier_conf['recipients']
    subject = notifier_conf['subject']
    send_email(
        user=user,
        password=password,
        recipients=recipients,
        subject=subject,
        body=report,
        host=host,
        port=port,
    )


def send_email(user, password, recipients, subject, body, host, port):
    message = (
        u"From: {user}\r\n"
        u"To: {to}\r\n"
        u"Subject: {subject}\r\n\r\n"
        u"{body}\r\n"
        .format(
            user=user,
            to=", ".join(recipients),
            subject=subject,
            body=body,
        )
    )
    try:
        server = smtplib.SMTP(host, port)  # ("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(user, recipients, message.encode("utf-8"))
        server.close()
        logger.debug('Successfully sent the mail')
    except:
        logger.exception("Failed to send the e-mail")
