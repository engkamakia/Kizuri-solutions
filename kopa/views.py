#from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from .models import CustomUser



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser




from django.shortcuts import render, redirect,get_object_or_404
#from .forms import LoanForm




from decimal import Decimal, InvalidOperation
#import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from . models import *




import requests
from datetime import datetime

import json
import base64
from django.http import JsonResponse
from . utils import get_access_token, query_stk_status
from django.http import HttpResponseServerError
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError





from django.contrib.auth.decorators import login_required
from .decorators import login_required  # Import the decorator

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.backends import ModelBackend


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse



# Create your views here.
def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"] 
        
        # send email
        """
        send_mail(
            f"message from {email}, SUBJECT:" + subject, #subject
            message, #message
            email, #from email
            [settings.EMAIL_HOST_USER], #to email
        )
        """
        return render(request,'kopa/contacts.html',{"name":name})  
    
    else:
        return render(request,'kopa/contacts.html',{})
    
    
def index(request):   
    return render(request,'kopa/index.html')




def logoutUser(request):  
    logout(request)
    return redirect('home')




def success(request):
    return render(request,'kopa/success.html')






def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'kopa/registration.html')

        # Create user
        try:
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                id_number=id_number,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully!')
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'A user with this ID number or email already exists.')
            return redirect('registration')

    return render(request, 'kopa/registration.html')





def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        id_number = request.POST.get('id_number')
        
        
        user = authenticate(request, email=email, password=password, id_number=id_number)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL
        else:
            messages.error(request, 'Invalid email, Id or password')
    
    return render(request, 'kopa/login.html')




@login_required
def client_info_view(request):
    # Fetch all ClientInfo records
    profile = Profile.objects.all()
    
    # Render the template with the client data
    return render(request, 'kopa/dashboard.html', {'profile': profile})
    
    
   

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None
    
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.utils.dateparse import parse_date
#from .models import ClientInfo, Guarantor, Collateral

