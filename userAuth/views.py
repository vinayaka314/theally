from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import ReferralCode, CustomUser
import random, string




def home(request):
    return render(request, "auth\index.html") 

def dashboard(request):
    users = CustomUser.objects.all()
    referral_codes = ReferralCode.objects.all()


    context = {
        'users': users,
        'referral_codes': referral_codes,
    }
    return render(request, 'auth\dashboard.html', context)



def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        my_ref_code = generate_referral_code()
        referral_code = request.POST.get('referral_code')
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'auth\signup.html', {'error': 'Email already exists'})
        
        # Create user
        user = CustomUser.objects.create_user(email=email, password=password, name=name, referral_code=referral_code, my_ref_code = my_ref_code)
        
        # Check if referral code is provided and exists in the database
        if referral_code:
            try:
                referred_by = CustomUser.objects.get(referral_code=referral_code)
                print(".............................",referred_by)
                
            except CustomUser.DoesNotExist:
                pass
        
        # redirect to home page
        return redirect('signin')
    
    return render(request, "auth\signup.html")

def generate_referral_code():
    letters = string.ascii_uppercase
    digits = string.digits
    code = ''.join(random.choice(letters + digits) for i in range(5))
    return code

def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            # return render(request, 'auth\dashboard.html')
        else:
            return render(request, 'auth\signin.html', {'error': 'Invalid email or password'})
    
    return render(request, "auth\signin.html")


# def authenticate_user(email, password):
#     try:
#         user = CustomUser.objects.get(email=email)
#         if user.check_password(password):
#             return user
#     except CustomUser.DoesNotExist:
#         return None
#     except:
#         return None
#     return None



def signout(request):
    logout(request)
    return redirect('home')