from celery import shared_task
from user.models import *
from django.utils.timezone import now
import uuid
from datetime import timedelta
from time import sleep

@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(code=uuid.uuid4(),user=user, expiration=expiration)
    record.send_verification_email()

