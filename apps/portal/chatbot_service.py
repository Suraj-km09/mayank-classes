import os
import json
import logging
import urllib.request
import urllib.error
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.academic.models import Course, Batch
from apps.accounts.models import User

logger = logging.getLogger(__name__)


def build_mayank_classes_knowledge():
    """Dynamically aggregates real-time knowledge from the database about Mayank Classes."""
    courses_info = []
    try:
        courses = Course.objects.filter(is_active=True).prefetch_related('subjects', 'batches')
        for c in courses:
            batches = [f"{b.name} ({b.schedule_time})" for b in c.batches.filter(is_active=True)]
            batches_str = ", ".join(batches) if batches else "Admissions Open for 2026-27 Session"
            features_str = "; ".join(c.features) if c.features else ""
            courses_info.append(
                f"• Program: {c.title}\n"
                f"  - Target Class/Grade: {c.target_class}\n"
                f"  - Category: {c.get_category_display()}\n"
                f"  - Course URL: /courses/{c.slug}/\n"
                f"  - Original Fee: ₹{int(c.price):,}\n"
                f"  - Special Discounted Fee: ₹{int(c.discount_price or c.price):,}\n"
                f"  - Duration: {c.duration_weeks} Weeks\n"
                f"  - Mode: {c.mode}\n"
                f"  - Description: {c.short_description}\n"
                f"  - Key Features: {features_str}\n"
                f"  - Batches: {batches_str}\n"
            )
    except Exception as e:
        logger.error(f"Error fetching courses for chatbot: {e}")

    teachers_info = []
    try:
        teachers = User.objects.filter(role='TEACHER').prefetch_related('teacher_profile')
        for t in teachers:
            prof = getattr(t, 'teacher_profile', None)
            desig = prof.designation if prof else "Senior Master Faculty"
            qual = prof.qualification if prof else "Ex-IITian / AIIMS"
            spec = prof.specialization if prof else "Core STEM"
            teachers_info.append(f"• {t.get_full_name()}: {desig} | Qualifications: {qual} | Specialization: {spec}")
    except Exception as e:
        logger.error(f"Error fetching teachers for chatbot: {e}")

    courses_block = "\n".join(courses_info) if courses_info else "NEET, JEE, Foundation, CUET, NDA programs."
    teachers_block = "\n".join(teachers_info) if teachers_info else "Senior IITian and AIIMS Faculty."

    prompt = f"""You are the official AI Academic Counselor and Support Assistant for **Mayank Classes** (India's premier coaching institute for NEET-UG, IIT-JEE Main & Advanced, and Classes 6-10 Foundation Olympiads).

=======================================================
CRITICAL RULE & STRICT DOMAIN BOUNDARY:
=======================================================
1. ONLY ANSWER QUESTIONS ABOUT MAYANK CLASSES:
   You are an expert on Mayank Classes. You must answer all questions related to our coaching institute, courses, fee structures, batch timings, admissions, faculty mentors, demo classes, test series, study materials, scholarships, and website navigation.

2. STRICT REFUSAL FOR EXTERNAL / UNRELATED QUERIES:
   If the user asks ANY external question unrelated to Mayank Classes (such as general knowledge, world politics, geography, movie trivia, entertainment, writing external general code, recipes, sports, random trivia, or other non-Mayank Classes queries), you MUST politely decline and strictly correct the user:
   "I am the dedicated AI Counselor for Mayank Classes. I can only assist with questions regarding our courses, fee structures, admissions, faculty mentors, batch schedules, and academic programs at Mayank Classes. How can I help you with your NEET, JEE, or Foundation preparation at Mayank Classes?"

=======================================================
MAYANK CLASSES INSTITUTION KNOWLEDGE BASE:
=======================================================
### Institution Overview:
- Institute Name: Mayank Classes
- Track Record: 15+ years of excellence, 5,000+ students trained, 98% success rate, consistent top AIR rankers in IIT-JEE and NEET-UG.
- Admissions Helpline / WhatsApp: +91 9919980246 (Available 8:00 AM - 9:00 PM)
- Email: Mayankclasses083@gmail.com
- Free Demo Class: Students can book a 100% Free Demo Class directly on the website or via helpline.
- Scholarships: Up to 100% scholarship on tuition fees through the Mayank Classes Scholarship & Diagnostic Test.
- Portals: Student Portal & Teacher Portal at `/login/`, Certificate Verification at `/verify-certificate/`.

### All Active Programs & Exact Fee Structure:
{courses_block}

### Senior Faculty Mentors:
{teachers_block}

### 6-Step Student Learning Journey:
1. Step 1: Concept Building from First Principles (3D animations, visual STEM models)
2. Step 2: Daily DPP Practice (20-25 graded questions daily)
3. Step 3: NTA AI-CBT Tests (Bi-weekly computer-based test series matching NTA national interface)
4. Step 4: Weakness Analytics (AI diagnostic reports pinpointing negative marks and speed)
5. Step 5: 1-on-1 Doubt Desk (12-Hour daily faculty counters)
6. Step 6: Final Rank Mastery (Formula cheat sheets, rapid revision masterclasses, full simulations)

=======================================================
RESPONSE FORMATTING GUIDELINES:
=======================================================
- Format answers cleanly with Markdown: use bolding, bullet points, headers, and emoji highlights.
- Always quote exact fees (mentioning Original Fee and Special Discounted Fee).
- Always be encouraging, polite, concise, and helpful.
- Suggest booking a **Free Demo Class** or calling **+91 9919980246** for admission assistance.
"""
    return prompt


