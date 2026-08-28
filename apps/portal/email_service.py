import logging
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

logger = logging.getLogger(__name__)


def build_student_confirmation_html(inquiry):
    """Builds a beautiful, mobile-optimized HTML confirmation email for the student."""
    created_time = timezone.now().strftime('%d %B %Y, %I:%M %p')
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Counseling & Demo Booking Confirmation - Mayank Classes</title>
</head>
<body style="margin:0;padding:0;background-color:#F8FAFC;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed;background-color:#F8FAFC;padding:30px 10px;">
    <tr>
      <td align="center">
        <!-- Main Container Card -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:620px;background-color:#FFFFFF;border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,0.08);border:1px solid #E2E8F0;">
          
          <!-- Brand Header Banner -->
          <tr>
            <td align="center" style="background:linear-gradient(135deg, #8E0E00 0%, #C41E3A 50%, #1E1B4B 100%);padding:36px 24px;text-align:center;">
              <table border="0" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <div style="display:inline-block;padding:4px 14px;background-color:#FFC107;color:#8E0E00;font-size:12px;font-weight:800;letter-spacing:1px;border-radius:20px;text-transform:uppercase;margin-bottom:12px;">
                      ★ Admissions 2026–27 Session ★
                    </div>
                    <h1 style="color:#FFFFFF;font-size:26px;font-weight:900;margin:0 0 6px;letter-spacing:-0.5px;">
                      MAYANK CLASSES
                    </h1>
                    <p style="color:#FDE68A;font-size:13px;margin:0;font-weight:600;letter-spacing:0.5px;">
                      PREMIER COACHING FOR NEET-UG • IIT-JEE • FOUNDATION OLYMPIADS
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Confirmation Title & Greeting -->
          <tr>
            <td style="padding:32px 32px 16px;">
              <div style="background-color:#DCFCE7;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-bottom:24px;display:flex;align-items:center;">
                <span style="font-size:22px;margin-right:12px;">✅</span>
                <div>
                  <h3 style="margin:0;color:#166534;font-size:16px;font-weight:800;">
                    Free Demo Class & Counseling Reserved!
                  </h3>
                  <p style="margin:2px 0 0;color:#15803D;font-size:13px;">
                    Your request has been successfully registered with our admissions board.
                  </p>
                </div>
              </div>

              <h2 style="font-size:19px;font-weight:800;color:#0F172A;margin:0 0 10px;">
                Dear {inquiry.full_name},
              </h2>
              <p style="font-size:14px;line-height:1.6;color:#475569;margin:0 0 20px;">
                Thank you for reaching out to <strong>Mayank Classes</strong>. Our senior academic counseling desk has received your request for <strong>{inquiry.course_interested}</strong>. A dedicated faculty counselor is reviewing your profile and will connect with you within <strong>24 hours</strong>.
              </p>

              <!-- Booking Details Table -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#F8FAFC;border-radius:12px;border:1px solid #E2E8F0;margin-bottom:24px;">
                <tr>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:13px;color:#64748B;font-weight:700;width:38%;">
                    Student Name:
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:14px;color:#0F172A;font-weight:800;">
                    {inquiry.full_name}
                  </td>
                </tr>
                <tr>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:13px;color:#64748B;font-weight:700;">
                    Target Program:
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:14px;color:#C41E3A;font-weight:800;">
                    {inquiry.course_interested}
                  </td>
                </tr>
                <tr>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:13px;color:#64748B;font-weight:700;">
                    Current Class / Grade:
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:14px;color:#0F172A;font-weight:700;">
                    {inquiry.current_class}
                  </td>
                </tr>
                <tr>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:13px;color:#64748B;font-weight:700;">
                    Contact Phone:
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #E2E8F0;font-size:14px;color:#0F172A;font-weight:700;">
                    {inquiry.phone}
                  </td>
                </tr>
                <tr>
                  <td style="padding:14px 18px;font-size:13px;color:#64748B;font-weight:700;">
                    Booking Timestamp:
                  </td>
                  <td style="padding:14px 18px;font-size:13px;color:#64748B;">
                    {created_time}
                  </td>
                </tr>
              </table>

              <!-- What to Expect Section -->
              <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 14px;">
                🎯 What Happens Next in Your 6-Step Journey:
              </h3>
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
                <tr>
                  <td style="padding:8px 0;vertical-align:top;width:24px;font-size:16px;">1️⃣</td>
                  <td style="padding:8px 0 8px 10px;font-size:13px;line-height:1.5;color:#334155;">
                    <strong>1-on-1 Mentorship Call:</strong> Our counselor will call you at <strong>{inquiry.phone}</strong> to discuss batch timings, offline vs hybrid modes, and study plans.
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;vertical-align:top;width:24px;font-size:16px;">2️⃣</td>
                  <td style="padding:8px 0 8px 10px;font-size:13px;line-height:1.5;color:#334155;">
                    <strong>Free Live Demo Class Access:</strong> Attend real interactive lectures led by our IIT Roorkee and AIIMS Delhi senior mentors.
                  </td>
                </tr>
                <tr>
                  <td style="padding:8px 0;vertical-align:top;width:24px;font-size:16px;">3️⃣</td>
                  <td style="padding:8px 0 8px 10px;font-size:13px;line-height:1.5;color:#334155;">
                    <strong>Scholarship Test Eligibility:</strong> You qualify for up to <strong>100% tuition scholarship</strong> via the Mayank Classes Diagnostic Test.
                  </td>
                </tr>
              </table>

              <!-- Quick Action Helpline Card -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background:linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);border-radius:12px;border:1px solid #FECDD3;padding:20px;text-align:center;margin-bottom:24px;">
                <tr>
                  <td>
                    <h4 style="margin:0 0 6px;color:#991B1B;font-size:15px;font-weight:800;">
                      Need Immediate Assistance?
                    </h4>
                    <p style="margin:0 0 14px;color:#4C0519;font-size:13px;">
                      Call our counselor desk directly or chat with us on WhatsApp:
                    </p>
                    <a href="tel:+919919980246" style="display:inline-block;padding:10px 20px;background-color:#C41E3A;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:800;font-size:13px;margin:4px;">
                      📞 Call Helpline: +91 9919980246
                    </a>
                    <a href="https://wa.me/919919980246" style="display:inline-block;padding:10px 20px;background-color:#16A34A;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:800;font-size:13px;margin:4px;">
                      💬 WhatsApp Support
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Campus Centers Summary -->
              <p style="font-size:12px;color:#64748B;line-height:1.6;margin:0 0 8px;">
                <strong>Kota Main Campus:</strong> Mayank Towers, Knowledge Park Road, Vigyan Nagar, Kota, Rajasthan – 324005<br>
                <strong>New Delhi Center:</strong> E-14, South Extension Part-II, Main Ring Road, New Delhi – 110049
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color:#0F172A;color:#94A3B8;padding:20px 24px;text-align:center;font-size:12px;border-top:1px solid #1E293B;">
              <p style="margin:0 0 6px;color:#FFFFFF;font-weight:700;">
                Mayank Classes — India's Premier STEM Coaching Institute
              </p>
              <p style="margin:0 0 8px;color:#94A3B8;">
                Email: <a href="mailto:Mayankclasses083@gmail.com" style="color:#FDE68A;text-decoration:none;">Mayankclasses083@gmail.com</a> • Website: <a href="http://127.0.0.1:8000" style="color:#FDE68A;text-decoration:none;">mayankclasses.com</a>
              </p>
              <p style="margin:0;color:#64748B;font-size:11px;">
                This is an automated confirmation email for your counseling inquiry. © 2026 Mayank Classes. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return html_content


