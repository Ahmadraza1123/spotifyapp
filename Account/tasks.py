from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email, username):
    subject = "Welcome to Spotify App!"
    message = f"Hello {username},\n\nYour account has been created successfully.\nEnjoy using Spotify App!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    return "Email sent successfully"



@shared_task
def send_password_reset_email_task(username, email, reset_url):
    subject = "Password Reset Request"
    message = (
        f"Hi {username},\n\n"
        f"Use the link below to reset your password:\n{reset_url}\n\n"
        "If you did not request this, please ignore this email."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return "Password reset email sent successfully"
