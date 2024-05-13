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
            'repair_type': entrust.repair_type,
            'material_cost': entrust.material_cost,
            'labor_cost': entrust.labor_cost,
            'is_carried': entrust.is_carried,
            'is_finished': entrust.is_finished,
        }
        entrust_data.append(entrust_info)

    entrust_data.sort(key=lambda x: x['repair_type'] != 'urgent')
    info_list =  {'user_list':user_list,'entrust_data':entrust_data}

    if request.method == 'POST':
        if request.POST.get('action') == 'add':
            user_id = request.POST.get('customer_id')
            car_id = request.POST.get('car_id')
            wash = request.POST.get('wash')
            error_info = request.POST.get('fault_description')
            repair_type = request.POST.get('repair_type')
            work_type = request.POST.get('work_type')
            settle_type = request.POST.get('settle_type')
            commission = models.Repair_commission.objects.create(principal_id=user_id,
                                                                 service_man_id=service_id,
                                                                 car_id=car_id,
                                                                 fault_info=error_info,
                                                                 repair_type=repair_type,
                                                                 work_type=work_type,
                                                                 settle_type=settle_type,
                                                                 wash=wash)
            commission.save()
            return redirect('/service/entrust')

    return render(request,'service_man/entrust.html',info_list)


def entrust_delete(request):
    entrust_id = request.GET.get('id')
    models.Repair_commission.objects.filter(id=entrust_id).delete()
    return redirect('/service/entrust')


def entrust_details(request):
    entrust_id = request.GET.get('id')
    entrust = models.Repair_commission.objects.filter(id=entrust_id).first()
    print(entrust_id,entrust)
    entrust_info = {
        'id': entrust.id,
        'car_license_plate': entrust.car.license_plate,
        'principal_name': entrust.principal.user_name,
        'fault_info': entrust.fault_info,
        'material_cost': entrust.material_cost,
        'labor_cost': entrust.labor_cost,
        'repair_type': entrust.repair_type,
        'work_type': entrust.work_type,
        'settle_type': entrust.settle_type,
        'is_carried': entrust.is_carried,
        'is_finished': entrust.is_finished,
        'is_paid': entrust.is_paid
    }
    return render(request,'service_man/details.html',entrust_info)

def get_cars(request):
    user_id = request.GET.get('customer_id')
    car = models.User_Vehicle.objects.filter(user_id=user_id)
    car_list = [{'id':item.vehicle_id,'license_plate':models.Vehicle.objects.filter(id=item.vehicle_id).first().license_plate} for item in car]
    return JsonResponse(car_list,safe=False)


# =============================================================================
# Module: repair_manager
# =============================================================================

# 对于一个委托单，如果里面所有的工作都已经完成，显示在结算费用的页面，点击右侧结算费用按钮，显示当前的
# 人工费用，物料费用，这两个费用可以修改，确认后，自动计算总费用，修改委托单信息。费用计算完毕。
# 折扣在用户支付时计算。

def check_cost(request):
    commission_all = models.Repair_commission.objects.filter(is_finished=True,is_paid=False,total_cost=0).all()
    commission_list = []
    for commission in commission_all:
        # 人工费用计算
        labor_cost = 0
        orders = models.Repair_order.objects.filter(repair_commission=commission).all()
        for order in orders:
            labor_cost += order.work_time * models.Repair_cost.objects.filter(project=order.project).first().unit_laber_cost
        models.Repair_commission.objects.filter(id=commission.id).update(labor_cost=labor_cost)
        # 物料费用计算
        material_cost = 0
        for order in orders:
            material_cost += models.Repair_cost.objects.filter(project=order.project).first().material_cost
        models.Repair_commission.objects.filter(id=commission.id).update(material_cost=material_cost)
        # 信息发送前端进行检查
        car_license = models.Vehicle.objects.filter(id=commission.car.id).first().license_plate
        info = {
            'id':commission.id,
            'car_license_plate':car_license,
            'fault_info':commission.fault_info,
            'material_cost':commission.material_cost,
            'labor_cost':commission.labor_cost,
            'total_cost':commission.total_cost
        }
        commission_list.append(info)

    if request.method == 'POST':
        commission_id = request.POST.get('commission_id')
        material_cost = request.POST.get('material_cost')
        labor_cost = request.POST.get('labor_cost')
        total_cost = request.POST.get('total_cost')
        models.Repair_commission.objects.filter(id=commission_id).update(material_cost=material_cost,
                                                                          labor_cost=labor_cost,
                                                                          total_cost=total_cost)
        return redirect('/repair_manage/check_cost')
    
    return render(request,'repair_manager/check_cost.html',{'commission_list':commission_list})


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
            
        elif role == "repair_man":
            repairpeople = models.Repair_man.objects.filter(name=username,password=password).first()
            if repairpeople:
                return JsonResponse({'status': 'success', 'message': '登录成功'})
            else:
                return JsonResponse({'status': 'fail', 'message': '用户名或密码错误'})