'''
@login_required
def guarantor_view(request):
    if request.method == 'POST':
        try:
            # Parse the guarantee date
            guarantee_date_str = request.POST.get('guarantee_date', '')
            guarantee_date = parse_date(guarantee_date_str)
            
            # Debugging statements to check form data and current user
            print("Received form data:", request.POST)
            print("Received files:", request.FILES)
            print("Current logged-in user:", request.user)
            
             # Get the ClientInfo associated with the logged-in user
            client_infos = ClientInfo.objects.filter(user=request.user)
            if client_infos.count() > 1:
                # Handle multiple ClientInfo objects, e.g., choose the first one
                client_info = client_infos.first()
                print("Multiple ClientInfo found. Using the first one.")
            elif client_infos.exists():
                client_info = client_infos.get()
            else:
                print("Client information not found for this user.")
                return HttpResponseServerError("Client information not found for this user.")
            # Save Guarantor information
            if Guarantor.objects.filter(client_info=client_info).exists():
                messages.error(request, "A Guarantor already exists for this client.")
                print("A Guarantor already exists for this client.")
                return render(request, 'kopa/guarantor.html')
            try:
                guarantor = Guarantor.objects.create(
                    client_info=client_info,
                    full_name=request.POST.get('full_name', ''),
                    nick_name=request.POST.get('nick_name', ''),
                    id_number=request.POST.get('id_number', ''),
                    phone1=request.POST.get('phone1', ''),
                    phone2=request.POST.get('phone2', ''),
                    email=request.POST.get('email', ''),
                    face_image=request.FILES.get('image'),
                    guarantee_name=request.POST.get('guarantee_name', ''),
                    loan_amount=request.POST.get('loan_amount', ''),
                    loan_amount_words=request.POST.get('loan_amount_words', ''),
                    guarantee_date=guarantee_date,
                    residence=request.POST.get('residence', ''),
                    id_photo=request.FILES.get('image'),
                )
                print("Guarantor saved successfully.")
            except Exception as e:
                print(f"Error creating Guarantor: {e}")
                return HttpResponseServerError("An error occurred while saving Guarantor information.")
            
            # Handle collateral items
            try:
                item_count = int(request.POST.get('item_count', 0))
                for i in range(1, item_count + 1):
                    item_name = request.POST.get(f'item-name-{i}', '')
                    item_description = request.POST.get(f'item-description-{i}', '')
                    photo1 = request.FILES.get(f'item-photo-{i}-1')
                    photo2 = request.FILES.get(f'item-photo-{i}-2')
                    photo3 = request.FILES.get(f'item-photo-{i}-3')
                    photo4 = request.FILES.get(f'item-photo-{i}-4')

                    Collateral.objects.create(
                        guarantor=guarantor,
                        item_name=item_name,
                        item_description=item_description,
                        photo1=photo1,
                        photo2=photo2,
                        photo3=photo3,
                        photo4=photo4,
                    )
                    print(f"Collateral item {i} saved successfully.")
                
                print("All collateral items saved successfully.")
            except Exception as e:
                print(f"Error creating Collateral items: {e}")
                return HttpResponseServerError("An error occurred while saving collateral items.")
            
            return HttpResponse("Form submitted successfully!")

        except Exception as e:
            print(f"An error occurred: {e}")
            return render(request, 'kopa/guarantor.html')
    
    return render(request, 'kopa/guarantor.html')



def safe_decimal(value, default='0'):
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(default)

def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default


#from django.contrib.auth import get_user_model   
@login_required
def client_submission_form(request):
    if request.method == 'POST':
        print(request.user.first_name)
        try:
            # Get the logged-in user
            user = CustomUser.objects.get(id=request.user.id)
            
            
            
           
            
            # Create ClientInfo
            client_info = ClientInfo.objects.create(
                user=user,
                
                nickname=request.POST.get('Nickname', ''),
                #national_id=request.POST.get('NationalId', ''),
                phone1=request.POST.get('phone1', ''),
                phone2=request.POST.get('phone2', ''),
                image = request.FILES.get('image'),
                #email=request.POST.get('email', ''),
                employment_status=request.POST.get('employment-status', ''),
                employer_name=request.POST.get('employer-name', ''),
                job_title=request.POST.get('job-title', ''),
                location_of_work=request.POST.get('location_of_work', ''),
                supervisors_name=request.POST.get('supervisors_name', ''),
                supervisors_contact=request.POST.get('supervisors_contact', ''),
                monthly_income=safe_decimal(request.POST.get('monthly_income', '')),
                monthly_expense=safe_decimal(request.POST.get('monthly_expense', '')),
                business_name=request.POST.get('business-name', ''),
                industry_type=request.POST.get('industry-type', ''),
                business_location=request.POST.get('business_location', ''),
                daily_income=safe_decimal(request.POST.get('daily_income', '')),
                daily_expense=safe_decimal(request.POST.get('daily_expense', '')),
                net_income=safe_decimal(request.POST.get('net_income', '')),
                loan_amount=safe_decimal(request.POST.get('loan_amount', '')),
                amount_in_words=request.POST.get('amount_in_words', ''),
                date_of_loan=request.POST.get('date_of_loan', ''),
                repay_principal=safe_decimal(request.POST.get('repay_principal', '')),
                interest=request.POST.get('interest', ''),
                total=safe_decimal(request.POST.get('total', '')),
                repay_date=request.POST.get('repay_date', '')
            )
            item_count = int(request.POST.get('item_count', 0))
            for i in range(1, item_count + 1):
                item_name = request.POST.get(f'item-name-{i}', '')
                item_description = request.POST.get(f'item-description-{i}', '')
                photo1 = request.FILES.get(f'item-photo-{i}-1')
                photo2 = request.FILES.get(f'item-photo-{i}-2')
                photo3 = request.FILES.get(f'item-photo-{i}-3')
                photo4 = request.FILES.get(f'item-photo-{i}-4')

                Client_Collateral.objects.create(
                    client=client_info,
                    item_name=item_name,
                    item_description=item_description,
                    photo1=photo1,
                    photo2=photo2,
                    photo3=photo3,
                    photo4=photo4,
                )
            
            print("client collateral items saved successfully")
           
            
            # Spouse Info
            SpouseInfo.objects.create(
                client=client_info,
                marital_status=request.POST.get('marital-status', ''),
                spouse_name=request.POST.get('spouse-name', ''),
                work_place=request.POST.get('work_place', ''),
                position=request.POST.get('position', ''),
                contact=request.POST.get('contact', ''),
                no_of_dependants=safe_int(request.POST.get('no_of_dependants', '')),                
                parent_type=request.POST.get('parent-type', ''),  
                father_full_name=request.POST.get('father-full-name', ''),
                father_contact=request.POST.get('father-contact', ''),
                mother_full_name=request.POST.get('mother-full-name', ''), 
                mother_contact=request.POST.get('mother-contact', ''),
                nextofkin=request.POST.get('nextofkin', ''),
            )

            # Residence Info
            ResidenceInfo.objects.create(
                client=client_info,
                residence_type = request.POST.get('residence_type', ''),
                residence_description = request.POST.get('residence_description', ''),
                rural_residence=request.POST.get('rural_residence', '')
            )

            # CRB Info
            CRBInfo.objects.create(
                client=client_info,
                image = request.FILES.get('image'),
                agree_to_terms = request.POST.get('agree_to_terms') == 'on'  # Checkbox returns 'on' if checked, otherwise None
            )
            #return HttpResponse("Form submitted successfully!")

            messages.success(request, "Client information submitted successfully.")
            return redirect('guarantor')  # Replace with your success URL

        except Exception as e:
            # Log the error and handle as necessary
            print(f"An error occurred: {e}")
            return HttpResponseServerError("An error occurred while processing the form.")
    
    return render(request, 'kopa/client.html')  # Replace with your template


@login_required
def client_profile(request, client_id):
    # Retrieve the client using the provided client_id
    client = get_object_or_404(ClientInfo, id=client_id)
    
    # Fetch the associated guarantors
    guarantors = client.guarantors.all()
    residence_info = client.residence_info

    # Pass the client and guarantors data to the template context
    context = {
        'client': client,
        'guarantors': guarantors,
        'residence_info': residence_info,
    }
    
    return render(request, 'kopa/profile.html', context)
    
    
    '''
    
    
