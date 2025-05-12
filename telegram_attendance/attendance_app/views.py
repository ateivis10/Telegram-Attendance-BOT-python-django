from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Attendance

def attendance_table(request):
    employee_name = request.GET.get('employee')
    date = request.GET.get('date')

    attendance_records = Attendance.objects.select_related('employee').all().order_by('-date')

    if employee_name:
        attendance_records = attendance_records.filter(employee__full_name__icontains=employee_name)

    if date:
        attendance_records = attendance_records.filter(date=date)

    paginator = Paginator(attendance_records, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'attendance_app/attendance_table.html', {
        'page_obj': page_obj,
        'request': request,
    })
