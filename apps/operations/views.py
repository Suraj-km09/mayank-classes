from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Attendance, FeeRecord, Certificate
from .serializers import AttendanceSerializer, FeeRecordSerializer, CertificateSerializer
from apps.academic.models import Batch
from apps.accounts.models import User
from apps.core.permissions import IsTeacherOrAdmin, IsAdminRole

class AttendanceListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        batch_id = request.query_params.get('batch_id')
        date_str = request.query_params.get('date')

        if user.is_student_role():
            queryset = Attendance.objects.filter(student=user)
            if batch_id:
                queryset = queryset.filter(batch_id=batch_id)
            serializer = AttendanceSerializer(queryset, many=True)
            return Response(serializer.data)

        # Teacher or Admin
        queryset = Attendance.objects.all()
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
        if date_str:
            queryset = queryset.filter(date=date_str)

        serializer = AttendanceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Bulk mark attendance for a batch.
        Payload format:
        {
            "batch_id": 1,
            "date": "2026-08-26",
            "records": [
                {"student_id": 4, "status": "PRESENT", "remarks": ""},
                {"student_id": 5, "status": "ABSENT", "remarks": "Medical leave"}
            ]
        }
        """
        if not (request.user.is_teacher_role() or request.user.is_admin_role()):
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        batch_id = request.data.get('batch_id')
        date_val = request.data.get('date', timezone.now().date())
        records = request.data.get('records', [])
        if isinstance(records, str):
            import json
            try:
                records = json.loads(records)
            except Exception:
                records = []

        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return Response({'error': 'Batch not found.'}, status=status.HTTP_404_NOT_FOUND)

        saved_records = []
        for r in records:
            student_id = r.get('student_id')
            status_val = r.get('status', 'PRESENT')
            remarks = r.get('remarks', '')

            student = User.objects.filter(id=student_id).first()
            if student:
                attendance, created = Attendance.objects.update_or_create(
                    batch=batch,
                    student=student,
                    date=date_val,
                    defaults={
                        'status': status_val,
                        'marked_by': request.user,
                        'remarks': remarks
                    }
                )
                saved_records.append(attendance)

        return Response({
            'message': f'Attendance marked for {len(saved_records)} students on {date_val}.',
            'records': AttendanceSerializer(saved_records, many=True).data
        }, status=status.HTTP_200_OK)

class StudentAttendanceStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_student_role():
            student_id = request.query_params.get('student_id')
            if student_id:
                user = User.objects.filter(id=student_id).first() or user

        total = Attendance.objects.filter(student=user).count()
        present = Attendance.objects.filter(student=user, status='PRESENT').count()
        late = Attendance.objects.filter(student=user, status='LATE').count()
        absent = Attendance.objects.filter(student=user, status='ABSENT').count()

        percentage = round(((present + (0.5 * late)) / total * 100.0), 1) if total > 0 else 100.0

        return Response({
            'total_classes': total,
            'present_count': present,
            'late_count': late,
            'absent_count': absent,
            'attendance_percentage': percentage
        })

class FeeRecordListView(generics.ListCreateAPIView):
    serializer_class = FeeRecordSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return FeeRecord.objects.none()

        if user.is_student_role():
            return FeeRecord.objects.filter(student=user)
        
        queryset = FeeRecord.objects.all()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

class FeePaySimulationView(APIView):
    """
    Simulates making an online payment for a pending fee record.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, invoice_id):
        try:
            fee = FeeRecord.objects.get(id=invoice_id)
        except FeeRecord.DoesNotExist:
            return Response({'error': 'Invoice not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_student_role() and fee.student != request.user:
            return Response({'error': 'You can only pay for your own invoices.'}, status=status.HTTP_403_FORBIDDEN)

        amount = request.data.get('amount', fee.due_amount)
        payment_mode = request.data.get('payment_mode', 'UPI')
        
        fee.paid_amount = float(fee.paid_amount) + float(amount)
        if fee.paid_amount >= float(fee.total_amount):
            fee.status = 'PAID'
        else:
            fee.status = 'PARTIAL'

        fee.payment_mode = payment_mode
        fee.payment_date = timezone.now().date()
        fee.transaction_id = f"TXN-MAYANK-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        fee.receipt_url = f"/api/fees/{fee.id}/receipt/"
        fee.save()

        return Response({
            'message': 'Payment processed successfully.',
            'invoice': FeeRecordSerializer(fee).data
        }, status=status.HTTP_200_OK)

class CertificateListView(generics.ListCreateAPIView):
    serializer_class = CertificateSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Certificate.objects.none()
        if user.is_student_role():
            return Certificate.objects.filter(student=user)
        return Certificate.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

class CertificateVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, code):
        cert = Certificate.objects.filter(verification_code=code).first()
        if not cert:
            cert = Certificate.objects.filter(certificate_number=code).first()

        if not cert:
            return Response({'valid': False, 'message': 'Invalid certificate identifier.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'valid': True,
            'certificate': CertificateSerializer(cert).data
        })
