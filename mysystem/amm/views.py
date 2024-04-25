from django.shortcuts import render
from django.http import HttpResponse
from . import models

def entry(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        action = request.POST.get('action')
        role = request.POST.get('role')
        
        if role =='user':
            if action == 'login':
                user = models.User.objects.filter(user_name=username).first()
                if user and user.user_password == password:
                    return render(request,'user.html') 
                else:
                    context = {}
                    if user:
                        context = {'password_error':'password_error'}
                    else:
                        context = {'user_not_exist':'user_not_exist'}
                    return render(request,'entry.html',context)
                
            elif action == 'register':
                user = models.User()
                user.user_name = username
                user.user_password = password
                user.save()
                context = {'success_register':'register successfully'}
                return render(request,'entry.html',context)  

    return render(request,'entry.html')