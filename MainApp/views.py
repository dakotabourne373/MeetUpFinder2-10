from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.views.generic import TemplateView, ListView

# importing models
from .models import Event, Address, Profile, GroupMember
from django.contrib.auth.models import User

# importing model filter stuff
from django.db.models import Q

from django.db.models import CharField, Model 
from django_mysql.models import ListCharField
import datetime

#Logout import
from django.contrib.auth import logout

# inlcude for timezone check
from pytz import timezone
import pytz


# Create your views here.
def mainpage(request):
    # getting UTC timezone for comparison
    utc = pytz.UTC
    # get the current time in utc
    now = datetime.datetime.utcnow()
    
    # get the current time so expired events are not present
    # need to make it an aware datetime field
    now = now.replace(tzinfo=utc)
    # day variable to check for when an event is over a day old
    day = datetime.timedelta(days=1)


    # gets all of the live events
    live_events = Event.objects.filter(Q(event_date__lt=now),Q(event_endtime__gt=now))

    # gets all of the upcoming ev from the database that aren't occuring
    upcoming_events = Event.objects.filter(Q(event_date__gt=now),Q(event_endtime__gt=now))

    # gets all of the events that have expired within the past day
    recently_expired = Event.objects.filter(Q(event_endtime__gt=(now-day)),Q(event_endtime__lt=(now)))

    # Gathers all expired events
    expired_events = Event.objects.filter(event_endtime__lt=(now-day))

    # delete all of the expired events
    if expired_events:
        expired_events.delete()

    context= {
        'upcoming_events': upcoming_events,
        'recently_expired' : recently_expired,
        'live_events' : live_events,
    }



    return render(request, 'MainApp/mainpage.html', context)

def eventForm(request):

    # checks to make sure they are logged in first
    if (not request.user.is_authenticated) or (request.user.is_anonymous):
        return render(request, 'MainApp/login.html')

    event = Event()

    context = {

        'event_tags': event.event_tags

    }

    return render(request, 'MainApp/event_form.html',context)


def login(request):

    if request.user.is_authenticated:

        signed_in = True
    else:

        signed_in = False

    context = {
        'signed_in' : signed_in,
    }


    return render(request, 'MainApp/login.html',context)

def Logout(request):
    logout(request)

    context = {
        'signed_in' : False,
    }
    return render(request, 'MainApp/login.html',context)

def createEvent(request):
    if( request.method == "POST"):

        # Creating a new event
        event = Event()


        # assigning attributes to the created event
        event.event_name = request.POST['eventName']
        event.event_description = request.POST['eventDescription']
        event.event_date = request.POST['dateTime']

        # might want a condition to check if addresss exists already
        # Adding new address to the database
        address = Address()

        addy = request.POST.get('addy')

        # Getting all of the address email from the html post request
        # fills in "?" when the field is not found
        address.street_number = request.POST.get('street_number','?')
        address.street_name = request.POST.get('route',"?")
        address.city = request.POST.get('locality',"?")
        address.state = request.POST.get('administrative_area_level_1',"?")
        address.zip_code = request.POST.get('postal_code',"?")
    
        address.save()

        # Now that the address is saved, we can assign it to the event
        event.event_location = address
        event.event_endtime = request.POST['endTime']
        
        event.event_capacity = request.POST['capacity']
        # subtract 1 from capacity since host is included
        event.event_capacity = int(event.event_capacity) - 1

        # Still need to figure out if duration should be there or 
        # and how we will handle event_tags
        the_tags = request.POST.getlist('tags')

        for tag in the_tags:
            event.event_tags.append(tag)

        # saves event
        event.save()       


        # adding user as creator
        profile = Profile.objects.get(user=request.user)
        new_member = GroupMember.objects.create(profile=profile,group=event,type='creator')
        new_member.save()

        # return to the main page
        return HttpResponseRedirect(reverse('mainpage'))
    else:
        # return to the main page
        return HttpResponseRedirect(reverse('mainpage'))
    
