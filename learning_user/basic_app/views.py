from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


from django.contrib.auth import authenticate,login,logout
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in!")

@login_required
def user_logout(request):
    logout(request)    #auto by django
    return HttpResponseRedirect(reverse('index'))

def register(request):

        registered=False

        if request.method=="POST":
            user_form=UserForm(data=request.POST)
            profile_form=UserProfileInfoForm(data=request.POST)

            if user_form.is_valid() and profile_form.is_valid():
                user=user_form.save()
                user.set_password(user.password)    #hashing
                user.save()

                profile=profile_form.save(commit=False)   #Don't want to commmit to the database yet otherwise i may get errors with collision where try to override this user
                profile.user=user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic=request.FILES['profile_pic']

                profile.save()
                registered=True
            else:
                print(user_form.errors,profile_form.errors)
        else:
            user_form=UserForm()
            profile_form=UserProfileInfoForm()

        return render(request,'basic_app/registration.html',
                                                            {'user_form':user_form,
                                                            'profile_form':profile_form,
                                                            'registered':registered})


def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)   #django automatically authenticate

        if user:
            if user.is_active:
                login(request,user)   #automattically by django
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Either username or password is invalid!")
            print("Username {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'basic_app/login.html',{})
