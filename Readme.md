# Healthifyme-Notification-Assignment

Readme for Notification Applications.

There are 2 applications in this project, one for backend which exposes the REST APIs, and one for the UI Frontend which consumes the Backend REST APIs.

Since the port of the rest calls is hardcoded in the frontend application, the backend application needs to run on 127.0.0.1:8000

Multiple python packages are used for thie project which will be required to be installed on the machine on which you need to run the applications.

Primarily, Python 3.6.1 has been used with the following packages :-
	Django
	djangorestframework
	apscheduler
	django-cors-headers

The UI is self explanatory, there are 3 radio buttons which give you the possible options of inputs and based on the one you select, the input text boxes will be visible.

Once you click on the Submit button, in order to simulate the send notification, I print out the List of Ids and Notification_Payload to the console of the backend app. Please monitor its console to verify that the scheduled task gets executed on its scheduled time.

If you select the Add Notification Only choice, Once you click submit, it will output the Notification Id below the Submit button which you can use when Creating a query against the notification.
Similarly, you will also get the Query Id when you choose Add Query Only or when you select Add Both.

The requirement of the Notification to be sent AFTER 2 hours has been changed to a minimum tile delay of 10 seconds for testing purposes.

When Creating Both Notification and Query form the UI, in case the Query creation fails due to invalid timestamp, the Notification is still created and its ID is returned. You can further use this ID to just create a query since the notification already exists.

Since I have a windows system and I could not find a working MySQL connector with Python 3.6.1, I'm using SQLite3.