@login_required
def guarantor_view(request, loan_id):
    context = {}
    if request.method == 'POST':
        try:
            # Parse the guarantee date
            guarantee_date_str = request.POST.get('guarantee_date', '')
            guarantee_date = parse_date(guarantee_date_str)
            
            # Get the Profiles associated with the logged-in user
            #print(f"Loan Info ID: {loan_id}")
            loan_info = get_object_or_404(LoanInfo, id=loan_id)
            context['loan_info'] = loan_info
            #loan_info = LoanInfo.objects.filter(user=request.user).latest('date_of_loan')
            
            # Save Guarantor information
            guarantor = Guarantor.objects.create(
                loan_info= loan_info,
                full_name=request.POST.get('full_name', ''),
                nick_name=request.POST.get('nick_name', ''),
                id_number=request.POST.get('id_number', ''),
                phone1=request.POST.get('phone1', ''),
                phone2=request.POST.get('phone2', ''),
                email=request.POST.get('email', ''),
                face_image=request.FILES.get('image'),
                guarantee_name=request.POST.get('guarantee_name', ''),
                loan_amount=request.POST.get('loan_amount', ''),
                loan_amount_words=request.POST.get('loan_amount_words', ''),
                guarantee_date=guarantee_date,
                residence=request.POST.get('residence', ''),
                id_photo=request.FILES.get('image'),
            )
            print("Guarantor saved successfully.")
            
            # Handle collateral items
            item_count = int(request.POST.get('item_count', 0))
            for i in range(1, item_count + 1):
                item_name = request.POST.get(f'item-name-{i}', '')
                item_description = request.POST.get(f'item-description-{i}', '')
                photo1 = request.FILES.get(f'item-photo-{i}-1')
                photo2 = request.FILES.get(f'item-photo-{i}-2')
                photo3 = request.FILES.get(f'item-photo-{i}-3')
                photo4 = request.FILES.get(f'item-photo-{i}-4')

                Collateral.objects.create(
                    guarantor=guarantor,
                    item_name=item_name,
                    item_description=item_description,
                    photo1=photo1,
                    photo2=photo2,
                    photo3=photo3,
                    photo4=photo4,
                )
                print(f"Collateral item {i} saved successfully.")
                
            print("All collateral items saved successfully.")
            messages.success(request, "guarantor information submitted successfully.")
            return redirect('home')

        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error("An error occurred while saving Guarantor information.")
            
    loan_info = get_object_or_404(LoanInfo, id=loan_id)
    context['loan_info'] = loan_info
    return render(request, 'kopa/guarantor.html', context)


