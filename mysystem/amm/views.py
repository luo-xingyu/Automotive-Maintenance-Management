from django.shortcuts import render,redirect
from . import models
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Prefetch

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
    user_list = models.User.objects.all()
    # entrust_list = models.Repair_commission.objects.all()
    
    entrust_list = models.Repair_commission.objects.prefetch_related(
        Prefetch('car', queryset=models.Vehicle.objects.all()),
        Prefetch('principal', queryset=models.User.objects.all())
    )
    
    entrust_data = []
    for entrust in entrust_list:
        entrust_info = {
            'id': entrust.id,
            'license_plate': entrust.car.license_plate if entrust.car else 'No Car Info',
            'principal_name': entrust.principal.user_name if entrust.principal else 'No Principal Info',
            'fault_info': entrust.fault_info,
            'material_cost': entrust.material_cost,
            'labor_cost': entrust.labor_cost
        }
        entrust_data.append(entrust_info)

    info_list =  {'user_list':user_list,'entrust_data':entrust_data}
    if request.method == 'POST':
        if request.POST.get('action') == 'add':
            user_id = request.POST.get('customer_id')
            car_id = request.POST.get('car_id')
            wash = request.POST.get('wash')
            error_info = request.POST.get('fault_description')
            print("we get here:",user_id,car_id,wash,error_info)
            commission = models.Repair_commission.objects.create(principal_id=user_id,
                                                                 service_man_id=service_id,
                                                                 car_id=car_id,
                                                                 fault_info=error_info,
                                                                 wash=wash)
            commission.save()
            return redirect('/service/entrust')

    return render(request,'service_man/entrust.html',info_list)


def get_cars(request):
    user_id = request.GET.get('customer_id')
    car = models.User_Vehicle.objects.filter(user_id=user_id)
    car_list = [{'id':item.vehicle_id,'license_plate':models.Vehicle.objects.filter(id=item.vehicle_id).first().license_plate} for item in car]
    return JsonResponse(car_list,safe=False)