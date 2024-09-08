from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy 

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
import uuid
from cloudinary.models import CloudinaryField

from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, id_number, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            id_number=id_number,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        
        
        return user

    def create_superuser(self, first_name, last_name, id_number, email, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            id_number=id_number,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        
        
        
        return user

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'id_number']

    def __str__(self):
        return f" {self.first_name} {self.last_name} "

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

 
    
class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profiles')   
    nickname = models.CharField(max_length=255, blank=True, null=True)   
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    face_image = CloudinaryField('client_image')
   
    employment_status = models.CharField(
        max_length=20,
        choices=[('employed', 'Employed'), ('unemployed', 'Unemployed'), ('self-employed', 'Self-employed')]
    )
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    location_of_work = models.CharField(max_length=255, blank=True, null=True)
    supervisors_name = models.CharField(max_length=255, blank=True, null=True)
    supervisors_contact = models.CharField(max_length=15, blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_expense = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    industry_type = models.CharField(max_length=255, blank=True, null=True)
    business_location = models.CharField(max_length=255, blank=True, null=True)
    daily_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    daily_expense = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)    
    
    class Meta:        
        verbose_name_plural = "Profiles"              
    
    def __str__(self):
        return f" {self.user.first_name} {self.user.last_name} "
    
class LoanInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True) 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='loan_infos')   
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.CharField(max_length=255)
    date_of_loan = models.DateField()
    repay_principal = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    repay_date = models.DateField()
    is_paid = models.BooleanField(default=False) 
    
    class Meta:        
        verbose_name_plural = "Loan information"              
    
    def __str__(self):
        return f" {self.profile}"
    
     # Method to check if the LoanInfo object has a guarantor and delete if it doesn't
    def check_and_delete_if_no_guarantor(self):
        # Check if there is no related guarantor
        if not hasattr(self, 'guarantor'):
            # If no guarantor exists, delete the LoanInfo object
            self.delete()
            return True  # Return True if the LoanInfo was deleted
        return False  # Return False if the LoanInfo has a guarantor and wasn't deleted
    
class SpouseInfo(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='spouse_info')
    marital_status = models.CharField(
        max_length=20,
        choices=[('married', 'married'), ('single', 'single')]
    )
    spouse_name = models.CharField(max_length=255, blank=True, null=True)
    work_place = models.CharField(max_length=255, blank=True, null=True)
    position= models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    no_of_dependants = models.PositiveIntegerField()
    
    parent_type = models.CharField(
        max_length=6,
        choices=[('father', 'Father'), ('mother', 'Mother')],
        blank=True,
        null=True
    )
    father_full_name = models.CharField(max_length=255, blank=True, null=True)
    father_contact = models.CharField(max_length=15, blank=True, null=True)
    mother_full_name = models.CharField(max_length=255, blank=True, null=True)
    mother_contact = models.CharField(max_length=15, blank=True, null=True)
    
    nextofkin = models.CharField(max_length=255, blank=True, null=True)

    
    class Meta:        
        verbose_name_plural = "Spouse information"              
    
    def __str__(self):
        return f" {self.profile} "

class ResidenceInfo(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='residence_info')
    RESIDENCE_TYPE_CHOICES = [
        ('permanent', 'Permanent Residence'),
        ('temporary', 'Temporary Residence'),
    ]
    
    residence_type = models.CharField(
        max_length=20,
        choices=RESIDENCE_TYPE_CHOICES,
        blank=True,
    )
    residence_description = models.CharField(max_length=255, blank=True, null=True)
    rural_residence = models.TextField(max_length = 450,null = True, blank = True)
    
    class Meta:        
        verbose_name_plural = "Residence information"              
    
    def __str__(self):
        return f" {self.profile} "
    

class CRBInfo(models.Model):
    loan_info = models.OneToOneField(LoanInfo, on_delete=models.CASCADE, related_name='crb_info')
    signature_image = CloudinaryField('signature_pic')
    agree_to_terms = models.BooleanField(default=False, verbose_name="Agree to Terms and Conditions")
    authorization_text = models.TextField(default="I authorize Kizuri Solutions Limited to access my credit profile from credit reference bureau.")
    
    class Meta:        
        verbose_name_plural = "CRB infomation"              
    
    def __str__(self):
        return f" {self.loan_info} "
    
    
    
class Guarantor(models.Model):
    loan_info = models.OneToOneField(LoanInfo, on_delete=models.CASCADE, related_name='guarantor')
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, blank=True)
    id_number = models.CharField(max_length=50)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    face_image = CloudinaryField('guarantor_face')
    guarantee_name = models.CharField(max_length=255)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_amount_words = models.CharField(max_length=255)
    guarantee_date = models.DateField(null=True, blank=True)
    residence = models.CharField(max_length=255)
    signature_image = CloudinaryField('guarantor_signature')
    
    
    class Meta:        
        verbose_name_plural = "Guarantors"              
    
    def __str__(self):
        return f" {self.full_name} "
    

class Collateral(models.Model):
    guarantor = models.ForeignKey(Guarantor, on_delete=models.CASCADE, related_name='collaterals')
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    photo1 = CloudinaryField('guarantor_collateral')
    photo2 = CloudinaryField('guarantor_collateral')
    photo3 = CloudinaryField('guarantor_collateral')
    photo4 = CloudinaryField('guarantor_collateral')
    
    class Meta:        
        verbose_name_plural = "Collaterals"              
    
    def __str__(self):
        return f" {self.guarantor} "
    
class Client_Collateral(models.Model):
    loan_info = models.ForeignKey(LoanInfo, on_delete=models.CASCADE, related_name='client_collaterals')
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    photo1 = models.ImageField(upload_to='collateral_photos/')
    photo2 = models.ImageField(upload_to='collateral_photos/')
    photo3 = models.ImageField(upload_to='collateral_photos/')
    photo4 = models.ImageField(upload_to='collateral_photos/')
    
    class Meta:        
        verbose_name_plural = "Client Collaterals"              
    
    def __str__(self):
        return f" {self.item_name} "