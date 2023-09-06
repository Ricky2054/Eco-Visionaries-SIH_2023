from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages

from accounts.models import User
from accounts.utils import current_time, check_str_special, validate_email


# Create your views here.

#signup page
def signup(request):
    phone = first_name = last_name = password = ""
    context = {}
    try:

        #check if user is authenticated
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('aqi')
        else:
            try:
                if request.method == "POST":
                    phone = request.POST.get("phone")
                    first_name = request.POST.get("firstName")
                    last_name = request.POST.get("lastName")
                    password = request.POST.get("password")

                    #check if phone number is valid
                    if phone.isdigit() and len(phone)==10:

                        #check if first_name and last_name are valid
                        if first_name != "" and not check_str_special(first_name) and last_name != "" and not check_str_special(last_name):

                            #check if user with same phone number is registered
                            if User.objects.filter(phone = phone).first() is not None:
                                messages.error(request, "An account already exists with this phone number")
                            else:
                                #create user obj if everything is fine
                                new_user = User.objects.create_user(phone=phone, password=password)
                                new_user.first_name = first_name
                                new_user.last_name = last_name
                                new_user.save()

                                phone = first_name = password = ""

                                # login the user
                                auth.login(request, new_user)

                                messages.success(request, "you are registered successfully")

                                #redirect user to aqi page
                                return redirect('aqi')

                        else:
                            messages.error(request, "special characters not allowed in name")

                    else:
                        messages.error(request, "invalid phone number")

            except Exception as e:
                print(e)
                pass
        
        
    except Exception as e:
        print(e)
        pass

        
    context["phone"] = phone
    context["first_name"] = first_name
    context["last_name"] = last_name
    context["password"] = password

    return render(request, 'accounts/signup.html', context)


#login view
def login(request):
    phone  = password = ""
    context = {}
    try:

        #check if user is authenticated
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('aqi')
        else:
            try:
                if request.method == "POST":
                    phone = request.POST.get("phone")
                    password = request.POST.get("password")
                    #check if phone number is valid
                    if phone.isdigit() and len(phone)==10:

                        #check if user exists with given phone number
                        if User.objects.filter(phone = phone).first() is None:
                            messages.error(request, "no account exists with this phone number")
                        else:
                            #authenticate the user
                            auth_user = auth.authenticate(phone = phone, password = password)
                            if auth_user is not None:
                                #login the user
                                auth.login(request, auth_user)
                                
                                phone = password = ""

                                #if next in url then return to that page
                                if request.GET.get('next') != None:
                                    return redirect(request.GET.get('next'))

                                messages.success(request, "you are logged in now")

                                #redirect user to aqi page
                                return redirect('aqi')
                            else:
                                messages.error(request, "invalid credentials")
                       
                    else:
                        messages.error(request, "invalid phone number")

            except Exception as e:
                print(e)
                pass
        
    
    except Exception as e:
        print(e)
        pass

    context["phone"] = phone
    context["password"] = password

    return render(request, 'accounts/login.html', context)



#logout view
@login_required(login_url="/auth/login")
def logout(request):
    try:
        #check if any session is set for current phone
        if request.session.get('phone'):
            #delete the session if present
            del request.session['phone']
        
        #set last login time for user
        request.user.last_logout = current_time
        request.user.save()
        auth.logout(request)  
    except Exception as e:
        print(e)
        pass

    messages.warning(request, "You are logged out now")  
    return redirect('login')



