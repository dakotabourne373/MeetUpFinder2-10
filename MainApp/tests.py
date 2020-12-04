# /***************************************************************************************
# *  REFERENCES
# *  Title: tests.py
# *  Author: jacobian (GitHub Name)
# *  Date Published: Feb 15th, 2011
# *  Date Accessed: October 20th, 2020
# *  Code version: first and only version
# *  URL: https://gist.github.com/jacobian/827937
# *  Software License: None
# *
# /***************************************************************************************
#
#
# Additional Test Cases (not unit test cases):
#
#         These are the general test cases for models and events that were able to
#     contain unit test cases. However, more integration, system, and acceptance 
#     testing was conducted for the HTML/User interface, login authentication, and 
#     profile authorization. Here are a few examples of other tests that were run:
#
#     * Testing that User could not access created event or see their "profile"
#       when they are not logged in throught their google account
#    
#     * Testing when event details are shown, the correct button is displayed
#       for every possible case (delete button when user is the creator, rsvp button
#       when the user is not a member and capacity is not full, unrsvp button if the
#       user is already a member, and lastly a message to the user when the event is 
#       at capacity and if they are not currently a member)
#
#     * Testing the google authentiction process and that the social accounts login
#       worked apporpriately
#
#     * Testing that when the user does not fully complete the event form then they
#       are prompted to fill in the rest of the form (submission is not allowed until
#       all the fields have been inputted)
#
#     * Testing that events are sorted correctly both on the main page (Current,
#       Upcoming, and Expired) as well as on the profile page (Created vs. RSVPed)
#
#

from django.test import TestCase
from MainApp.models import Event, Address, Profile, GroupMember

from django.contrib.auth.models import User

import datetime

from django.db.models import Q

# inlcude for timezone check
from pytz import timezone
import pytz

class EventModelTest(TestCase):

    def setUp(self):

        utc = pytz.UTC
        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=utc)

        print(now)
        print(now + datetime.timedelta(hours=1))

        # Setting up default stuff
        Address.objects.create(
            street_number="123",
            street_name="Main Street",
            city="Manassas",
            state="VA",
            zip_code="20110"
        )

        Event.objects.create(
            event_name="The Name",
            event_description="Some Description",
            event_date= now,
            event_endtime= now + datetime.timedelta(hours=1),
            event_location= Address.objects.get(street_name="Main Street"),
            event_public=True,
            event_capacity= 10,

        )

        Event.objects.create(
            event_name="Expired",
            event_description="this event is expired",
            event_date= now - datetime.timedelta(hours=1),
            event_endtime= datetime.datetime.now(),
            event_location= Address.objects.get(street_name="Main Street"),
            event_public=True,
            event_capacity= 10,

        )

        Event.objects.create(
            event_name="At Capacity",
            event_description="this event is at capacity",
            event_date= now - datetime.timedelta(hours=1),
            event_endtime= datetime.datetime.now(),
            event_location= Address.objects.get(street_name="Main Street"),
            event_public=True,
            event_capacity= 0,

        )

        Event.objects.create(
            event_name="IDK",
            event_description="this event should not be able to be created",
            event_date= now - datetime.timedelta(hours=1),
            event_endtime= datetime.datetime.now(),
            event_location= Address.objects.get(street_name="Main Street"),
            event_public=True,
            event_capacity= -1,

        )

    
    def test_made_event(self):
        event = Event.objects.get(event_name="The Name")
        self.assertEqual(event.event_name, "The Name")
        self.assertEqual(event.event_description,"Some Description")

    def test_event_not_finsihed(self):
        event = Event.objects.get(event_name="The Name")
        self.assertIs(event.is_finished(), False)
    
    def test_event_is_finished(self):
        event = Event.objects.get(event_name="Expired")
        self.assertIs(event.is_finished(), True)

    def test_event_public(self):
        event = Event.objects.get(event_name="The Name")
        self.assertIs(event.is_public(),True)
    
    def test_event_not_public(self):
        event = Event.objects.get(event_name="The Name")
        event.event_public = False
        self.assertIs(event.is_public(),False)

    def test_event_at_capacity(self):
        event = Event.objects.get(event_name="At Capacity")
        self.assertIs(event.at_capacity(),True)

    def test_event_not_at_capacity(self):
        event = Event.objects.get(event_name="The Name")
        self.assertIs(event.at_capacity(),False)