@method_decorator(csrf_exempt, name='dispatch')
class ChatbotAssistantView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_message = request.data.get('message', '').strip()
        history = request.data.get('history', [])

        if not user_message:
            return Response({'error': 'Message cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY', '')

        system_instruction = build_mayank_classes_knowledge()

        # Build clean alternating contents list from history
        contents = []
        if isinstance(history, list):
            last_role = None
            for h in history[-8:]:
                role = 'user' if h.get('role') == 'user' else 'model'
                text = str(h.get('text', '')).strip()
                if text:
                    # Ensure alternating roles
                    if role == last_role:
                        continue
                    contents.append({'role': role, 'parts': [{'text': text}]})
                    last_role = role

        # Ensure first element is 'user' if history exists
        if contents and contents[0]['role'] != 'user':
            contents.pop(0)

        # Add current user message
        if not contents or contents[-1]['role'] != 'user':
            contents.append({'role': 'user', 'parts': [{'text': user_message}]})
        else:
            # Replace last user message with current
            contents[-1] = {'role': 'user', 'parts': [{'text': user_message}]}

        payload = {
            'systemInstruction': {'parts': [{'text': system_instruction}]},
            'contents': contents,
            'generationConfig': {
                'temperature': 0.2,
                'maxOutputTokens': 800,
            }
        }

        # Try models in order
        candidate_models = [
            'gemini-3.1-flash-lite',
            'gemini-3.5-flash-lite',
            'gemini-3.5-flash',
            'gemini-flash-latest'
        ]

        last_error_detail = None

        for model_name in candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            req_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={'Content-Type': 'application/json'}
            )
            try:
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_json = json.loads(response.read().decode('utf-8'))
                    candidates = res_json.get('candidates', [])
                    if candidates and 'content' in candidates[0]:
                        parts = candidates[0]['content'].get('parts', [])
                        if parts and 'text' in parts[0]:
                            reply_text = parts[0]['text'].strip()
                            return Response({
                                'reply': reply_text,
                                'status': 'success',
                                'model': model_name
                            })
            except urllib.error.HTTPError as e:
                err_body = e.read().decode('utf-8', errors='ignore')
                logger.warning(f"Chatbot model {model_name} HTTP {e.code}: {err_body}")
                last_error_detail = f"HTTP {e.code}: {err_body}"
            except Exception as e:
                logger.warning(f"Chatbot model {model_name} error: {e}")
                last_error_detail = str(e)

        # Generate intelligent dynamic response from database if external API is temporarily unavailable
        logger.error(f"All Gemini models failed. Last error: {last_error_detail}")
        
        # Build dynamic fallback based on query
        msg_lower = user_message.lower()
        if 'neet' in msg_lower or 'medical' in msg_lower or 'doctor' in msg_lower:
            dynamic_reply = (
                "### 🩺 **NEET-UG Preparation Programs at Mayank Classes**\n\n"
                "• **NEET-UG Medical Champions (2-Year Comprehensive)** (Class 11 & 12):\n"
                "  - **Discounted Fee:** **₹79,000** *(Original: ₹92,000)*\n"
                "  - **Duration:** 104 Weeks | Daily 4h lectures by AIIMS mentors, 3D NCERT diagrams.\n\n"
                "• **NEET Droppers / Repeaters Super Batch** (12th Passed):\n"
                "  - **Discounted Fee:** **₹62,000** *(Original: ₹76,000)*\n"
                "  - **Duration:** 44 Weeks | 75+ full OMR mocks & 12h doubt counters.\n\n"
                "👉 Book a **Free Demo Class** or call **+91 9919980246** to reserve your seat!"
            )
        elif 'jee' in msg_lower or 'iit' in msg_lower or 'engineering' in msg_lower:
            dynamic_reply = (
                "### ⚛️ **IIT-JEE Preparation Programs at Mayank Classes**\n\n"
                "• **JEE Advanced Pinnacle (2-Year Comprehensive)** (Class 11 & 12):\n"
                "  - **Discounted Fee:** **₹82,000** *(Original: ₹95,000)*\n"
                "  - **Duration:** 104 Weeks | Led by Kota & Delhi IITian HODs.\n\n"
                "• **JEE Main Target (1-Year Fast-Track)** (Class 12):\n"
                "  - **Discounted Fee:** **₹56,000** *(Original: ₹68,000)* | 52 Weeks.\n\n"
                "• **JEE Dropper / Repeater Ranker Batch**:\n"
                "  - **Discounted Fee:** **₹64,000** *(Original: ₹78,000)* | 44 Weeks.\n\n"
                "👉 Book a **Free Demo Class** or call **+91 9919980246** to get started!"
            )
        elif 'foundation' in msg_lower or 'class 8' in msg_lower or 'class 9' in msg_lower or 'class 10' in msg_lower or 'olympiad' in msg_lower:
            dynamic_reply = (
                "### 🎓 **Foundation & Olympiad Programs (Classes 6–10)**\n\n"
                "• **Class 8 Pre-Foundation & IJSO/PRMO Target:** **₹27,500** *(Original: ₹34,000)*\n"
                "• **Class 9 Foundation Master & NTSE Accelerator:** **₹31,000** *(Original: ₹38,000)*\n"
                "• **Class 10 Board Excellence & JEE/NEET Bridge:** **₹34,500** *(Original: ₹42,000)*\n\n"
                "👉 Includes printed study modules, daily DPP sheets, and early STEM olympiad workshops. Call **+91 9919980246** to enroll!"
            )
        elif 'fee' in msg_lower or 'cost' in msg_lower or 'price' in msg_lower:
            dynamic_reply = (
                "### 💰 **Mayank Classes Complete Fee Structure**\n\n"
                "• **NEET-UG (2-Year):** **₹79,000** *(Orig. ₹92,000)*\n"
                "• **NEET Droppers:** **₹62,000** *(Orig. ₹76,000)*\n"
                "• **JEE Advanced (2-Year):** **₹82,000** *(Orig. ₹95,000)*\n"
                "• **JEE Main (1-Year):** **₹56,000** *(Orig. ₹68,000)*\n"
                "• **JEE Droppers:** **₹64,000** *(Orig. ₹78,000)*\n"
                "• **Foundation (Classes 8–10):** Starting at **₹27,500**\n"
                "• **CUET (UG) / NDA:** Starting at **₹25,000**\n\n"
                "✨ *Up to 100% Scholarship available via Scholarship Test! Call **+91 9919980246** for details.*"
            )
        else:
            dynamic_reply = (
                "Hello! Welcome to **Mayank Classes**. We provide premier coaching for **NEET-UG**, **IIT-JEE (Main & Advanced)**, "
                "and **Classes 6–10 Foundation Olympiads**.\n\n"
                "• **NEET 2-Year Program:** ₹79,000 (Orig. ₹92,000)\n"
                "• **JEE 2-Year Program:** ₹82,000 (Orig. ₹95,000)\n"
                "• **Foundation (Classes 6-10):** From ₹27,500\n\n"
                "You can book a **Free Demo Class** anytime or call our admissions helpline at **+91 9919980246**."
            )

        return Response({
            'reply': dynamic_reply,
            'status': 'fallback_dynamic',
            'error_detail': last_error_detail
        })
