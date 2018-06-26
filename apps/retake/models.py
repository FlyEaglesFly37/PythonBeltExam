from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateRegistration(self, postData):
        errors = []
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 3:
            errors.append("First name must be greater than 3 characters")
        if len(postData['last_name']) < 3:
            errors.append('Last Name must be greater than 3 characters')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Please enter a valid email address')
        if len(existing_user):
            errors.append('This email already exists')
        if len(postData['pw']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['pw'] != postData['cpw']:
            errors.append('Passwords must match')
        if len(errors):
            return errors
        me = User.objects.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            password= bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
            )
        return me

    def validateLogin(self, postData):
        errors = []
        existing_user_list = User.objects.filter(email=postData['email'])
        if len(existing_user_list):
            if bcrypt.checkpw(postData['pw'].encode(), existing_user_list[0].password.encode()):
                return existing_user_list[0]
        return 'invalid email / password combination'

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name='uploaded_quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name='liked_quotes')


# Create your models here.
