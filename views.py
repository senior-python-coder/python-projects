from django.http import HttpResponse
from .models import Student

def student_list(request):
    students = Student.objects.all()
    output = "<h1>Talabalar ro‘yxati</h1><ul>"
    for student in students:
        output += f"<li>{student.full_name} ({student.faculty.name}) - {student.email}</li>"
    output += "</ul>"

    # Admin panelga link qo‘shamiz
    output += """
        <hr>
        <p style='text-align:center;'>
            <a href='/admin/' style='padding:10px 20px; background:#3498db; color:white; text-decoration:none; border-radius:5px;'>
                Admin paneli ->
            </a>
        </p>
    """

    return HttpResponse(output)
