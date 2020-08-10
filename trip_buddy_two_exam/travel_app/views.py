from django.shortcuts import render, redirect
import bcrypt
# Create your views here.
from django.contrib import messages
from .models import User, Trip
import datetime


def create_user(request):
    print(request.POST)
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator_reg(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        messages.info(request, 'Registration')
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        securepassword = bcrypt.hashpw(request.POST['passwreg'].encode(), bcrypt.gensalt()).decode()
        print(f"This is the secure password {securepassword}")
        user = User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email= request.POST['emailreg'], password=securepassword)
        request.session['loggedinID'] = user.id
        messages.success(request, "Successfully Registered!")
        # redirect to a success route
        return redirect('/dashboard')

def index(request):
    print(datetime.date.today())
    print(datetime.datetime.now())
    all_messages = list(messages.get_messages(request))
    print(f"This is all messages: {all_messages}")
    all_error_messages_content = [msg.message for msg in list(messages.get_messages(request))]
    print(f"This is the all error messages: {all_error_messages_content}")
    context = {
        'all_messages': all_error_messages_content
    }

    return render(request, 'login_reg_page.html', context)

def success(request):
    checkLogIn(request)
        
    loggedinuser = User.objects.get(id = request.session['loggedinID'])
    my_trips = Trip.objects.filter(creator = request.session['loggedinID'])
    trips_joined = loggedinuser.trips.all()
    alltrips = Trip.objects.exclude(creator=request.session['loggedinID'])
    context = {
        'loggedinuser': loggedinuser,
        'my_trips': my_trips,
        'alltrips': alltrips,
        'joined_trips': trips_joined,
    }
    return render(request, 'success.html', context)

def login(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator_log(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        messages.info(request, 'Login')
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save
        loggedUser = User.objects.filter(email = request.POST['emaillog'])[0]
        print(loggedUser)      
        request.session['loggedinID'] = loggedUser.id
        messages.success(request, "Successfully Logged In!")
        # redirect to a success route
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def trip_page(request):
    checkLogIn(request)

    loggedinuser = User.objects.get(id = request.session['loggedinID'])
    context = {
        'loggedinuser': loggedinuser
    }
    return render(request, 'trip_maker_page.html', context)

def plan_trip(request):
    loggedinuser = User.objects.get(id = request.session['loggedinID'])
    print(request.POST)
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Trip.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/trips/new')
    else:
        trip = Trip.objects.create(destination=request.POST['destination'], startdate=request.POST['startdate'], endate= request.POST['endate'],  creator= request.session['loggedinID'], plan= request.POST['plan'])

        print(f"{loggedinuser.first_name} is creating a trip numbered {trip.id} to {trip.destination}")
        
        messages.success(request, "Successfully Planned Trip!")
        # redirect to a success route
        return redirect('/dashboard')

def destroy(request, x):
    triptodelete = Trip.objects.get(id = x)
    triptodelete.delete()
    return redirect('/dashboard')

def editTrip(request, x):
    tripToEdit = Trip.objects.get(id = x)
    loggedinuser = User.objects.get(id = request.session['loggedinID'])
    context = {
        'currTrip': tripToEdit,
        'loggedinuser': loggedinuser
    }
    return render(request, 'trip_editor_page.html', context)

def updateTrip(request, x):
    checkLogIn(request)
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        trip = Trip.objects.get(id = x)
        return redirect(f'/trips/edit/{trip.id}')
    else:
        tripToUpdate = Trip.objects.get(id = x)
        tripToUpdate.destination = request.POST['destination']
        tripToUpdate.plan = request.POST['plan']
        tripToUpdate.startdate = request.POST['startdate']
        tripToUpdate.endate = request.POST['endate']
        tripToUpdate.save()
        print(request.POST)
        return redirect('/dashboard')

def tripage(request, x):
    currentTrip = Trip.objects.get(id = x)
    loggedinuser = User.objects.get(id = request.session['loggedinID'])
    trip_creator = User.objects.get(id = currentTrip.creator)
    creator_name = f"{trip_creator.first_name} {trip_creator.last_name[0]}"
    attenders = currentTrip.attendees.all()
    context = {
        'currentTrip': currentTrip,
        'loggedinuser': loggedinuser,
        'tripcreator': creator_name,
        'attenders': attenders
    }
    return render(request, 'trip_info_page.html', context)

def joinATrip(request, x):
    the_trip = Trip.objects.get(id=x)
    attendee_id = request.session['loggedinID']
    the_trip.attendees.add(User.objects.get(id=attendee_id))
    return redirect('/dashboard')

def cancel(request, x):
    the_trip = Trip.objects.get(id=x)
    attendee_id = request.session['loggedinID']
    the_trip.attendees.remove(User.objects.get(id=attendee_id))
    return redirect('/dashboard')

def checkLogIn(request):
     #Can't do to this route if you're not logged in
    if 'loggedinID' not in request.session:
        messages.info(request, 'notlogged')
        messages.error(request, "User is not logged in")
        print("We are at the logged out redirect button")
        return redirect('/')