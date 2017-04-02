from rest_framework import serializers
from Healthifyme_Notification_Assignment_REST_App.models import Notifications, QueryNotificationMapping, AuthenticatedUser


class AuthenticatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticatedUser
        fields = ('id', 'first_name', 'last_name')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('id', 'header', 'content', 'image_url')


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryNotificationMapping
        fields = ('id', 'query', 'notificationId', 'timestamp', 'status')
