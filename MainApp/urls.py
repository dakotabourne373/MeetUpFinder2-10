from django.urls import path

from . import views

urlpatterns = [
    # Has the URL pattern MeetUpFinder/login/
    path('login/', views.login, name='login'),
    # Has the URL pattern MeetUpFinder/
    path('', views.mainpage, name='mainpage'),
    #  Has the URL pattern MeetUpFinder/eventForm/
    path('eventForm/',views.eventForm, name='event_form'),
    # Has the URL pattern MeetUpFinder/create_event
    path('create_event/',views.createEvent, name='create_event'),
    # Has the URL pattern MeetUpFinder/*some number/details/
    path('<int:event_id>/details/',views.event_detail_view, name='event_detail_view'),
    
    # Has the URL pattern MeetUpfinder/search/
    path('search/',views.eventSearchResults, name='event_search'),

    # Has the URL patter MeetUpfinder/profile/
    path('profile/',views.profile_view, name='profile_view'),

    path('<int:event_id>/rsvp/',views.rsvp_event, name='rsvp_view'),

    # Has the URL pattern MeetUpFinder/login/
    path('logout/', views.Logout, name='logout'),

]