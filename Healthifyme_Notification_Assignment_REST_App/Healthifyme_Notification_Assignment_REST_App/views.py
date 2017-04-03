import time
from Healthifyme_Notification_Assignment_REST_App.models import Notifications
from Healthifyme_Notification_Assignment_REST_App.models import QueryNotificationMapping
from Healthifyme_Notification_Assignment_REST_App.models import AuthenticatedUser
from Healthifyme_Notification_Assignment_REST_App.serializers import NotificationSerializer
from Healthifyme_Notification_Assignment_REST_App.serializers import QuerySerializer
from Healthifyme_Notification_Assignment_REST_App.serializers import AuthenticatedUserSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
__author__ = 'aaraokar'


class NotificationView(APIView):
    """
    API endpoint that allows Notifications to be viewed or edited.
    """
    content_type = 'application/json'
    valid_image_formats = ['png', 'jpg', 'jpeg']

    def get(self, request, num):
        notification = Notifications.objects.filter(id=int(num))
        serialized_notification = NotificationSerializer(notification, many=True)
        return Response(serialized_notification.data, content_type=self.content_type)

    def post(self, request):
        print(request.data)
        if(len(request.data['header']) < 20 or len(request.data['header']) > 150 or
                len(request.data['content']) < 20 or len(request.data['content']) > 300 or
                not self.validate_image_url(request.data['image_url'])):
            return Response("Bad Request! Please check the parameter constraints.", status=status.HTTP_400_BAD_REQUEST)
        serialized_notification = NotificationSerializer(data=request.data)
        if serialized_notification.is_valid():
            serialized_notification.save()
        else:
            return Response(serialized_notification.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'id': serialized_notification.data.get('id')})

    def validate_image_url(self, image_url):
        if image_url.split('.')[-1] not in self.valid_image_formats:
            return False
        return True


class QueryView(APIView):
    """
    API endpoint that allows Query_Notification_Mappings to be viewed or edited.
    """
    content_type = 'application/json'

    def get(self, request, num):
        query = QueryNotificationMapping.objects.filter(id=int(num))
        serialized_query = QuerySerializer(query, many=True)
        return Response(serialized_query.data, content_type=self.content_type)

    def post(self, request):
        serialized_query = QuerySerializer(data=request.data)
        if not serialized_query.is_valid():
            return Response(serialized_query.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('id'):
            return JsonResponse({'id': serialized_query.data.get('id'), 'query': serialized_query.data.get('query')})
        valid_timestamp_format = self.validate_timestamp_format_check(request.data['timestamp'])
        if not valid_timestamp_format:
            return Response("Invalid Timestamp Format.", status=status.HTTP_400_BAD_REQUEST)
        valid_timestamp = self.validate_timestamp_check(request.data['timestamp'])
        if not valid_timestamp:
            return Response("Invalid Timestamp. The timestamp should be at least 10 Seconds post the current time.",
                            status=status.HTTP_400_BAD_REQUEST)
        serialized_query.save()
        self.schedule_task(serialized_query.data.get('id'), request.data['timestamp'])
        return JsonResponse({'id': serialized_query.data.get('id')})

    @staticmethod
    def validate_timestamp_format_check(timestamp):
        # Timestamp needs to be of the format :- '2009-11-06 16:30:05'
        try:
            datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_timestamp_check(timestamp):
        input_date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        input_time_in_seconds = time.mktime(input_date.timetuple())
        current_time_in_seconds = time.time()
        # if(input_time_in_seconds - current_time_in_seconds) < 7200:
        if(input_time_in_seconds - current_time_in_seconds) < 10:
            return False
        return True

    def schedule_task(self, query_notification_mapping_id, timestamp):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.call_send_notification, 'date', run_date=timestamp, args=[query_notification_mapping_id])
        scheduler.start()

    def call_send_notification(self, query_notification_mapping_id):
        print(query_notification_mapping_id)
        query = QueryNotificationMapping.objects.filter(id=int(query_notification_mapping_id))
        serialized_query = QuerySerializer(query, many=True)
        user_query = serialized_query.data[0].get('query')
        list_ids = ""
        for user in AuthenticatedUser.objects.raw(user_query):
            list_ids = list_ids + str(user.id) + ", "
        if not list_ids:
            return
        list_ids = list_ids[:-2]
        notification_id = serialized_query.data[0].get('notification_id')
        notification = Notifications.objects.filter(id=int(notification_id))
        serialized_notification = NotificationSerializer(notification, many=True)
        payload = {
            'header': serialized_notification.data[0].get('header'),
            'content': serialized_notification.data[0].get('content'),
            'image_url': serialized_notification.data[0].get('image_url')
        }
        result_json = {
            'ids': list_ids,
            'notification_payload': payload
        }
        print('current time :- '+str(datetime.now()))
        print('db timestamp :- '+str(serialized_query.data[0].get('timestamp')))
        print('resultant payload :- '+str(result_json))
        query_id = serialized_query.data[0]['id']
        qnm_object = QueryNotificationMapping.objects.get(id=int(query_id))
        qnm_object.status = self.send_notification(list_ids, payload)
        qnm_object.save()

    @staticmethod
    def send_notification(list_of_ids, notification_payload):
        return True


class AuthenticatedUserView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    content_type = 'application/json'

    def get(self, request, num):
        user = AuthenticatedUser.objects.filter(id=int(num))
        serialized_user = AuthenticatedUserSerializer(user, many=True)
        return Response(serialized_user.data, content_type=self.content_type)

    def post(self, request):
        serialized_user = AuthenticatedUserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
        else:
            return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'id': serialized_user.data.get('id')})

