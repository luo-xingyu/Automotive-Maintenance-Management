from django.shortcuts import render,redirect
from . import models
from django.contrib.auth import logout

def home(request):
    return render(request,'home.html')

def userlogout(request):
    logout(request)
    return redirect('/entry/')

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
                return redirect('/user/')
            else:
                context = {}
                if user:
                    context = {'password_error':'password_error'}
                else:
                    context = {'user_not_exist':'user_not_exist'}
                return render(request,'entry.html',context)
        
        elif role == 'service_man':
            man = models.Service_advisor.objects.filter(name=username).first()
            if man and man.password == password:
                request.session['username'] = username
                return redirect('/service/')
            else:
                context = {}
                if man:
                    context = {'password_error':'password_error'}
                else:
                    context = {'user_not_exist':'user_not_exist'}
                return render(request,'entry.html',context)
        elif role == 'repair_man':
            man = models.Repair_man.objects.filter(name=username).first()
            if man and man.password == password:
                return redirect('/repair/')
            else:
                context = {}
                if man:
                    context = {'password_error':'password_error'}
                else:
                    context = {'user_not_exist':'user_not_exist'}
                return render(request,'entry.html',context)
        elif role == 'repair_manager':
            man = models.Repair_manager.objects.filter(name=username).first()
            if man and man.password == password:
                return redirect('/repairmanage/')
            else:
                context = {}
                if man:
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

def user(request):
    return render(request,'user/index.html')

# =============================================================================
# Module: service_man
# =============================================================================

def service(request):
    username = request.session.get('username')
    if request.method == 'POST':
        if request.POST.get('action') == 'changename':
            newname = request.POST.get('name')
            models.Service_advisor.objects.filter(name=username).update(name=newname)
            request.session['username'] = newname
            return redirect('/service/')
        if request.POST.get('action') == 'changepassword':
            nowpassword = request.POST.get('currentPassword')
            newpassword = request.POST.get('newPassword')
            confirmpwd = request.POST.get('confirmPassword')
            context = {}
            storepwd = models.Service_advisor.objects.filter(name=username).first().password
            if storepwd != nowpassword:
                context = {'password_error':'password_error','username':username}
                return render(request,'service_man/index.html',context)
            if newpassword != confirmpwd:
                context = {'confirm_error':'confirm_error','username':username}
                return render(request,'service_man/index.html',context)
            
            models.Service_advisor.objects.filter(name=username).update(password=newpassword)
            return redirect('/logout/')
        
    return render(request,'service_man/index.html',{'username':username})

def showProject(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'add':
            projectname = request.POST.get('project')
            person_cost = request.POST.get('unit_laber_cost')
            material_cost = request.POST.get('material_cost')
            item = models.Repair_cost.objects.create(project=projectname,
                                                        unit_laber_cost=person_cost,
                                                        material_cost=material_cost)
            item.save()

        if request.POST.get('action') == 'delete':
            projectid = request.POST.get('id')
            models.Repair_cost.objects.filter(id=projectid).delete()

        if request.POST.get('action') == 'update':
            projectid = request.POST.get('id')
            person_cost = request.POST.get('unit_laber_cost')
            material_cost = request.POST.get('material_cost')
            models.Repair_cost.objects.filter(id=projectid).update(unit_laber_cost=person_cost,
                                                                          material_cost=material_cost)
        return redirect('/service/project')
    
    repair_project = models.Repair_cost.objects.all()
    return render(request,'service_man/project.html',{'repair_project':repair_project})

def entrust(request):
    service_name = request.session.get('username')
    service_id = models.Service_advisor.objects.filter(name=service_name).first().id
    
    entrust_list = models.Repair_commission.objects.all()
    return render(request,'service_man/entrust.html',{'entrust_list':entrust_list})