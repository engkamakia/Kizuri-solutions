from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy 

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
import uuid


'''
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # This should be auto-populated

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'id_number']

'''
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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



    
class ClientInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_infos')
    #full_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    #national_id = models.CharField(max_length=20)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    #email = models.EmailField()
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
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.CharField(max_length=255)
    date_of_loan = models.DateField()
    repay_principal = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    repay_date = models.DateField()
    
    class Meta:        
        verbose_name_plural = "Client information"              
    
    def __str__(self):
        return f" {self.user.first_name} {self.user.last_name} "

class SpouseInfo(models.Model):
    client = models.OneToOneField(ClientInfo, on_delete=models.CASCADE, related_name='spouse_info')
    marital_status = models.CharField(
        max_length=20,
        choices=[('Married', 'Married'), ('Single', 'Single')]
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
        return f" {self.client} "

class ResidenceInfo(models.Model):
    client = models.OneToOneField(ClientInfo, on_delete=models.CASCADE, related_name='residence_info')
    permanent_residence = models.CharField(max_length=255)
    temporary_residence = models.CharField(max_length=255, blank=True, null=True)
    rural_residence = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:        
        verbose_name_plural = "Residence information"              
    
    def __str__(self):
        return f" {self.client} "
    

class CRBInfo(models.Model):
    client = models.OneToOneField(ClientInfo, on_delete=models.CASCADE, related_name='crb_info')
    agree_to_terms = models.BooleanField(default=False, verbose_name="Agree to Terms and Conditions")
    authorization_text = models.TextField(default="I authorize Kizuri Solutions Limited to access my credit profile from credit reference bureau.")
    
    class Meta:        
        verbose_name_plural = "CRB infomation"              
    
    def __str__(self):
        return f" {self.client} "
    
    
    
class Guarantor(models.Model):
    client_info = models.OneToOneField(ClientInfo, on_delete=models.CASCADE, related_name='guarantor')
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, blank=True)
    id_number = models.CharField(max_length=50)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    guarantee_name = models.CharField(max_length=255)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_amount_words = models.CharField(max_length=255)
    guarantee_date = models.DateField(null=True, blank=True)
    residence = models.CharField(max_length=255)
    
    class Meta:        
        verbose_name_plural = "Guarantors"              
    
    def __str__(self):
        return f" {self.full_name} "
    

class Collateral(models.Model):
    guarantor = models.ForeignKey(Guarantor, on_delete=models.CASCADE, related_name='collaterals')
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    photo1 = models.ImageField(upload_to='collateral_photos/')
    photo2 = models.ImageField(upload_to='collateral_photos/')
    photo3 = models.ImageField(upload_to='collateral_photos/')
    photo4 = models.ImageField(upload_to='collateral_photos/')
    
    class Meta:        
        verbose_name_plural = "Collaterals"              
    
    def __str__(self):
        return f" {self.guarantor} "
    
    
