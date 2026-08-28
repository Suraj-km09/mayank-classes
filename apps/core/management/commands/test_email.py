import sys
from django.core.management.base import BaseCommand
from django.core.mail import send_mail, get_connection
from django.conf import settings


class Command(BaseCommand):
    help = "Tests SMTP email delivery and prints step-by-step diagnostic information."

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient',
            nargs='?',
            type=str,
            default=None,
            help='Target email address to receive the test email'
        )

    def handle(self, *args, **options):
        recipient = options.get('recipient') or settings.ADMIN_EMAIL_NOTIFICATION or settings.EMAIL_HOST_USER
        
        self.stdout.write(self.style.MIGRATE_HEADING("=== SMTP EMAIL DIAGNOSTIC TEST ==="))
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}")
        self.stdout.write(f"EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
        self.stdout.write(f"EMAIL_TIMEOUT: {getattr(settings, 'EMAIL_TIMEOUT', 15)} seconds")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or '[NOT CONFIGURED]'}")
        self.stdout.write(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else '[NOT CONFIGURED]'}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"TARGET RECIPIENT: {recipient}")
        self.stdout.write("---------------------------------------------")

        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(self.style.ERROR("ERROR: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is not set in environment variables!"))
            return

        if not recipient:
            self.stdout.write(self.style.ERROR("ERROR: No recipient specified. Provide one: python manage.py test_email user@example.com"))
            return

        self.stdout.write("1. Testing connection to SMTP server...")
        try:
            connection = get_connection()
            connection.open()
            self.stdout.write(self.style.SUCCESS("[OK] SMTP connection & TLS/SSL handshake established successfully!"))
            connection.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] Failed to connect to SMTP server: {type(e).__name__} - {e}"))
            import traceback
            traceback.print_exc()
            return

        self.stdout.write(f"2. Sending test email to {recipient}...")
        try:
            sent = send_mail(
                subject="[TEST] Mayank Classes SMTP Delivery Verification",
                message=(
                    "Hello!\n\n"
                    "If you are reading this email, your SMTP configuration on Mayank Classes is working perfectly!\n\n"
                    f"Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}\n"
                    f"TLS: {getattr(settings, 'EMAIL_USE_TLS', False)} | SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}\n"
                    f"From: {settings.DEFAULT_FROM_EMAIL}\n\n"
                    "— Mayank Classes Automated Diagnostics"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"[OK] Success! Sent {sent} test email(s) to {recipient}."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] Failed to send email: {type(e).__name__} - {e}"))
            import traceback
            traceback.print_exc()
