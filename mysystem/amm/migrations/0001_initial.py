# Generated by Django 3.2 on 2024-05-05 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repair_commission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fault_info', models.CharField(max_length=100)),
                ('wash', models.BooleanField(default=False)),
                ('material_cost', models.FloatField(default=0)),
                ('labor_cost', models.FloatField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('expected_delivery_time', models.IntegerField(default=14)),
                ('is_carried', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Repair_cost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project', models.CharField(max_length=20)),
                ('unit_laber_cost', models.FloatField()),
                ('material_cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Repair_man',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('job', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Repair_manager',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Service_advisor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('user_password', models.CharField(max_length=20)),
                ('user_character', models.CharField(max_length=20, null=True)),
                ('user_discount', models.FloatField(null=True)),
                ('user_email', models.CharField(max_length=20, null=True)),
                ('user_phone', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=10)),
                ('license_plate', models.CharField(max_length=10)),
                ('ident_number', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='User_Vehicle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amm.user')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amm.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Repair_order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project', models.CharField(max_length=20)),
                ('work_time', models.IntegerField(default=0)),
                ('is_finished', models.BooleanField(default=False)),
                ('repair_commission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amm.repair_commission')),
                ('repair_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amm.repair_man')),
            ],
        ),
        migrations.AddField(
            model_name='repair_commission',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amm.vehicle'),
        ),
        migrations.AddField(
            model_name='repair_commission',
            name='principal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amm.user'),
        ),
        migrations.AddField(
            model_name='repair_commission',
            name='service_man',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amm.service_advisor'),
        ),
    ]
