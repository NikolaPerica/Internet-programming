from .models import User, Subjects, Enrollment
from django.forms import CharField,PasswordInput
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','role']

class addUserForm(forms.ModelForm):
    password = CharField(widget=PasswordInput())
    
    class Meta:
        model=User
        fields=['username','email', 'first_name', 'last_name','password','role']
class UserChangeForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class PredmetForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'izborni', 'nositelj']

    def __init__(self, *args, **kwargs):
        super(PredmetForm, self).__init__(*args, **kwargs)
        self.fields['nositelj'].queryset = User.objects.filter(role='prof')

class changePredmetForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields=('name', 'kod','nositelj')
    def __init__(self, *args, **kwargs):
        super(changePredmetForm, self).__init__(*args, **kwargs)
        self.fields['nositelj'].queryset = User.objects.filter(role='prof')

class UpisForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['user_id', 'predmet_id','status']

    def __init__(self, *args, **kwargs):
        super(UpisForm, self).__init__(*args, **kwargs)
        
class changeUpisForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['user_id','predmet_id', 'status']

    def __init__(self, *args, **kwargs):
        super(changeUpisForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].disabled = True

class profEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['status']