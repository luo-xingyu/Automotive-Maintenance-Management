from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20,unique=True)
    user_password = models.CharField(max_length=20)
    user_character = models.CharField(max_length=20,null=True) # personal or unit
    user_discount = models.FloatField(null=True)
    user_email = models.CharField(max_length=20,null=True)
    user_phone = models.CharField(max_length=20,null=True)

class Service_advisor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)

class Repair_man(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    job = models.CharField(max_length=20)

class Repair_manager(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10)
    license_plate = models.CharField(max_length=10) # 车牌号
    ident_number = models.CharField(max_length=18) # 车架号

class User_Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

# 维修委托书
class Repair_commission(models.Model):
    id = models.AutoField(primary_key=True)
    principal = models.ForeignKey(User, on_delete=models.CASCADE)
    service_man = models.ForeignKey(Service_advisor,on_delete=models.CASCADE)
    car = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    fault_info = models.CharField(max_length=100)
    wash = models.BooleanField(default=False)
    material_cost  = models.FloatField(default=0)
    labor_cost = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    expected_delivery_time = models.IntegerField(default=14)
    is_carried = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

# 维修派工单
class Repair_order(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=20)
    work_time = models.IntegerField(default=0)
    repair_man = models.ForeignKey(Repair_man, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    repair_commission = models.ForeignKey(Repair_commission, on_delete=models.CASCADE)
    # no = models.IntegerField(default=0) 1 2 3 4 5 ...

# 维修项目单
class Repair_cost(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=20)
    unit_laber_cost = models.FloatField()
    material_cost = models.FloatField()

