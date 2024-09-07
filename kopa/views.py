from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from datetime import datetime
import requests
import json
import base64
import logging

from .models import CustomUser, LoanInfo, Guarantor, Collateral, Profile, SpouseInfo, ResidenceInfo, CRBInfo, Client_Collateral
from .utils import get_access_token, query_stk_status
from .decorators import login_required 
from django.core.mail import send_mail
from django.conf import settings


# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.
def contact(request):
    
        return render(request, 'kopa/contact.html', {})
   
    
def index(request):   
    return render(request,'kopa/index.html')




def logoutUser(request):  
    logout(request)
    return redirect('home')




def success(request):
    return render(request,'kopa/success.html')






def sign_up(request):
    if request.method == 'POST':
        try:
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
        except Exception as e:
            logger.error(f"Error in sign_up view: {e}")
            messages.error(request, 'An error occurred during sign-up. Please try again.')
            return redirect('registration')
    return render(request, 'kopa/registration.html')





def sign_in(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            id_number = request.POST.get('id_number')
            
            user = authenticate(request, email=email, password=password, id_number=id_number)
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully, you can now fill the loan application form')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email, ID number, or password')
        except Exception as e:
            logger.error(f"Error in sign_in view: {e}")
            messages.error(request, 'An error occurred during sign-in. Please try again.')
    return render(request, 'kopa/login.html')





    
    
   

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None
    
 
    
@login_required
def guarantor_view(request, loan_id):
    context = {}
    if request.method == 'POST':
        try:
            # Parse the guarantee date
            guarantee_date_str = request.POST.get('guarantee_date', '')
            guarantee_date = parse_date(guarantee_date_str)
            print(f"Parsed guarantee date: {guarantee_date}")

            # Get the LoanInfo associated with the loan_id
            print(f"Fetching LoanInfo with ID: {loan_id}")
            loan_info = get_object_or_404(LoanInfo, id=loan_id)
            context['loan_info'] = loan_info
            print(f"LoanInfo found: {loan_info}")

            # Save Guarantor information
            guarantor = Guarantor.objects.create(
                loan_info=loan_info,
                full_name=request.POST.get('full_name', ''),
                nick_name=request.POST.get('nick_name', ''),
                id_number=request.POST.get('id_number', ''),
                phone1=request.POST.get('phone1', ''),
                phone2=request.POST.get('phone2', ''),
                email=request.POST.get('email', ''),
                face_image=request.FILES.get('face_image'),
                guarantee_name=request.POST.get('guarantee_name', ''),
                loan_amount=request.POST.get('loan_amount', ''),
                loan_amount_words=request.POST.get('loan_amount_words', ''),
                guarantee_date=guarantee_date,
                residence=request.POST.get('residence', ''),
                signature_image=request.FILES.get('signature_image'),
            )
            print("Guarantor saved successfully.")
            print(f"Guarantor details: {guarantor}")

            # Handle collateral items
            item_count = int(request.POST.get('item_count', 0))
            print(f"Number of collateral items: {item_count}")
            for i in range(1, item_count + 1):
                item_name = request.POST.get(f'item-name-{i}', '')
                item_description = request.POST.get(f'item-description-{i}', '')
                photo1 = request.FILES.get(f'item-photo-{i}-1')
                photo2 = request.FILES.get(f'item-photo-{i}-2')
                photo3 = request.FILES.get(f'item-photo-{i}-3')
                photo4 = request.FILES.get(f'item-photo-{i}-4')

                print(f"Saving collateral item {i}:")
                print(f"Item name: {item_name}")
                print(f"Item description: {item_description}")
                print(f"Photo1: {photo1}")
                print(f"Photo2: {photo2}")
                print(f"Photo3: {photo3}")
                print(f"Photo4: {photo4}")

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
            messages.success(request, "Guarantor information submitted successfully.")
            return redirect('home')

        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, "An error occurred while saving Guarantor information.")
    
    # For non-POST requests
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


@login_required
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
                    face_image=request.FILES.get('face_image'),
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
                #id=id,
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
                signature_image=request.FILES.get('signature_image'),
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
        #messages.error(request, f"An error occurred while processing the form, fill all required form fields",e)
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('client')



@login_required
def client_profile(request, client_id, loan_id):
    # Retrieve the profile using the provided client_id
    profile = get_object_or_404(Profile, id=client_id)
    
    # Fetch the associated data
    loan_info = get_object_or_404(LoanInfo, id=loan_id, profile=profile)
    if loan_info.check_and_delete_if_no_guarantor():
        print("LoanInfo was deleted because it has no guarantor.")
    else:
        print("LoanInfo was not deleted because it has a guarantor.")
    spouse_info = profile.spouse_info
    residence_info = profile.residence_info
    crb_info = loan_info.crb_info
    guarantor = loan_info.guarantor
    #client_collaterals = [loan.client_collaterals.all() for loan in loan_infos]
    
    

    # Pass the client and related data to the template context
    context = {
        'profile': profile,
        'loan_info': loan_info,
        'spouse_info': spouse_info,
        'residence_info': residence_info,
        'crb_info': crb_info,
        'guarantor': guarantor,
        #'client_collaterals': client_collaterals,
    }
    
    return render(request, 'kopa/profile.html', context)
    


@login_required
def client_info_view(request):
    # Fetch all LoanInfo records along with related data
    loan_infos = LoanInfo.objects.select_related(
        'profile',  # Fetch Profile linked with LoanInfo
        'profile__spouse_info',  # Fetch SpouseInfo linked with Profile
        'profile__residence_info',  # Fetch ResidenceInfo linked with Profile
        'guarantor'  # Fetch Guarantor linked with LoanInfo
    ).prefetch_related(
        'client_collaterals',  # Fetch Client_Collateral linked with LoanInfo
        'crb_info'  # Fetch CRBInfo linked with LoanInfo
    )
    query = request.GET.get('q')
    if query:
        profiles = CustomUser.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(id_number__icontains=query) |
            Q(email__icontains=query) 
           
        )
        logging.debug(f"Profiles found: {profiles}")  # Log the profiles found
    else:
        profiles = CustomUser.objects.all()
    
    # Combine all necessary context data into a single dictionary
    context = {
        'loan_infos': loan_infos,
        'profiles': profiles,
    }

    # Render the template with all the related data
    return render(request, 'kopa/dashboard.html', context)


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