from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db import models
from django.contrib import messages
from .models import *
from django.db.models import Q

# Create your views here.

def home(request):
    current_user = request.user
    if  current_user.is_authenticated:    
         if current_user.role=='adm':
             return redirect('super')
         elif current_user.role=='stu':
             return redirect('student')
         elif current_user.role=='prof':
             return redirect('profesor')
    else:
        return render(request,'projekti/home.html')

@login_required
def admin_home(request):
    current_user = request.user
    if current_user.role=='adm':
        return render(request,'projekti/admin.html',{'user':current_user})
def stud_home(request):
    current_user = request.user
    if current_user.role=='stu':
        return render(request,'projekti/student.html',{'user':current_user})
def prof_home(request):
    current_user = request.user
    if current_user.role=='prof':
        return render(request,'projekti/profesor.html',{'user':current_user})

def adduser(request):
    if request.method=='POST':
         ap_form=addUserForm(request.POST)
         if ap_form.is_valid():
            first_name = ap_form.cleaned_data['username']
            passw = make_password(ap_form.cleaned_data['password'])
            stat = ap_form.cleaned_data['role']
            user=User(username=first_name, password=passw, role=stat)
            user.save()
            username=ap_form.cleaned_data.get('username')
            messages.success(request,f'User  {username} created !')
            return redirect('home')
    else:
        ap_form=addUserForm()
    context={'ap_form':ap_form,}   
    return render(request,'projekti/adduser.html',context)

def edituser(request,pk):
    user=User.objects.get(id=pk)
    eu_form=UserChangeForm(instance=user)
    if request.method=='POST':
         eu_form=UserChangeForm(request.POST,instance=user)
         if eu_form.is_valid():
            eu_form.save()
            username=eu_form.cleaned_data.get('username')
            messages.success(request,f'User  {username} updated !')
            return redirect('home')
    context={'eu_form':eu_form,
    }
    return render(request,'projekti/edituser.html',context)

def editpredmet(request,pk):
    predmet=Subjects.objects.get(id=pk)
    eu_form=changePredmetForm(instance=predmet)
    if request.method=='POST':
         eu_form=changePredmetForm(request.POST,instance=predmet)
         if eu_form.is_valid():
            eu_form.save()
            name=eu_form.cleaned_data.get('name')
            messages.success(request,f'User  {name} updated !')
            return redirect('home')
    context={'eu_form':eu_form,
    }
    return render(request,'projekti/editpredmet.html',context)

def professors(request):
    professors = User.objects.filter(role='prof')
    context = {'professors': professors}
    return render(request, 'projekti/professors.html', context)

def students(request):
    students=User.objects.filter(role='stu')
    context={'students': students}
    return render(request,'projekti/students.html',context)

def Subjects(request):
    Subjects=Subjects.objects.all()
    context={'Subjects': Subjects}
    return render(request,'projekti/Subjects.html',context)

def addpredmet(request):
    if request.method=='POST':
         p_form=PredmetForm(request.POST)
         if p_form.is_valid():
            p_name = p_form.cleaned_data ['name']
            p_kod = p_form.cleaned_data['kod']
            p_program =p_form.cleaned_data['program']
            p_ects = p_form.cleaned_data['ects']
            p_sem_red =p_form.cleaned_data['sem_red']
            p_sem_izv =p_form.cleaned_data['sem_izv']
            p_izborni =p_form.cleaned_data['izborni']
            p_nositelj =p_form.cleaned_data['nositelj']
            predmet=Subjects(name=p_name,
                            kod=p_kod,
                            program=p_program,
                            ects=p_ects,
                            sem_red=p_sem_red,
                            sem_izv=p_sem_izv,
                            izborni=p_izborni,
                            nositelj=p_nositelj)
            predmet.save()
            predmet=p_form.cleaned_data.get('name')
            messages.success(request,f'Predmet {p_name} created !')
            return redirect('home')
    else:
        p_form=PredmetForm()
    context={'p_form':p_form,}   
    return render(request,'projekti/addpredmet.html',context)

