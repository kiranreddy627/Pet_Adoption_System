from django.shortcuts import render,redirect
from django.http import Http404
from django.utils import timezone
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators  import login_required


def home(request):
    return render(request, 'home.html')

def pets(request):
    pets = Pet.objects.all()
    search_term = request.GET.get('search_pet')
    if search_term:
        pets=pets.filter(
            Q(name__icontains=search_term) | 
            Q(species__icontains=search_term) | 
            Q(breed__icontains=search_term)
        )
    return render(request, 'pets.html', {
        'pets': pets,
    })

@login_required(login_url="/login/")
def add_pet(request):
    if request.method == "POST":
        data=request.POST
        name=data.get('name')
        submitter=data.get('submitter')
        species=data.get('species')
        breed=data.get('breed')
        description=data.get('description')
        sex=data.get('sex')
        submission_date=timezone.now()
        age=int(data.get('age'))
        pet_image=request.FILES.get("pet_image")
        Pet.objects.create(
            name=name, 
            submitter=submitter,  
            species=species, 
            breed=breed,
            description=description,
            submission_date=submission_date,
            pet_image=pet_image,
            sex=sex,
            age=age,
            )

    return render(request, 'add_pet.html')

def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        raise Http404('pet not found')
    return render(request, 'pet_detail.html', {
        'pet': pet,
    })

@login_required(login_url="/login/")
def delete_pet(request,id):
    queryset = Pet.objects.get(id=id)
    queryset.delete()
    return redirect('/all_pets/')

@login_required(login_url="/login/")
def update_pet(request,id):
    queryset = Pet.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        name=data.get('name')
        submitter=data.get('submitter')
        species=data.get('species')
        breed=data.get('breed')
        description=data.get('description')
        sex=data.get('sex')
        age=int(data.get('age'))
        pet_image=request.FILES.get("pet_image")

        queryset.name=name
        queryset.submitter=submitter
        queryset.species=species
        queryset.breed=breed
        queryset.description=description
        queryset.sex=sex
        queryset.age=age
        if pet_image:
            queryset.pet_image=pet_image
        queryset.save()
        return redirect('/all_pets/')
        
    context={'pet':queryset}
    return render(request, 'update_pet.html',context)


def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid Username!")
            return redirect('/login/')
        user = authenticate(username=username,password=password)
        if not user:
            messages.error(request,"Invalid Password!")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')

    return render(request,"login.html")

def logout_page(request):
    logout(request)
    return redirect('/login/')
    
def register_page(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.error(request,'Username already exists! Please try another one.')
            return redirect('/register/')
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password) #hashing the password
        user.save()
        messages.info(request,"Account created successfully!")
        return redirect('/login/')
    
    return render(request,"register.html")