def safe_decimal(value, default='0'):
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(default)

def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default


#from django.contrib.auth import get_user_model

def client_submission_form(request):
    user = CustomUser.objects.get(id=request.user.id)

    try:
        # Check if the user already has a profile
        existing_profile = Profile.objects.filter(user=user).first()
        
        if request.method == 'POST':
            # If there's an existing profile, update it instead of creating a new one
            if existing_profile:
                profile = existing_profile
            else:
                profile = Profile.objects.create(
                    user=user,
                    nickname=request.POST.get('Nickname', ''),
                    phone1=request.POST.get('phone1', ''),
                    phone2=request.POST.get('phone2', ''),
                    image=request.FILES.get('image'),
                    employment_status=request.POST.get('employment-status', ''),
                    employer_name=request.POST.get('employer-name', ''),
                    job_title=request.POST.get('job-title', ''),
                    location_of_work=request.POST.get('location_of_work', ''),
                    supervisors_name=request.POST.get('supervisors_name', ''),
                    supervisors_contact=request.POST.get('supervisors_contact', ''),
                    monthly_income=safe_decimal(request.POST.get('monthly_income', '')),
                    monthly_expense=safe_decimal(request.POST.get('monthly_expense', '')),
                    business_name=request.POST.get('business-name', ''),
                    industry_type=request.POST.get('industry-type', ''),
                    business_location=request.POST.get('business_location', ''),
                    daily_income=safe_decimal(request.POST.get('daily_income', '')),
                    daily_expense=safe_decimal(request.POST.get('daily_expense', '')),
                    net_income=safe_decimal(request.POST.get('net_income', '')),
                )
            
            loan_info = LoanInfo.objects.create(
                profile=profile,
                loan_amount=safe_decimal(request.POST.get('loan_amount', '')),
                amount_in_words=request.POST.get('amount_in_words', ''),
                date_of_loan=request.POST.get('date_of_loan', ''),
                repay_principal=safe_decimal(request.POST.get('repay_principal', '')),
                interest=request.POST.get('interest', ''),
                total=safe_decimal(request.POST.get('total', '')),
                repay_date=request.POST.get('repay_date', '')
            )
            
            item_count = int(request.POST.get('item_count', 0))
            for i in range(1, item_count + 1):
                item_name = request.POST.get(f'item-name-{i}', '')
                item_description = request.POST.get(f'item-description-{i}', '')
                photo1 = request.FILES.get(f'item-photo-{i}-1')
                photo2 = request.FILES.get(f'item-photo-{i}-2')
                photo3 = request.FILES.get(f'item-photo-{i}-3')
                photo4 = request.FILES.get(f'item-photo-{i}-4')

                Client_Collateral.objects.create(
                    loan_info=loan_info,
                    item_name=item_name,
                    item_description=item_description,
                    photo1=photo1,
                    photo2=photo2,
                    photo3=photo3,
                    photo4=photo4,
                )

            if existing_profile:
                SpouseInfo.objects.filter(profile=profile).update(
                    marital_status=request.POST.get('marital-status', existing_profile.spouse_info.marital_status),
                    spouse_name=request.POST.get('spouse-name', existing_profile.spouse_info.spouse_name),
                    work_place=request.POST.get('work_place', existing_profile.spouse_info.work_place),
                    position=request.POST.get('position', existing_profile.spouse_info.position),
                    contact=request.POST.get('contact', existing_profile.spouse_info.contact),
                    no_of_dependants=safe_int(request.POST.get('no_of_dependants', existing_profile.spouse_info.no_of_dependants)),
                    parent_type=request.POST.get('parent-type', existing_profile.spouse_info.parent_type),
                    father_full_name=request.POST.get('father-full-name', existing_profile.spouse_info.father_full_name),
                    father_contact=request.POST.get('father-contact', existing_profile.spouse_info.father_contact),
                    mother_full_name=request.POST.get('mother-full-name', existing_profile.spouse_info.mother_full_name),
                    mother_contact=request.POST.get('mother-contact', existing_profile.spouse_info.mother_contact),
                    nextofkin=request.POST.get('nextofkin', existing_profile.spouse_info.nextofkin),
                )
            else:
                SpouseInfo.objects.create(
                    profile=profile,
                    marital_status=request.POST.get('marital-status', ''),
                    spouse_name=request.POST.get('spouse-name', ''),
                    work_place=request.POST.get('work_place', ''),
                    position=request.POST.get('position', ''),
                    contact=request.POST.get('contact', ''),
                    no_of_dependants=safe_int(request.POST.get('no_of_dependants', '')),
                    parent_type=request.POST.get('parent-type', ''),
                    father_full_name=request.POST.get('father-full-name', ''),
                    father_contact=request.POST.get('father-contact', ''),
                    mother_full_name=request.POST.get('mother-full-name', ''),
                    mother_contact=request.POST.get('mother-contact', ''),
                    nextofkin=request.POST.get('nextofkin', ''),
                )
            
            if existing_profile:
                ResidenceInfo.objects.filter(profile=profile).update(
                    residence_type=request.POST.get('residence_type', existing_profile.residence_info.residence_type),
                    residence_description=request.POST.get('residence_description', existing_profile.residence_info.residence_description),
                    rural_residence=request.POST.get('rural_residence', existing_profile.residence_info.rural_residence),
                )
            else:
                ResidenceInfo.objects.create(
                    profile=profile,
                    residence_type=request.POST.get('residence_type', ''),
                    residence_description=request.POST.get('residence_description', ''),
                    rural_residence=request.POST.get('rural_residence', '')
                )

            CRBInfo.objects.create(
                loan_info=loan_info,
                image=request.FILES.get('image'),
                agree_to_terms=request.POST.get('agree_to_terms') == 'on'
            )

            messages.success(request, "Client information submitted successfully.")
            print(f"Redirecting to guarantor with loan_id: {loan_info.id}")
            if loan_info:
                return redirect('guarantor', loan_id=loan_info.id)
            else:
                messages.error(request, "Failed to create loan information.")
                return redirect('client_form')

        context = {
            'existing_profile': existing_profile
        }
        return render(request, 'kopa/client.html', context)

    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred while processing the form.")



