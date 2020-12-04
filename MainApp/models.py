# /***************************************************************************************
# *  REFERENCES
# *  Title: django-multiselectfield
# *  Author: Pablo Martin
# *  Date Published: Feb 20, 2020
# *  Date Accessed: October 5th, 2020
# *  Code version: 0.1.12
# *  URL: https://pypi.org/project/django-multiselectfield/
# *  Software License: LGPL
# *
# *  Title: Extending Django User Model (UserProfile) like a Pro
# *  Author: KhoPhi
# *  Date Published: N/A, about 4 years ago
# *  Date Accessed: October 21st, 2020
# *  Code version: N/A, Blog post
# *  URL: https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/
# *  Software License: None
# *
# *  Title: models.py
# *  Author: jacobian (GitHub Name)
# *  Date Published: Feb 15th, 2011
# *  Date Accessed: October 20th, 2020
# *  Code version: first and only version
# *  URL: https://gist.github.com/jacobian/827937
# *  Software License: None
# *
# *  Title: pytz
# *  Author: Stuart Bishop
# *  Date Published: Nov 2, 2020
# *  Date Accessed: October 16th, 2020
# *  Code version: 2020.4
# *  URL: https://pypi.org/project/pytz/#description
# *  Software License: MIT License (MIT)
# *
# ***************************************************************************************/

from django.db import models
# may or may not work for tag list
from django.db.models import CharField, Model 
from django_mysql.models import ListCharField
import datetime

# User includes for automatic updates
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# inlcude for timezone check
from pytz import timezone
import pytz

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='No Name')
    groups = models.ManyToManyField('Event',through='GroupMember',related_name='people')
    
    # can include more information later

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user,name=user.username)
        user_profile.save()
post_save.connect(create_profile, sender=User)





class Address(models.Model):

    street_number = models.CharField("Address line 1", max_length=1024, blank=True)

    street_name = models.CharField("Address line 2", max_length=1024, blank=True)

    city = models.CharField("City", max_length=1024, blank=True)

    state = models.CharField("State", max_length=2, blank=True)

    zip_code = models.CharField("ZIP / Postal code",max_length=5, blank=True)


    def __str__(self):
        return (self.street_number + " " + self.street_name)


class Event(models.Model):

    # all of the different attribute
    event_name = models.CharField(max_length=100)
    event_description = models.CharField(max_length=500)
    event_date = models.DateTimeField('date and start time', blank=True, null=True)
    event_location = models.ForeignKey(Address,on_delete= models.CASCADE, null=True, blank=True)
    event_duration = models.IntegerField(default=1)
    # added in the end time which might replace the duration thing
    event_endtime = models.DateTimeField(null=True, blank=True)
    event_capacity = models.IntegerField(default=10)
    event_public = models.BooleanField(default=True)
    
    

    # Event_tags is a list of CharFields with a max length of 20 chars and the list of tags can be no more than 10
    # max_length=(10 * 21) represents the total storage for the tags, their names followed by a comma
    #
    # HTML will deal with adding in tags when requesting for event information using a drop down menu
    event_tags = ListCharField(base_field=models.CharField(max_length=20), size=10, max_length=(10 * 21))
    
    #event_tags = MultiSelectField(choices=tags)


    def is_finished(self):
        # getting UTC timezone for comparison
        utc = pytz.UTC

        # gets the end time which is already in UTC
        end_time = self.event_endtime
        
        # get the current time in utc
        now = datetime.datetime.utcnow()
        
        # need to make it an aware datetime field
        now = now.replace(tzinfo=utc)

        if( now <= end_time):
            return False
        else:
            return True

    # Lets you know if an event is public or not
    def is_public(self):
        return self.event_public

    # Tells you if an event is at capacity or not
    def at_capacity(self):
        if(self.event_capacity > 0):
            return False
        else:
            return True


    

    def __str__(self):
        return self.event_name


class GroupMember(models.Model):
    # added on_delete.CASCADE, but idk if that is right
    profile = models.ForeignKey(Profile, related_name='membership', on_delete=models.CASCADE)
    group = models.ForeignKey(Event, related_name='membership', on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    
    def __unicode__(self):
        return "%s is in group %s (as %s)" % (self.profile, self.group, self.type)