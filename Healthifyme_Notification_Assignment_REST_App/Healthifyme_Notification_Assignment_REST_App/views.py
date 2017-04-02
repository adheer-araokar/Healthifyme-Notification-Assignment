__author__ = 'aaraokar'
from Healthifyme_Notification_Assignment_REST_App.models import Notifications, QueryNotificationMapping, AuthenticatedUser
from Healthifyme_Notification_Assignment_REST_App.serializers import NotificationSerializer, QuerySerializer, AuthenticatedUserSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time


class NotificationView(APIView):
    """
    API endpoint that allows Notifications to be viewed or edited.
    """
    content_type = 'application/json'
    valid_image_formats = ['png', 'jpg', 'jpeg']
    def get(self, request, num):
        notification = Notifications.objects.filter(id = int(num))
        serializedNotification = NotificationSerializer(notification, many = True)
        return Response(serializedNotification.data, content_type=self.content_type)

    def post(self, request):
        print(request.data)
        if(len(request.data['header']) < 20 or len(request.data['header']) > 150
           or len(request.data['content']) < 20 or len(request.data['content']) > 300
           or not self.validateImageURL(request.data['image_url'])):
            return Response("Bad Request! Please check the parameter constraints.", status=status.HTTP_400_BAD_REQUEST)
        serializedNotification = NotificationSerializer(data=request.data)
        if serializedNotification.is_valid():
            serializedNotification.save()
        else:
            return Response(serializedNotification.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'id': serializedNotification.data.get('id')})

    def validateImageURL(self, image_url):
        if image_url.split('.')[-1] not in self.valid_image_formats:
            return False
        else:
            return True


class QueryView(APIView):
    """
    API endpoint that allows Query_Notification_Mappings to be viewed or edited.
    """
    content_type = 'application/json'
    def get(self, request, num):
        query = QueryNotificationMapping.objects.filter(id = int(num))
        serializedQuery = QuerySerializer(query, many = True)
        return Response(serializedQuery.data, content_type=self.content_type)

    def post(self, request):
        serializedQuery = QuerySerializer(data=request.data)
        if serializedQuery.is_valid():
            if not request.data.get('id'):
                validTSF = self.validateTimestampFormat(request.data['timestamp'])
                if validTSF:
                    validTS = self.validateTimestamp(request.data['timestamp'])
                    if validTS:
                        serializedQuery.save()
                        self.scheduleTask(serializedQuery.data.get('id'), request.data['timestamp'])
                    else:
                        return Response("Invalid Timestamp. The timestamp should be atleast 10 Seconds post the current time.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Invalid Timestamp Format.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializedQuery.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'id': serializedQuery.data.get('id')})

    def validateTimestampFormat(self, timestamp):
        # Timestamp needs to be of the format :- '2009-11-06 16:30:05'
        try:
            datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    def validateTimestamp(self, timestamp):
        inputDate = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        inputTimeSeconds = time.mktime(inputDate.timetuple())
        currentTimeSeconds = time.time()
        #if((inputTimeSeconds - currentTimeSeconds) < 7200):
        if((inputTimeSeconds - currentTimeSeconds) < 10):
            return False
        else:
            return True

    def scheduleTask(self, id, timestamp):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.call_send_notification, 'date', run_date=timestamp, args=[id])
        scheduler.start()

    def call_send_notification(self, qnId):
        print(qnId)
        query = QueryNotificationMapping.objects.filter(id = int(qnId))
        serializedQuery = QuerySerializer(query, many = True)
        userQuery = serializedQuery.data[0].get('query')
        list_ids = ""
        for user in AuthenticatedUser.objects.raw(userQuery):
            list_ids = list_ids + str(user.id) + ", "
        if list_ids:
            list_ids = list_ids[:-2]
            nId = serializedQuery.data[0].get('notificationId')
            notification = Notifications.objects.filter(id = int(nId))
            serializedNotification = NotificationSerializer(notification, many = True)
            payload = {}
            payload['header'] = serializedNotification.data[0].get('header')
            payload['content'] = serializedNotification.data[0].get('content')
            payload['image_url'] = serializedNotification.data[0].get('image_url')
            result_json = {}
            result_json['ids'] = list_ids
            result_json['notification_payload'] = payload
            print('current time :- '+str(datetime.now()))
            print('db timestamp :- '+str(serializedQuery.data[0].get('timestamp')))
            print('resultant payload :- '+str(result_json))
            queryId = serializedQuery.data[0]['id']
            qnmObject = QueryNotificationMapping.objects.get(id = int(queryId))
            qnmObject.status = self.send_notification(list_ids, payload)
            qnmObject.save()

    def send_notification(self, list_of_ids, notification_payload):
        return True


class AuthenticatedUserView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    content_type = 'application/json'
    def get(self, request, num):
        user = AuthenticatedUser.objects.filter(id = int(num))
        serializedUser = AuthenticatedUserSerializer(user, many = True)
        return Response(serializedUser.data, content_type=self.content_type)

    def post(self, request):
        serializedUser = AuthenticatedUserSerializer(data=request.data)
        if serializedUser.is_valid():
            serializedUser.save()
        else:
            return Response(serializedUser.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'id': serializedUser.data.get('id')})

