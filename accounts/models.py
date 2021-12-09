from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.expressions import Value

# Possible improvement: add a grader user class that can update students grades. (Maybe same power could be given to faculty?)

#================================================                   User Model Manager             ====================================================

class UserManager(BaseUserManager):

    #UserManager handles creating different types of users
        #The various methods here deal with the creation of a student, faculty, spc, superSpc, placement and admin users

    #Student user creation method
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must provide a password')
        
        user = self.model(
            email=self.normalize_email(email),
        )
        #what is self.model? https://stackoverflow.com/questions/51163088/self-model-in-django-custom-usermanager

        user.set_password(password)
        user.save(using=self._db)
        return user

    #Faculty user creation method
    def create_coordinatoruser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, password=password)
        user.is_coordinator = True
        user.save(using=self._db) #'using' keyword tells django which db to do the save in.
                                    #self._db references the 'default' under DATABASES in settings.py
        return user
    
    #SPC User creation method
    def create_adminuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    #Super SPC creation method
    def create_technicianuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, password=password)
        user.is_technician = True
        user.save(using=self._db)
        return user

    

    #Admin Creation Method
    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
#==============================================                   End of User Model Manager            ============================================================
       



#==============================================                          User Model            ======================================================
class CustomUser(AbstractBaseUser):

    #CustomUser defines the model for Users of the portal

    email           = models.EmailField(max_length=255, unique=True)

    # is_active, is_staff and is_superuser attributes are required attributes in a user model to integrate with the admin app.
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False) # staff has special meaning in django. Does not refer to faculty
    is_superuser    = models.BooleanField(default=False) # a superuser

    # below attributes are defined for providing other functionalities
    is_coordinator          = models.BooleanField(default=False)
    is_admin     = models.BooleanField(default=False)
    is_technician    = models.BooleanField(default=False)
    """is_student      = models.BooleanField(default=True)
    is_faculty      = models.BooleanField(default=False)"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
                            #email since it has been specified as the USERNAME_FIELD
    #no field for pwd as it is inherited from AbstractBaseUser

    """ def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email """
    # The above are normally defined methods. (Conventions followed)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    #has_module_perms needs to be defined to view our user model on admin

    """ @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff """

    """ @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.is_superuser """
    #what is django's @propery decorator? https://stackoverflow.com/questions/58558989/what-does-djangos-property-do

    objects = UserManager() #links the user model to the user model manager.