'''   
@login_required
def client_submission_form(request):
    if request.method == 'POST':
        print(request.user.first_name)
        try:
            # Get the logged-in user
            user = CustomUser.objects.get(id=request.user.id)
            
            
            
           
            
            # Create ClientInfo
            profile= Profile.objects.create(
                user=user,
                
                nickname=request.POST.get('Nickname', ''),
                #national_id=request.POST.get('NationalId', ''),
                phone1=request.POST.get('phone1', ''),
                phone2=request.POST.get('phone2', ''),
                image = request.FILES.get('image'),
                #email=request.POST.get('email', ''),
                employment_status=request.POST.get('employment-status', ''),
                employer_name=request.POST.get('employer-name', ''),
                job_title=request.POST.get('job-title', ''),
                location_of_work=request.POST.get('location_of_work', ''),
                supervisors_name=request.POST.get('supervisors_name', ''),
                supervisors_contact=request.POST.get('supervisors_contact', ''),
                monthly_income=safe_decimal(request.POST.get('monthly_income', '')),
                monthly_expense=safe_decimal(request.POST.get('monthly_expense', '')),
                business_name=request.POST.get('business-name', ''),
                industry_type=request.POST.get('industry-type', ''),
                business_location=request.POST.get('business_location', ''),
                daily_income=safe_decimal(request.POST.get('daily_income', '')),
                daily_expense=safe_decimal(request.POST.get('daily_expense', '')),
                net_income=safe_decimal(request.POST.get('net_income', '')),
                #loan_amount=safe_decimal(request.POST.get('loan_amount', '')),
                #amount_in_words=request.POST.get('amount_in_words', ''),
                #date_of_loan=request.POST.get('date_of_loan', ''),
                ##repay_principal=safe_decimal(request.POST.get('repay_principal', '')),
                #interest=request.POST.get('interest', ''),
               #total=safe_decimal(request.POST.get('total', '')),
                #repay_date=request.POST.get('repay_date', '')
            )
            print("profile saved successfully")
            
            loan_info = LoanInfo.objects.create(
                profile=profile,
                loan_amount=safe_decimal(request.POST.get('loan_amount', '')),
                amount_in_words=request.POST.get('amount_in_words', ''),
                date_of_loan=request.POST.get('date_of_loan', ''),
                repay_principal=safe_decimal(request.POST.get('repay_principal', '')),
                interest=request.POST.get('interest', ''),
                total=safe_decimal(request.POST.get('total', '')),
                repay_date=request.POST.get('repay_date', '')
                )
            
            print("loan items saved successfully")
           
            item_count = int(request.POST.get('item_count', 0))
            for i in range(1, item_count + 1):
                item_name = request.POST.get(f'item-name-{i}', '')
                item_description = request.POST.get(f'item-description-{i}', '')
                photo1 = request.FILES.get(f'item-photo-{i}-1')
                photo2 = request.FILES.get(f'item-photo-{i}-2')
                photo3 = request.FILES.get(f'item-photo-{i}-3')
                photo4 = request.FILES.get(f'item-photo-{i}-4')

                Client_Collateral.objects.create(
                    loan_info=loan_info ,
                    item_name=item_name,
                    item_description=item_description,
                    photo1=photo1,
                    photo2=photo2,
                    photo3=photo3,
                    photo4=photo4,
                )
            
            print("client collateral items saved successfully")
           
            
            # Spouse Info
            SpouseInfo.objects.create(
                profile=profile,
                marital_status=request.POST.get('marital-status', ''),
                spouse_name=request.POST.get('spouse-name', ''),
                work_place=request.POST.get('work_place', ''),
                position=request.POST.get('position', ''),
                contact=request.POST.get('contact', ''),
                no_of_dependants=safe_int(request.POST.get('no_of_dependants', '')),                
                parent_type=request.POST.get('parent-type', ''),  
                father_full_name=request.POST.get('father-full-name', ''),
                father_contact=request.POST.get('father-contact', ''),
                mother_full_name=request.POST.get('mother-full-name', ''), 
                mother_contact=request.POST.get('mother-contact', ''),
                nextofkin=request.POST.get('nextofkin', ''),
            )
            print("spouse details saved successfully.")

            # Residence Info
            ResidenceInfo.objects.create(
                profile=profile,
                residence_type = request.POST.get('residence_type', ''),
                residence_description = request.POST.get('residence_description', ''),
                rural_residence=request.POST.get('rural_residence', '')
            )
            print("residency saved successfully.")

            # CRB Info
            CRBInfo.objects.create(
                loan_info=loan_info,
                image = request.FILES.get('image'),
                agree_to_terms = request.POST.get('agree_to_terms') == 'on'  # Checkbox returns 'on' if checked, otherwise None
            )
            print("crb info saved successfully.")

            messages.success(request, "Client information submitted successfully.")
            return redirect('guarantor')  # Replace with your success URL

        except Exception as e:
            # Log the error and handle as necessary
            print(f"An error occurred: {e}")
            return HttpResponseServerError("An error occurred while processing the form.")
    
    return render(request, 'kopa/client.html')  # Replace with your template
'''

@login_required
def client_profile(request, client_id):
    # Retrieve the client using the provided client_id
    profile = get_object_or_404(Profile, id=client_id)
    
    # Fetch the associated guarantors
    guarantors = profile.guarantors.all()
    residence_info = profile.residence_info

    # Pass the client and guarantors data to the template context
    context = {
        'profile': profile,
        'guarantors': guarantors,
        'residence_info': residence_info,
    }
    
    return render(request, 'kopa/profile.html', context)
    
    