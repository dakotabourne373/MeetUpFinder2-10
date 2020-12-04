# meetupfinder-2-10

    This application is used as a way for users to create, see, and rsvp for events in their local area. Each user is asked to log in using thier google account (google authorization) before creating events, rsvping for events, or seeing their profile. Once the user has been logged in, they then have the ability to create events, rsvp for events on the webpage, and view their profile. All events contain details on what the event is called, the time it starts, the time it ends, the description, and the address of the location. The database only keeps upcoming events, current events, and ones that have expired within the past 24 hours.


# Deploying and Installation

    First, use a virtual environment of your choice! If you need help with setting that up, trying looking at [this page][1]
    [1] https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

    Next install the files in the requirements using the following command:
    `pip install -r requirements.txt`

    Next, you can then either run this application on a local server using 'py manage.py runserver' or by deploying the application to Heroku. Once this has been done, you are free to use the app as much as you would like!



# Usage

    Profile -
    
    In order to see thier profile, users must go to the "login" page and sign in to their google account. Once this is done, they can go to the profile page and see their created events and also RSVPed events. If you wish to sign into a differnt account, go to the "login" page again and click "sign out" and then you will be able to log in under another google account.

    Events - 
    
    Events can be created by going to the "Create Event" tab and then inputting information in the event form. All of the fields are required in order to create an event. There is a google autocomplete box located at the bottom of the page for the address. Be sure that the google auto complete puts in all of the typed information for the address

    RSVP - 
    
    When you create an event, you are assigned as the "creator" of the event and have the ability to "delete" that event you created. However, if you are not the creator you have the ability to sign up as an "attendee". To do this, click on the event tab box located on the page which will redirect you to the event details. From there, you can click the green "RSVP" button to register the event. To see this event, you can click on your profile and it should be located under "RSVPed events". To UnRSVP, you can just click on the event again and then click the red "UnRSVP" button at the bottom of the page.

    Searching - 
    
    You can search for events by typing text into the search bar located in the navigation bar. The inputted text will be searched through all of the events descriptions, names, and addresses. These will be divided into two separate sections, one named "Matching Name or Description" or "Matching Address", and if no results were found each of these sections will have text displayed that nothing was found.

# Contributions and Suggestions

    We are all new developers and would really appreciate advice on how we can make this application better! If you have any bug reports, fixes, or other things that we can improve, just submit them to the github issue tracker.

# Resources used

    All resources used to create this application are cited at the top of the respective page where the code/algorithim/idea was used. Additionally, Django documentation was used for all of the pages since this is the main framework used to construct this application. The citation for Django is located at the top of the "settings.py" file. Bootstrap was also used for a majority of the HTML files, and is cited at the top of each HTML file. Lastly, Google API's were also integrated (maps and auto complete address) into the system and are also cited at the top of each page where they are used.


# Licensing
    This Library is BSD-licensed
