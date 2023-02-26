from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.conf import settings
import random
import string

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, referral_code=None, my_ref_code=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            referral_code=referral_code,
            my_ref_code=my_ref_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    my_ref_code = models.CharField(max_length=5, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class ReferralCode(models.Model):
    code = models.CharField(max_length=50, unique=True, default=generate_referral_code)
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referrer')
    
    # referred_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='referral_code', blank=True)

    def __str__(self):
        return self.code
