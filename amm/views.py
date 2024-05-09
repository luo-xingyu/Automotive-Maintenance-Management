from django.shortcuts import render,redirect
from . import models
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Prefetch
from django.core import serializers
from django.middleware.csrf import get_token
import json

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
        
        if role == 'service_man':
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
    
        elif role == 'repair_manager':
            man = models.Repair_manager.objects.filter(name=username).first()
            if man and man.password == password:
                request.session['username'] = username
                return redirect('/repair_manage/')
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
            context = {'user_type':'repair_man'}
            return render(request,'register.html',context)
        if user_type == 'repair_manager': 
            context = {'user_type':'repair_manager'}
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
            worktype = request.POST.get('type')
            repair_man = models.Repair_man.objects.create(name=username,
                                                          password=password,job=worktype)
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


# =============================================================================
# Module: repair_manager
# =============================================================================

def manageIndex(request):
    username = request.session.get('username')
    if request.method == 'POST':
        if request.POST.get('action') == 'changename':
            newname = request.POST.get('name')
            models.Repair_manager.objects.filter(name=username).update(name=newname)
            request.session['username'] = newname
            return redirect('/repair_manage/')
        if request.POST.get('action') == 'changepassword':
            nowpassword = request.POST.get('currentPassword')
            newpassword = request.POST.get('newPassword')
            confirmpwd = request.POST.get('confirmPassword')
            context = {}
            storepwd = models.Repair_manager.objects.filter(name=username).first().password
            if storepwd != nowpassword:
                context = {'password_error':'password_error','username':username}
                return render(request,'repair_manager/index.html',context)
            if newpassword != confirmpwd:
                context = {'confirm_error':'confirm_error','username':username}
                return render(request,'repair_manager/index.html',context)
            
            models.Repair_manager.objects.filter(name=username).update(password=newpassword)
            return redirect('/logout/')
        
    return render(request,'repair_manager/index.html',{'username':username})

def manageTask(request):
    entrust_list = models.Repair_commission.objects.prefetch_related(
        Prefetch('car', queryset=models.Vehicle.objects.all()),
        Prefetch('principal', queryset=models.User.objects.all())
        ).filter(is_carried=False).all()
    
    entrust_data = []
    for entrust in entrust_list:
        entrust_info = {
            'id': entrust.id,
            'principal_name': entrust.principal.user_name if entrust.principal else 'No Principal Info',
            'license_plate': entrust.car.license_plate if entrust.car else 'No Car Info',
            'car_type': entrust.car.type if entrust.car else 'No Car Info',
            'fault_info': entrust.fault_info,
            'wash': entrust.wash,
        }
        entrust_data.append(entrust_info)
    
    entrust_list2 = models.Repair_commission.objects.prefetch_related(
        Prefetch('car', queryset=models.Vehicle.objects.all()),
        Prefetch('principal', queryset=models.User.objects.all())
        ).filter(is_finished=False,is_carried=True).all()
    
    entrust_cost = []
    for entrust in entrust_list2:
        entrust_info = {
            'id': entrust.id,
            'principal_name': entrust.principal.user_name if entrust.principal else 'No Principal Info',
            'license_plate': entrust.car.license_plate if entrust.car else 'No Car Info',
            'car_type': entrust.car.type if entrust.car else 'No Car Info',
            'fault_info': entrust.fault_info,
            'wash': entrust.wash,
        }
        entrust_cost.append(entrust_info)

    repair_project = models.Repair_cost.objects.all()
    repair_man = models.Repair_man.objects.all()
    repair_project_json = serializers.serialize('json', repair_project)
    repair_man_json = serializers.serialize('json', repair_man)

    data = {
        'entrust_data': entrust_data, # 待分配的任务
        'entrust_cost': entrust_cost, # 没有结算费用的任务 在work.html中补充结算费用的地方
        'repair_project': repair_project_json,
        'repair_man':repair_man_json
    }

    if request.method == 'POST':
        commission_id = request.POST.get('commission_id')
        projects = request.POST.getlist('projects[]')
        times = request.POST.getlist('times[]')
        men = request.POST.getlist('men[]')
        print(commission_id,projects,times,men)
        for project_id,time,man_id in zip(projects,times,men):
            man = models.Repair_man.objects.filter(id=man_id).first()
            projectname = models.Repair_cost.objects.filter(id=project_id).first().project
            commission = models.Repair_commission.objects.filter(id=commission_id).first()
            order = models.Repair_order.objects.create(project=projectname,
                                                        work_time=time,
                                                        repair_man=man,
                                                        repair_commission=commission)
            order.save()
        models.Repair_commission.objects.filter(id=commission_id).update(is_carried=True) # 待测试
   
        return redirect('/repair_manage/work')

    return render(request,'repair_manager/work.html',data)

# wechat applet
def user_login(request):
    if request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')
        role = request.GET.get('role')
        if role == "user":
            user = models.User.objects.filter(user_name=username,user_password=password).first()
            if user:
                return JsonResponse({'status': 'success', 'message': '登录成功'})
            else:
                return JsonResponse({'status': 'fail', 'message': '用户名或密码错误'})
            
        elif role == "repairman":
            repairpeople = models.Repair_man.objects.filter(name=username,password=password).first()
            if repairpeople:
                return JsonResponse({'status': 'success', 'message': '登录成功'})
            else:
                return JsonResponse({'status': 'fail', 'message': '用户名或密码错误'})
       