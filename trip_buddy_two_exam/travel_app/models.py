from django.db import models
from django.utils.dateparse import parse_date
import datetime
import re	# the regex module
import bcrypt
# Create your models here.

class userManager(models.Manager):
    def basic_validator_reg(self, postData):
        print('we are in the userManager Register Validator, printing postData below')
        print(postData)
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "The first name must have at least 2 characters"
        if len(postData['fname']) == 0:
            errors["nofname"] = "You must fill in the first name field"
        if len(postData['lname']) < 2:
            errors["lname"] = "The last name must have at least 2 characters"
        if len(postData['lname']) == 0:
            errors["nolname"] = "You must fill in the last name field"
        Users = User.objects.all()
        for user in Users:
            if user.email == postData['emailreg']:
                errors["email_in_use"] = "This email is already in use"
        if len(postData['emailreg']) == 0:
            errors['emailrequired'] = "Must fill in an email address"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['emailreg']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['passwreg']) < 8:
            errors["passwreg"] = "Password must contain more than 8 characters"
        if postData['passwreg'] == postData['passwregcon']:
            pass
        else:
            errors["passwreg"] = "Password does not match confirmation password"

        print(f"this is the current date {datetime.date.today()}" )
        print(f"this is the posted date {postData['birthdate']}" )

        if parse_date(postData['birthdate']) > datetime.date.today():
            errors["birthdate"] = "The date must be in the past" 
        if calculate_age(parse_date(postData['birthdate'])) < 13 :
            errors["tooyoung"] = "Must be older the 13 to register"
    
        return errors

    def basic_validator_log(self, postData):
        print("***")
        print('we are in the userManager Login Validator, printing postData below')
        print("***")
        print("This are the errors at basic_validator_log")
        print(postData)
        errors = {}
        
        if len(postData['passwlog']) == 0 :
            errors["no_email"] = "The first name must have at least 2 characters"
        if len(postData['passwlog']) < 8:
            errors["passwlog"] = "Password must contain more than 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['emaillog']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"

        Users = User.objects.all()
        print(f"this is all the user objects: {Users}")
        for user in Users:
            print(f"this is all the users: {user}")
            print("***")
            print(f"{user.email}")
            print("***")
            if user.email == postData['emaillog']:
                if bcrypt.checkpw(postData['passwlog'].encode(), user.password.encode()):
                    print("password match")
                    return errors
                else:
                    print("incorrect password")
        errors["nonexistent_email"] = "There is no account with this email address"
    

        print(f"this is the current date {datetime.date.today()}" )
    
        return errors

    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = userManager()


def calculate_age(born):
        today = datetime.date.today()
        age = (today - born).days/365
        return age


class tripManager(models.Manager):
    def basic_validator(self, postData):
        print('we are in the userManager Register Validator, printing postData below')
        print(postData)
        errors = {}
        if len(postData['destination']) < 3:
            errors["destination"] = "The destination must have at least 3 characters"
        if len(postData['destination']) == 0:
            errors["nodestination"] = "Fill out the 'Destination' field. Can't take a trip without a destination!"
        if len(postData['plan']) < 3:
            errors["plan"] = "The plan must have at least 3 characters"
        if len(postData['plan']) == 0:
            errors["noplan"] = "Fill out the 'Plan' field. Can't take a trip without a plan!"
        
        if parse_date(postData['startdate']) < datetime.date.today():
            errors["startdate"] = "The date must be in the future, you can't time travel!" 
        if parse_date(postData['startdate']) > parse_date(postData['endate']):
            errors["endate"] = "Time travel is not allowed, you can't end the trip before you start the trip!" 
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    startdate = models.DateField()
    endate = models.DateField()
    creator = models.IntegerField()
    attendees = models.ManyToManyField(User, related_name="trips")
    plan = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = tripManager()