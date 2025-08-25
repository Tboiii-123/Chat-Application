from django.db import models


from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
          

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
          



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
          



class Profile(models.Model):

    #Linking the fk to the use models that is imported
    user =models.OneToOneField(User, on_delete=models.CASCADE ,related_name='profile')


    fname=models.CharField(max_length=200,blank=True)
    
    lname=models.CharField(max_length=200,blank=True)

    username =models.CharField(max_length=200,blank=True)
    

    email =models.EmailField(blank=True)

    number =models.CharField(max_length=200,blank=True)

    address =models.CharField(max_length=200, blank=True)

    Dob =models.DateField(blank=True, null=True)

    about =models.TextField(blank=True)
     
    #To add a default profile 
    #We use default attribute
    profile_img  =models.ImageField(upload_to='profile',default ='blank.png',blank=True)

    



    def __str__(self):

        return self.user.username


class Friend(models.Model):
    profile =models.OneToOneField(Profile,on_delete=models.CASCADE)


    def __str__(self):

        return self.profile.fname




class ChatMessage(models.Model):
    body =models.TextField()
    msg_sender =models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='msg_sender')
    msg_receiver =models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='msg_receiver')
  
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    is_read = models.BooleanField(default=False,blank=True)
    voice_note = models.FileField(upload_to='voice_notes/', blank=True, null=True)
    


    def __str__(self):

        return self.body
