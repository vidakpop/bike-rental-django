from django.shortcuts import redirect,render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django .conf import settings
from userauths.models import User


#User=settings.AUTH_USER_MODEL

def register_view(request):

    if request.method == "POST":
      
      form=UserRegisterForm(request.POST or None)
      if form.is_valid():
         new_user=form.save()
         username=form.cleaned_data.get("username")
         messages.success(request,f"Hey{username},Account created successfully")
         #new_user=authenticate(username=form.cleaned_data['email'],password=form.cleaned_data['password1'])
         #login(request,new_user)
         return redirect("core:index")
      
    else:
        
        form=UserRegisterForm()
        
    context={
        'form':form,
    }
    return render(request,"userauths/signup.html",context)

def login_view(request):
   if request.user.is_authenticated:
      messages.warning(request,f"Hey you are already logged in")
      return redirect("core:index")
   if request.method=="POST":
      email=request.POST.get("email")
      password=request.POST.get("password")

      try:
         user=User.object.get(email=email)
         
      except:
         messages.warning(request,f"User with (email) does not exist")

         user=authenticate(request,email=email,password=password)
         if user is not None:
          login(request,user)
          messages.success(request,'You are logged in.')
          return redirect("core:index")
         else:
           messages.warning(request,"User does not exist.Create an account")
      
      
   context={
       
    }
       
    
   return render(request,'userauths/login.html',context)

def logout_view(request):
   logout(request)
   messages.success(request,'You are logged out.')
   return redirect("userauths:login")

