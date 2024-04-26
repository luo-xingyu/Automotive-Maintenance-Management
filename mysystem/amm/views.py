from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import models
from django.urls import reverse

def home(request):
    return render(request,'home.html')

# =============================================================================
# Module: login
# =============================================================================

def entry(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if role =='user':
            user = models.User.objects.filter(user_name=username).first()
            if user and user.user_password == password:
                return render(request,'user.html') # 
            else:
                context = {}
                if user:
                    context = {'password_error':'password_error'}
                else:
                    context = {'user_not_exist':'user_not_exist'}
                return render(request,'entry.html',context)
            
    return render(request,'entry.html')

# =============================================================================
# Module: register
# =============================================================================

def register(request):
    if request.method == 'GET':
        user_type = request.GET.get('role')

        if user_type == 'user':
            context = {'user_type':'user'}
            return render(request,'register.html',context)
        if user_type == 'service_man': 
            context = {'user_type':'service_man'}
            return render(request,'register.html',context)
        if user_type == 'repair_man':  
            context = {'user_type':'service_man'}
            return render(request,'register.html',context)
        if user_type == 'repair_manager': 
            context = {'user_type':'service_man'}
            return render(request,'register.html',context)
        
    elif request.method == 'POST':
        user_type = request.POST.get('usertype')
        if user_type == 'user':
            username = request.POST.get('username')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            character = request.POST.get('character')
            user = models.User.objects.create(user_name=username,user_password=password,
                                              user_character=character,user_discount=1,
                                              user_phone=phone)
            user.save()
            
        elif user_type == 'service_man':
            username = request.POST.get('username')
            password = request.POST.get('password')
            service_man = models.Service_advisor.objects.create(name=username,
                                                                password=password)
            service_man.save()
            
        elif user_type == 'repair_man':
            username = request.POST.get('username')
            password = request.POST.get('password')
            repair_man = models.Repair_man.objects.create(name=username,
                                                          password=password,job='null')
            repair_man.save()

        elif user_type == 'repair_manager':
            username = request.POST.get('username')
            password = request.POST.get('password')
            repair_manager = models.Repair_manager.objects.create(name=username,
                                                                  password=password)
            repair_manager.save()

        return redirect('/entry/')
    
    return render(request,'register.html')

# =============================================================================
# Module: user
# =============================================================================