class GroupMemberTests(TestCase):

    def setUp(self):

        #Create Users for profile
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.user3 = User.objects.create_user(username='testuser3', password='12345')

        # Create Three People
        self.joe = Profile.objects.get(user=self.user1)
        self.bob = Profile.objects.get(user=self.user2)
        self.jim = Profile.objects.get(user=self.user3)
        

        # Create Simple Address for every event
        self.addy = Address.objects.create(
                        street_number="123",
                        street_name='Main Street',
                        city="Manassas",
                        state="VA",
                        zip_code="20110"
                    )

        # Create three events for testing
        self.party = Event.objects.create(
            event_name="Party",
            event_description="Some Description",
            event_date= datetime.datetime.now(),
            event_endtime= datetime.datetime.now() + datetime.timedelta(hours=1),
            event_location= self.addy,
            event_public=True,
        )
        
        self.study = Event.objects.create(
            event_name="Study",
            event_description="Some Description",
            event_date= datetime.datetime.now(),
            event_endtime= datetime.datetime.now() + datetime.timedelta(hours=1),
            event_location= self.addy,
            event_public=True,
        )
        
        self.grad = Event.objects.create(
            event_name="Graduation",
            event_description="Some Description",
            event_date= datetime.datetime.now(),
            event_endtime= datetime.datetime.now() + datetime.timedelta(hours=1),
            event_location= self.addy,
            event_public=True,
        )

        # Every person is a member of every group, but Joe admins Created Party,
        # Jim created Study, and Bob created Graduation
        GroupMember.objects.create(profile=self.joe,group=self.party, type='creator')
        GroupMember.objects.create(profile=self.jim,group=self.party, type='atendee')
        GroupMember.objects.create(profile=self.bob,group=self.party, type='atendee')


        GroupMember.objects.create(profile=self.joe,group=self.study, type='atendee')
        GroupMember.objects.create(profile=self.jim,group=self.study, type='creator')
        GroupMember.objects.create(profile=self.bob,group=self.study, type='atendee')

        GroupMember.objects.create(profile=self.joe,group=self.grad, type='atendee')
        GroupMember.objects.create(profile=self.jim,group=self.grad, type='atendee')
        GroupMember.objects.create(profile=self.bob,group=self.grad, type='creator')

    def test_unfiltered_membership(self):
        # What groups is Jim in?
        jims_groups = Event.objects.filter(people=self.jim)
        self.assertEqual(list(jims_groups),[self.party,self.study,self.grad])

    def test_creator_groups(self):
        # Which Groups did Jim Create?
        jims_created_events = Event.objects.filter(people=self.jim,membership__type='creator')
        self.assertEqual(list(jims_created_events),[self.study])

    def test_member_groups(self):
        # which groups is Bob just a atendee of?
        bob_attendee = Event.objects.filter(people=self.bob,membership__type='atendee')
        self.assertEqual(list(bob_attendee),[self.party,self.study])

    def test_cant_be_attendee_and_creator(self):
        bob_creator = Event.objects.filter(people=self.bob,membership__type='creator')
        bob_attendee = Event.objects.filter(people=self.bob,membership__type='atendee')
        self.assertEqual((bob_creator in bob_attendee),False)


    
class EventSearchTests(TestCase):
    def setUp(self):

        #Create Users for profile
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.user3 = User.objects.create_user(username='testuser3', password='12345')

        # Create Three People
        self.joe = Profile.objects.get(user=self.user1)
        self.bob = Profile.objects.get(user=self.user2)
        self.jim = Profile.objects.get(user=self.user3)
        

        # Create Simple Address for every event
        self.addy = Address.objects.create(
                        street_number="123",
                        street_name='Main Street',
                        city="Manassas",
                        state="VA",
                        zip_code="20110"
                    )

        # Create three events for testing
        self.party = Event.objects.create(
            event_name="Party",
            event_description="time to party!!!",
            event_date= datetime.datetime.now(),
            event_endtime= datetime.datetime.now() + datetime.timedelta(hours=1),
            event_location= self.addy,
            event_public=True,
        )
        
        self.study = Event.objects.create(
            event_name="Study",
            event_description="time to study!!!",
            event_date= datetime.datetime.now(),
            event_endtime= datetime.datetime.now() + datetime.timedelta(hours=1),
            event_location= self.addy,
            event_public=True,
        )
        
        self.grad = Event.objects.create(
            event_name="Graduation",
            event_description="time to graduate!!!",
            event_date= datetime.datetime.now(),
            event_endtime= datetime.datetime.now() + datetime.timedelta(hours=1),
            event_location= self.addy,
            event_public=True,
        )

        # Every person is a member of every group, but Joe admins Created Party,
        # Jim created Study, and Bob created Graduation
        GroupMember.objects.create(profile=self.joe,group=self.party, type='creator')
        GroupMember.objects.create(profile=self.jim,group=self.party, type='atendee')
        GroupMember.objects.create(profile=self.bob,group=self.party, type='atendee')


        GroupMember.objects.create(profile=self.joe,group=self.study, type='atendee')
        GroupMember.objects.create(profile=self.jim,group=self.study, type='creator')
        GroupMember.objects.create(profile=self.bob,group=self.study, type='atendee')

        GroupMember.objects.create(profile=self.joe,group=self.grad, type='atendee')
        GroupMember.objects.create(profile=self.jim,group=self.grad, type='atendee')
        GroupMember.objects.create(profile=self.bob,group=self.grad, type='creator')

    def test_getting_event_based_on_description(self):
        query = "study"
        desc_name_match = Event.objects.filter(Q(event_name__icontains=query)|Q(event_description__icontains=query))
        self.assertEqual(list(desc_name_match),[self.study])

    def test_getting_event_based_on_address(self):
        query = 'Main Street'
        address_match = Event.objects.filter(Q(event_location__street_number__icontains=query)|
        Q(event_location__city__icontains=query) |
        Q(event_location__street_name__icontains=query) |
        Q(event_location__zip_code__icontains=query) |
        Q(event_location__state__icontains=query))

        self.assertEqual(list(address_match),[self.party,self.study,self.grad])

    def test_not_getting_event_based_on_description(self):
        query = "random"
        desc_name_match = Event.objects.filter(Q(event_name__icontains=query)|Q(event_description__icontains=query))
        self.assertEqual(list(desc_name_match),[])
    
    def test_not_getting_event_based_on_address(self):
        query = 'Not a street'
        address_match = Event.objects.filter(Q(event_location__street_number__icontains=query)|
        Q(event_location__city__icontains=query) |
        Q(event_location__street_name__icontains=query) |
        Q(event_location__zip_code__icontains=query) |
        Q(event_location__state__icontains=query))

        self.assertEqual(list(address_match),[])

        
