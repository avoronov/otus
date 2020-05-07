from django.core.mail import send_mass_mail
from django_rq import job

import logging

logger = logging.getLogger(__name__)


@job
def task_send_email(user_email, subject, message):
    mails = (
        (subject, message, 'info@learinigcenter.nowhere.org', ('admin@learinigcenter.nowhere.org', user_email)),
    )
    try:
        send_mass_mail(mails)
    except Exception as e:
        logger.debug(e)