def addupis(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        ap_form = UpisForm(request.POST)
        if ap_form.is_valid():
            upis = ap_form.save(commit=False)
            passw =ap_form.cleaned_data['predmet_id']
            stat = ap_form.cleaned_data['status']
            upis = Enrollment(user_id=user, predmet_id=passw, status=stat)
            upis.save()
            return redirect('home')
    else:
        
        initial_data = {'user_id': user.id}
        ap_form = UpisForm(initial=initial_data)
        ap_form.fields['user_id'].disabled = True
    context = {'ap_form': ap_form}
    return render(request, 'projekti/addupis.html', context)

def listupis(request,pk):
    user = User.objects.get(id=pk)
    Enrollment=Enrollment.objects.filter(user_id=user.id)
    context={'Enrollment': Enrollment}
    return render(request,'projekti/Enrollment.html',context)

def change_upis(request, pk):
    upis = Enrollment.objects.get(id=pk)
    if request.method == 'POST':
        form = changeUpisForm(request.POST, instance=upis)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = changeUpisForm(instance=upis)
    context = {'form': form}
    return render(request, 'projekti/editupis.html', context)

def list_users_per_predmet(request, pk):
    predmet = Subjects.objects.get(id=pk)
    users = predmet.Enrollment_set.all().values('user_id__username')
    context = {'predmet': predmet, 'users': users}
    return render(request, 'projekti/liststud.html', context)

def listpredmet(request):
    user = request.user
    Subjects = Subjects.objects.filter(nositelj=user)
    context = {'Subjects': Subjects}
    return render(request, 'projekti/profpred.html', context)

def liststud(request,pk):
    predmet = Subjects.objects.get(id=pk)
    izgubili_potpis = Enrollment.objects.filter(predmet_id=predmet, status='fail')
    dobili_potpis = Enrollment.objects.filter(predmet_id=predmet, status='up')
    polozili_predmet = Enrollment.objects.filter(predmet_id=predmet, status='pass')
    context = {
        'predmet': predmet,
        'izgubili_potpis': izgubili_potpis,
        'dobili_potpis': dobili_potpis,
        'polozili_predmet': polozili_predmet
    }
    return render(request, 'projekti/studpred.html', context)

def changestatus(request,pk,fk):
    user = User.objects.get(username=pk)
    Enrollment=Enrollment.objects.get(user_id=user,predmet_id=fk)
    if request.method == 'POST':
        form = profEnrollmentForm(request.POST, instance=Enrollment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = profEnrollmentForm(instance=Enrollment)
    return render(request, 'projekti/editupis.html', {'form': form})

def listpred(request):
    Subjects=Subjects.objects.all()
    context={'Subjects':Subjects}
    return render(request,'projekti/predstud.html',context)

def add_upis_student(request, pk):
    user = request.user 
    predmet = Subjects.objects.get(id=pk)
    
    if request.method == 'POST':
        form = UpisForm(request.POST)
        print(form.errors)
        if form.is_valid():
            upis = form.save(commit=False)
            upis.user_id = user
            upis.predmet_id = predmet
            upis.save()
            return redirect('home')
    else:
        form = UpisForm(initial={'user_id': user, 'predmet_id': predmet})
        form.fields['user_id'].disabled = True
        form.fields['predmet_id'].disabled = True
        
    
    context = {'form': form}
    return render(request, 'projekti/addupisstud.html', context)

def current_Enrollment(request):
    user = request.user
    Enrollment = Enrollment.objects.filter(user_id=user)
    context = {'Enrollment': Enrollment}
    return render(request, 'projekti/studEnrollment.html', context)

def delete_upis(request, upis_id):
    upis = get_object_or_404(Enrollment, id=upis_id, status='up')

    if request.method == 'POST':
        upis.delete()
        return redirect('home')

    context = {'upis': upis}
    return render(request, 'projekti/delete_upis.html', context)

def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    
    return render(request, 'projekti/delete_user.html', {'user': user})

def upis_studenta(request, student_id):
    user = User.objects.get(id=student_id)
    Enrollment = Enrollment.objects.filter(user_id=student_id)
    ap_form = UpisForm(request.POST or None)
    
    if request.method == 'POST':
        if ap_form.is_valid():
            upis = ap_form.save(commit=False)
            passw = ap_form.cleaned_data['predmet_id']
            stat = ap_form.cleaned_data['status']
            upis.user_id = user
            upis.predmet_id = passw
            
            if user.status == 'red':
                Subjects = Subjects.objects.filter(Q(sem_red=1) | Q(sem_red=2))
                for predmet in Subjects:
                    upis_obj = Enrollment.filter(predmet_id=predmet.id).first()
                    if upis_obj and upis_obj.status != 'pass':
                        return HttpResponse("Nije sve polozeno s 1. godine")
            
            elif user.status == 'izv':
                Subjects = Subjects.objects.filter(Q(sem_izv=1) | Q(sem_izv=2) | Q(sem_izv=3) | Q(sem_izv=4))
                for predmet in Subjects:
                    upis_obj = Enrollment.filter(predmet_id=predmet.id).first()
                    if upis_obj and upis_obj.status != 'pass':
                        return HttpResponse("Nije sve polozeno s 1. godine ili 2. godine")
                    if(Enrollment.objects.filter(predmet_id=predmet.id,user_id=student_id)):
                        return HttpResponse("Postoji")
            upis.save()
            return redirect('home')
    else:
        ap_form = UpisForm(initial={'user_id': user})
        ap_form.fields['user_id'].disabled = True
    
    context = {'ap_form': ap_form}
    return render(request, 'projekti/addupis.html', context)

   
            
    


