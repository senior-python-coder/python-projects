from django.db import models
from django.utils import timezone

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    email = models.EmailField()
    enrolled_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.full_name


class Subject(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.FloatField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.title}: {self.score}"

# def student_list(request, *args, **kwargs):
#     students = Student.objects.all()
#     output = "<h1>Talabalar ro‘yxati</h1><ul>"
#     for student in students:
#         output += f"<li>{student.full_name} ({student.faculty.name}) - {student.email}</li>"
#     output += "</ul>"
#     return HttpResponse(output)