def event_detail_view(request,event_id):

    # get the event being accessed
    event = get_object_or_404(Event, pk=event_id)
    
    # if they are not logged in, then not a member
    if (not request.user.is_authenticated) or (request.user.is_anonymous):
        is_member = False
    # if they are logged in, check to see if they are a member or not
    else:    
        # get the profile of the user
        profile = Profile.objects.get(user=request.user)

        # check to see if the user is already a group member for this event
        group_member = GroupMember.objects.filter(profile=profile,group=event)

        print(group_member)
        # Checks if they are already a member or not
        if group_member:
            print("Is a member")
            is_member = True
        else:
            print("Is not a member")
            is_member = False

    # Need to Get the Creator of the event and the attendees
    # both of these will be query sets
    attendees = GroupMember.objects.filter(group=event,type='attendee')
    # Query set that should only contain one person
    creator = GroupMember.objects.filter(group=event,type='creator')

    if creator.count() > 0:
        creator_name = creator[0].profile.name
    else:
        creator_name = "N/A"
    
    # Check to see if the event is finished or not
    is_finished = event.is_finished()

    # Check to see if the event is at capacity or not
    at_capacity = event.at_capacity()

    # check to see if the creator or not
    username = request.user.username
    if(username == creator_name):
        is_creator = True
    else:
        is_creator = False
    
    
    
    # Pass in the context variable for the html
    context = {
        'event': event,
        'is_member' : is_member,
        'attendees' : attendees,
        'creator' : creator_name,
        'finished' : is_finished,
        'at_capacity' : at_capacity,
        'is_creator' : is_creator,

    }
    return render(request,"MainApp/event_detail.html", context)    


def eventSearchResults(request):

    query = request.GET['query'] 
    # first object list is filtered events with the query in their name or description
    obj = Event.objects.filter(Q(event_name__icontains=query)|Q(event_description__icontains=query)) # can also add in | Q() for more filters
    # second object list is filtered events with the query somewhere in their address
    obj2 = Event.objects.filter(
        Q(event_location__street_number__icontains=query)|
        Q(event_location__city__icontains=query) |
        Q(event_location__street_name__icontains=query) |
        Q(event_location__zip_code__icontains=query) |
        Q(event_location__state__icontains=query)
    )
    # Checking the tags
    obj3 = Event.objects.filter(event_tags__contains='party') 


    context = {
        'object_list' : obj,
        'address_list' : obj2,
        'filter_list' : obj3,
        'q' : query
    }
    
    return render(request, "MainApp/search_results.html", context)


def profile_view(request):
    
    # checks to make sure they are logged in first
    if (not request.user.is_authenticated) or (request.user.is_anonymous):
        return render(request, 'MainApp/login.html')

    # get the profile of the user
    profile = Profile.objects.get(user=request.user)

    # get the users events they are rsvped for
    rsvped_events = Event.objects.filter(people=profile, membership__type='attendee')
    created_events = Event.objects.filter(people=profile, membership__type='creator')
    #user_events.filter(event_date__)

    context = {
        'profile' : profile,
        'rsvped_events' : rsvped_events,
        'created_events' : created_events,


    }

    return render(request, 'MainApp/profile.html', context)

def rsvp_event(request,event_id):

    # checks to make sure they are logged in first
    if (not request.user.is_authenticated) or (request.user.is_anonymous):
        return render(request, 'MainApp/login.html')


    # get the event information
    curr_user = request.user
    # Get the event passed in and the profile of the user
    event = get_object_or_404(Event, pk=event_id)
    profile = Profile.objects.get(user=curr_user)

    # Gets the user if they are the creator
    creator_list = GroupMember.objects.filter(profile=profile,group=event,type='creator')

    # If this event has them as the creator, then delete the event and go to rsvp_page
    if(creator_list):
        # Since the event is being deleted, we can move to the rsvp_success page,
        # show their events, and then redirect them home
        event_deleted = True
        event.delete()
        #still want to show their events
        user_events = Event.objects.filter(people=profile)  

        context = {
            'user_events' : user_events,
            'event_deleted' : event_deleted,
        }

        return render(request,'MainApp/rsvp_success.html', context)
    else:
        event_deleted = False

    # Check here to see if the event is at capacity or not
    # This is just a check to make sure they can't RSVP when
    # an event is already full
    if event.at_capacity():
        # This should not be entered because the RSVP button should not be availible
        # when the event is full
        print("The event is at capacity")

    # check to see if the user is already a group member for this event
    group_member = GroupMember.objects.filter(profile=profile,group=event)

    # Checks if they are already a member or not
    # If they are a member, remove them
    if group_member:

        was_member = True

        user_events = Event.objects.filter(people=profile)  

        group_member.delete()

        # need to change the capacity of the event here *******************************
        event.event_capacity = int(event.event_capacity) + 1
        # now save the new capacity
        event.save()

        context = {
            'user_events' : user_events,
            'was_member' : was_member,
            'event_deleted' : event_deleted,
        }

        return render(request,'MainApp/rsvp_success.html', context)
    # If they are not a member, add them
    else:
       
        was_member = False
        
        new_member = GroupMember.objects.create(profile=profile,group=event,type='attendee')

        new_member.save()

        user_events = Event.objects.filter(people=profile)

        # need to change the capacity of the event here *******************************

        event.event_capacity = int(event.event_capacity) - 1
        # now save the event
        event.save()

        context = {
            'user_events' : user_events,
            'was_member' : was_member,
            'event_deleted' : event_deleted,
        }

        return render(request,'MainApp/rsvp_success.html', context)