def build_admin_notification_html(inquiry):
    """Builds an urgent lead alert HTML email for the institute admin & counselors."""
    created_time = timezone.now().strftime('%d %B %Y, %I:%M %p')
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>New Counseling Lead Alert - Mayank Classes</title>
</head>
<body style="margin:0;padding:20px;background-color:#0F172A;font-family:'Segoe UI',Arial,sans-serif;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:580px;margin:0 auto;background-color:#FFFFFF;border-radius:16px;overflow:hidden;">
    <tr>
      <td style="background:#C41E3A;padding:20px;text-align:center;color:#FFFFFF;">
        <h2 style="margin:0;font-size:20px;font-weight:900;">🚨 NEW COUNSELING / DEMO LEAD</h2>
        <p style="margin:4px 0 0;font-size:13px;color:#FDE68A;">Immediate follow-up recommended (within 2 hours)</p>
      </td>
    </tr>
    <tr>
      <td style="padding:24px;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="font-size:14px;border-collapse:collapse;">
          <tr style="border-bottom:1px solid #E2E8F0;">
            <td style="padding:10px 0;font-weight:bold;color:#475569;width:35%;">Student Name:</td>
            <td style="padding:10px 0;font-weight:bold;color:#0F172A;font-size:16px;">{inquiry.full_name}</td>
          </tr>
          <tr style="border-bottom:1px solid #E2E8F0;">
            <td style="padding:10px 0;font-weight:bold;color:#475569;">Mobile Phone:</td>
            <td style="padding:10px 0;font-weight:bold;color:#C41E3A;font-size:16px;">
              <a href="tel:{inquiry.phone}" style="color:#C41E3A;text-decoration:none;">📞 {inquiry.phone}</a>
            </td>
          </tr>
          <tr style="border-bottom:1px solid #E2E8F0;">
            <td style="padding:10px 0;font-weight:bold;color:#475569;">Email Address:</td>
            <td style="padding:10px 0;color:#0F172A;">
              <a href="mailto:{inquiry.email}" style="color:#0284C7;">{inquiry.email}</a>
            </td>
          </tr>
          <tr style="border-bottom:1px solid #E2E8F0;">
            <td style="padding:10px 0;font-weight:bold;color:#475569;">Course Interested:</td>
            <td style="padding:10px 0;font-weight:bold;color:#7C3AED;">{inquiry.course_interested}</td>
          </tr>
          <tr style="border-bottom:1px solid #E2E8F0;">
            <td style="padding:10px 0;font-weight:bold;color:#475569;">Current Class:</td>
            <td style="padding:10px 0;color:#0F172A;">{inquiry.current_class}</td>
          </tr>
          <tr style="border-bottom:1px solid #E2E8F0;">
            <td style="padding:10px 0;font-weight:bold;color:#475569;">Student Message:</td>
            <td style="padding:10px 0;color:#334155;font-style:italic;">"{inquiry.message}"</td>
          </tr>
          <tr>
            <td style="padding:10px 0;font-weight:bold;color:#475569;">Submitted At:</td>
            <td style="padding:10px 0;color:#64748B;">{created_time}</td>
          </tr>
        </table>

        <div style="margin-top:24px;text-align:center;">
          <a href="tel:{inquiry.phone}" style="display:inline-block;padding:12px 24px;background-color:#16A34A;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;margin-right:8px;">
            📞 Call Student Now
          </a>
          <a href="https://wa.me/{inquiry.phone.replace('+', '').replace(' ', '')}" style="display:inline-block;padding:12px 24px;background-color:#0284C7;color:#FFFFFF;text-decoration:none;border-radius:8px;font-weight:bold;font-size:14px;">
            💬 Open WhatsApp
          </a>
        </div>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return html_content