def user_managecar(request):
    if request.method == "GET":
        action = request.GET.get('action')
        username = request.GET.get('username')
        if action == "inquire":
            user = models.User.objects.filter(user_name=username).first()
            user_vehicle = models.User_Vehicle.objects.filter(user=user).all()
            car_list = [{   'type': vehicle.vehicle.type,
                            'license_plate': vehicle.vehicle.license_plate,
                            'ident_number': vehicle.vehicle.ident_number
                        } for vehicle in user_vehicle ]
                        
            return JsonResponse(car_list,safe=False)
        elif action == "add":
            type = request.GET.get('type')
            license_plate = request.GET.get('license_plate')
            ident_number = request.GET.get('ident_number')
            vehicle = models.Vehicle.objects.create(type=type,license_plate=license_plate,ident_number=ident_number)
            vehicle.save()
            user = models.User.objects.filter(user_name=username).first()
            user_vehicle = models.User_Vehicle.objects.create(user=user,vehicle=vehicle)
            user_vehicle.save() 
            return JsonResponse({'status': 'success', 'message': '添加成功'})
        
        elif action == "delete":
            ident_number = request.GET.get('ident_number')
            vehicle = models.Vehicle.objects.filter(ident_number=ident_number).first()
            vehicle.delete()
            return JsonResponse({'status': 'success', 'message': '删除成功'})
        

# details of commission
def commission(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(user_name=username).first()
    entrust = models.Repair_commission.objects.filter(principal=user,is_paid=False).all()
    entrust_list = []
    for item in entrust:
        car_license = models.Vehicle.objects.filter(id=item.car.id).first().license_plate
        info = {
            'id':item.id,
            'car_license_plate':car_license,
            'fault_info':item.fault_info,
            'material_cost': item.material_cost,
            'labor_cost':item.labor_cost,
            'create_time':item.time,
            'expected_delivery_time':item.expected_delivery_time,
            'is_carried':item.is_carried,
            'is_finshed':item.is_finished,
        }
        entrust_list.append(info)
    return JsonResponse(entrust_list,safe=False)

# inquire progress
def progressquery(request):
    entrust_id = request.GET.get('entrust_id')
    entrust_list = models.Repair_commission.objects.filter(id=entrust_id).all()
    order_progress = []
    for item in entrust_list:
        orders = models.Repair_order.objects.filter(repair_commission=item).all()
        for order in orders:
            order_info = {
                'project': order.project,
                'progress':order.is_finished,
            }
            order_progress.append(order_info)

    return JsonResponse(order_progress,safe=False)


def get_commissionhistory(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(user_name=username).first()
    entrust_list = models.Repair_commission.objects.filter(principal=user).all()
    entrust_data = []
    for item in entrust_list:
        entrust_info = {
            'id': item.id,
            'fault_info': item.fault_info,
            'material_cost': item.material_cost,
            'labor_cost': item.labor_cost,
            'time': item.time,
            'expected_delivery_time': item.expected_delivery_time,
            'is_carried': item.is_carried,
            'is_finished': item.is_finished,
            'is_paid': item.is_paid
        }
        entrust_data.append(entrust_info)
    return JsonResponse(entrust_data,safe=False)
    

def pay(requset):
    commission_id = requset.GET.get('commission_id')
    models.Repair_commission.objects.filter(id=commission_id).update(is_paid=True)
    return JsonResponse({'status': 'success', 'message': '支付成功'})

# repair_man
def get_order(request):
    username = request.GET.get('username')
    repair_man = models.Repair_man.objects.filter(name=username).first()
    task = models.Repair_order.objects.filter(repair_man=repair_man).all()
    task_list = []
    for item in task:
        if item.is_finished:
            continue
        task_info = {
            'id': item.id,
            'project': item.project,
            'work_time': item.work_time,
            'is_finished': item.is_finished
        }
        task_list.append(task_info)
    return JsonResponse(task_list,safe=False)


def repair_finsh(request):
    id = request.GET.get('id')
    repair_order = models.Repair_order.objects.filter(id=id).first()
    repair_order.is_finished=True
    repair_order.save()
    commission = models.Repair_commission.objects.filter(id=repair_order.repair_commission.id).first()
    orders = models.Repair_order.objects.filter(repair_commission=commission)    
    all_finish = True
    for item in orders:
        if item.is_finished == False:
            all_finish=False
            break
    if all_finish:
        commission.is_finished=True
        commission.save()

    return JsonResponse({'status': 'success', 'message': '维修完成'})
