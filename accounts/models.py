from locale import currency
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.dispatch import receiver
from django_extensions.db.models import CreationDateTimeField
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# hook in the New Manager to our Model


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=2000, blank=True, null=True)
    phone = models.CharField(max_length=11)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Message(models.Model):
    created = CreationDateTimeField()
    sender = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    subject = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created']


class ResponseMessage(models.Model):
    created = CreationDateTimeField()
    receiver = models.ForeignKey(
        User, related_name='response_messages', on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    subject = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created']


class AvailableBanks(models.Model):
    active = models.BooleanField()
    code = models.CharField(max_length=100)
    country = models.CharField(max_length=255)
    createdAt = models.DateTimeField()
    currency = models.CharField(max_length=10)
    gateway = models.CharField(max_length=300, null=True)
    id = models.IntegerField(primary_key=True)
    is_deleted = models.BooleanField()
    longcode = models.CharField(max_length=255)
    name = models.CharField(max_length=300)
    pay_with_bank = models.BooleanField()
    slug = models.SlugField()
    type = models.CharField(max_length=255)
    updatedAt = models.DateTimeField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Banks'
        verbose_name_plural = 'Available Banks'


class UserAccountNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='account_numbers', related_query_name='account_numbers')
    bank = models.ForeignKey(AvailableBanks, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=15, unique=True)
    account_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs) -> None:
        qs = UserAccountNumber.objects.filter(user=self.user).exclude(
            account_number=self.account_number)
        if qs.exists():
            print('Qs exists')
            qs.delete()

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Account detail'
        verbose_name_plural = 'Account details'
