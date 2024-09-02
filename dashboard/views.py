import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .serializers import CarOwnerSerializer, ListAllCarOwnerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CarOwner, Car, Permission, Camera, CarEntry
from django.utils import timezone
from rest_framework import generics
from io import BytesIO
import jdatetime


# AUTH
class ValidateAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_active:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# Main Dashboard
class Statistics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localtime(timezone.now())
        #today = timezone.now().date()

        # Statistics
        start_of_today = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        end_of_today = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

        total_owners = CarOwner.objects.count()
        total_cars = Car.objects.count()
        allowed_permissions = Permission.objects.filter(isAllowed=True, endDate__gte=start_of_today).count()
        not_allowed_permissions = Permission.objects.filter(isAllowed=False).count()
        total_cameras = Camera.objects.count()
        today_entries = CarEntry.objects.filter(timestamp__gte=start_of_today, timestamp__lt=end_of_today).count()
        total_entries = CarEntry.objects.count()

        # Fetch 10 most recent entries
        recent_entries = CarEntry.objects.order_by('-timestamp')[:10]

        # Format recent entries data
        recent_entries_data = [
            {
                "license_plate": entry.license_plate.license_plate,
                "camera_location": entry.camera.location,
                "is_entry_camera": entry.camera.is_entry_camera,
                "timestamp": jdatetime.datetime.fromgregorian(datetime=timezone.localtime(entry.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            }
            for entry in recent_entries
        ]

        # Prepare response data
        data = {
            "Statistics":
            {
                "تعداد مالکان": total_owners,
                "تعداد ماشین‌ها": total_cars,
                "تعداد مجوزهای فعال": allowed_permissions,
                "تعداد مجوزهای منقضی شده": not_allowed_permissions,
                "تعداد دوربین‌ها": total_cameras,
                "تعداد ورودی‌/خروجی‌های امروز": today_entries,
                "تعداد کل ورودی/خروجی‌ها": total_entries,
            },
            "recent_entries": recent_entries_data
        }

        return Response(data)
    

class GenerateReport(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve license plate from request data
        license_plate = request.data.get('license_plate')
        if not license_plate:
            return Response({"error": "License plate is required."}, status=400)

        # Fetch car, owner, and related information
        try:
            car = Car.objects.select_related('owner').get(license_plate=license_plate)
            owner = car.owner
        except Car.DoesNotExist:
            return Response({"error": "Car with this license plate does not exist."}, status=404)

        # Fetch the last 10 entries
        last_10_entries = CarEntry.objects.filter(license_plate=car).order_by('-timestamp')[:10]

        # Fetch permission details
        permissions = Permission.objects.filter(license_plate=car)

        # Create a buffer to hold the PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Draw the report title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, height - 100, f"Report for License Plate: {license_plate}")
        p.setFont("Helvetica", 12)
        p.drawString(100, height - 120, f"Generated on: {jdatetime.datetime.fromgregorian(datetime=timezone.now()).strftime('%Y-%m-%d %H:%M:%S')}")

        # Draw owner information
        p.drawString(100, height - 150, "Owner Information:")
        p.drawString(120, height - 170, f"Name: {owner.firstName} {owner.lastName}")
        p.drawString(120, height - 190, f"National Code: {owner.nationalCode}")
        p.drawString(120, height - 210, f"Phone Number: {owner.phoneNumber}")
        p.drawString(120, height - 230, f"Date of Birth: {jdatetime.datetime.fromgregorian(date=owner.dateOfBirth).strftime('%Y-%m-%d')}")
        p.drawString(120, height - 250, f"Career: {owner.career}")

        # Draw car information
        p.drawString(100, height - 280, "Car Information:")
        p.drawString(120, height - 300, f"Color: {car.color}")
        p.drawString(120, height - 320, f"Model: {car.model}")

        # Draw last 10 entries
        p.drawString(100, height - 350, "Last 10 Entries:")
        y_position = height - 370
        for entry in last_10_entries:
            p.drawString(120, y_position, f"{jdatetime.datetime.fromgregorian(datetime=timezone.localtime(entry.timestamp)).strftime('%Y-%m-%d %H:%M:%S')} - Camera: {entry.camera.location} - Is Entry Camera: {entry.camera.is_entry_camera}")
            y_position -= 20

        # Draw permission details
        p.drawString(100, y_position - 20, "Permissions:")
        y_position -= 40
        for permission in permissions:
            status = "Allowed" if permission.isAllowed else "Not Allowed"
            p.drawString(120, y_position, f"From: {jdatetime.datetime.fromgregorian(datetime=timezone.localtime(permission.startDate)).strftime('%Y-%m-%d %H:%M:%S')} "
                                          f"To: {jdatetime.datetime.fromgregorian(datetime=timezone.localtime(permission.endDate)).strftime('%Y-%m-%d %H:%M:%S')} "
                                          f"- Status: {status}")
            y_position -= 20

        # Close the PDF object cleanly
        p.showPage()
        p.save()

        # Get the PDF content from the buffer
        pdf = buffer.getvalue()
        buffer.close()

        # Return the PDF as an HTTP response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{license_plate}.pdf"'
        return response
    

# Owner
class AddOwner(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CarOwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Car owner added successfully."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors, "message": "Failed to add car owner. Please check the input data."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class CarOwnerListView(generics.ListAPIView):
    queryset = CarOwner.objects.all()
    serializer_class = ListAllCarOwnerSerializer
    permission_classes = [IsAuthenticated]



# Cars
class CarListView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = ListAllCarOwnerSerializer
    permission_classes = [IsAuthenticated]