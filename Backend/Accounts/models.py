from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, Name,TC, password=None,password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            Name=Name,
            TC=TC,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, Name, TC, password=None):
        """
        Creates and saves a superuser with the given email, name 
        """
        user = self.create_user(
            email,
            password=password,
            Name=Name,
            TC=TC,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
# custom user model #
class User(AbstractBaseUser): #This is model which contain ,email,name,tc
    email = models.EmailField(
        verbose_name="email ",
        max_length=255,
        unique=True,
    )
    Name = models.CharField(max_length=100)
    TC = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["Name","TC"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    