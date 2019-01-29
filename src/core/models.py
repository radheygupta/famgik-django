from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class FamgikUserManager(BaseUserManager):
    """
    Custom Manager for FamgikUser

    """
    @staticmethod
    def normalize_phone(phone, country_code=None):
        phone = phone.strip().lower()
        try:
            import phonenumbers
            phone_number = phonenumbers.parse(phone, country_code)
            phone = phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.E164)
        except ImportError:
            pass

        return phone

    def _create_user(self, email, password,
                     is_staff, is_superuser, phone=None, **extra_fields):

        if not email:
            raise ValueError('User must have an email address.')

        if phone is not None:
            phone = FamgikUserManager.normalize_phone(
                phone, country_code=extra_fields.get("country_code"))

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            phone=phone,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class FamgikUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True, unique=True, db_index=True)
    phone = models.CharField(max_length=255, null=True, blank=True, unique=True, db_index=True)
    first_name = models.CharField(verbose_name="First Name", max_length=125)
    last_name = models.CharField(verbose_name="Last Name", max_length=125)
    is_staff = models.BooleanField(default=False, verbose_name="Staff Status")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_superuser = models.BooleanField(default=False, verbose_name="SuperUser")
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = FamgikUserManager()

    def get_full_name(self):
        """ Return the full name for the user."""
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        """ Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        db_table = 'famgik_user'








