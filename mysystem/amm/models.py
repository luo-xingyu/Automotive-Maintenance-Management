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
    name = models.CharField(max_length=20)
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
    license_plate = models.CharField(max_length=10)
    ident_number = models.CharField(max_length=18)

class User_Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

class Repair_commission(models.Model):
    id = models.AutoField(primary_key=True)
    principal = models.ForeignKey(User, on_delete=models.CASCADE)
    service_man = models.ForeignKey(Service_advisor,on_delete=models.CASCADE)
    car = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    wash = models.BooleanField() # car wash need extra cost
    material_cost  = models.FloatField()
    labor_cost = models.FloatField()
    time = models.DateTimeField() # created time
    expected_delivery_time = models.DateTimeField()

class Repair_order(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=20)
    work_time = models.DateTimeField()
    repair_man_id = models.ForeignKey(Repair_man, on_delete=models.CASCADE)

class Repair_cost(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=20)
    unit_laber_cost = models.FloatField()
    material_cost = models.FloatField()