def _send_email_thread(subject, text_body, html_body, from_email, recipient_list):
    """Worker function executed inside a thread with robust error logging for Railway/Production."""
    clean_recipients = [r.strip() for r in recipient_list if r and isinstance(r, str) and '@' in r.strip()]
    if not clean_recipients:
        print(f"[EMAIL SERVICE] Skipped: No valid recipient found in {recipient_list}")
        return

    # Ensure from_email is valid
    sender = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', 'noreply@mayankclasses.com')

    try:
        print(f"[EMAIL SERVICE] Connecting to {settings.EMAIL_HOST}:{settings.EMAIL_PORT} (TLS={getattr(settings, 'EMAIL_USE_TLS', False)}, SSL={getattr(settings, 'EMAIL_USE_SSL', False)}) to deliver: '{subject}' -> {clean_recipients}")
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=sender,
            to=clean_recipients
        )
        if html_body:
            msg.attach_alternative(html_body, "text/html")
        
        sent_count = msg.send(fail_silently=False)
        print(f"[EMAIL SERVICE SUCCESS] Successfully delivered {sent_count} email(s) to: {clean_recipients}")
        logger.info(f"Email successfully dispatched to: {clean_recipients}")
    except Exception as e:
        import traceback
        err_msg = f"[EMAIL SERVICE ERROR] Failed to deliver email to {clean_recipients}: {type(e).__name__} - {e}"
        print(err_msg)
        traceback.print_exc()
        logger.error(err_msg)


def dispatch_counseling_emails(inquiry):
    """
    Dispatches both Student Confirmation and Admin Alert emails asynchronously.
    Does not block the web response.
    """
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None) or 'Mayank Classes <admissions@mayankclasses.com>'
    admin_recipient = getattr(settings, 'ADMIN_EMAIL_NOTIFICATION', None) or getattr(settings, 'EMAIL_HOST_USER', None)

    # 1. Send Student Confirmation Email (if valid student email provided)
    if inquiry.email and '@' in inquiry.email and not inquiry.email.endswith('@brochure.mayankclasses.com'):
        student_subject = f"🎯 Demo Class & Counseling Booking Confirmed - Mayank Classes"
        student_text = (
            f"Dear {inquiry.full_name},\n\n"
            f"Thank you for choosing Mayank Classes! Your free demo class and counseling booking for '{inquiry.course_interested}' has been received.\n"
            f"Our senior academic counselor will call you within 24 hours at {inquiry.phone}.\n\n"
            f"Admissions Helpline: +91 9919980246\n"
            f"Website: https://mayankclasses.com\n\n"
            f"— Mayank Classes Admissions Board"
        )
        student_html = build_student_confirmation_html(inquiry)

        t1 = threading.Thread(
            target=_send_email_thread,
            args=(student_subject, student_text, student_html, from_email, [inquiry.email]),
            daemon=True
        )
        t1.start()

    # 2. Send Admin / Counselor Lead Notification Email (if admin email configured)
    if admin_recipient and '@' in admin_recipient:
        admin_subject = f"🚨 [NEW LEAD] {inquiry.full_name} - {inquiry.course_interested} ({inquiry.phone})"
        admin_text = (
            f"NEW INQUIRY RECEIVED:\n"
            f"Name: {inquiry.full_name}\n"
            f"Phone: {inquiry.phone}\n"
            f"Email: {inquiry.email}\n"
            f"Course: {inquiry.course_interested}\n"
            f"Class: {inquiry.current_class}\n"
            f"Message: {inquiry.message}\n"
        )
        admin_html = build_admin_notification_html(inquiry)

        t2 = threading.Thread(
            target=_send_email_thread,
            args=(admin_subject, admin_text, admin_html, from_email, [admin_recipient]),
            daemon=True
        )
        t2.start()

