from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

    
class Role(models.Model):
    ROLE_CHOICES = (('admin', 'Admin'), ('profesor', 'Profesor'), ('student', 'Student') )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_role_display()


class StudentStatus(models.TextChoices):
    NONE = 'none', 'None'
    REDOVNI = 'redovni', 'Redovni'
    IZVANREDNI = 'izvanredni', 'Izvanredni'
    


class MandatoryStatus(models.TextChoices):
    DA = 'da', 'Da'
    NE = 'ne', 'Ne'
    

class SubjectStatus(models.TextChoices):
    UPISAN = 'upisan', 'Upisan'
    POTPIS_IZGUBLJEN = 'potpis izgubljen', 'Potpis izgubljen'
    POLOZEN = 'polozen', 'Polozen'
    


class User(AbstractUser):
    status = models.CharField(max_length=20, choices=StudentStatus.choices, default=StudentStatus.NONE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)


class Subjects(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    program = models.TextField()
    bodovi = models.IntegerField()
    sem_redovni = models.IntegerField()
    sem_izvanredni = models.IntegerField()
    izborni = models.CharField(max_length=3, choices=MandatoryStatus.choices, default=MandatoryStatus.DA)
    nositelj = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__role': 'profesor'}
)


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=SubjectStatus.choices, default=SubjectStatus.UPISAN)
