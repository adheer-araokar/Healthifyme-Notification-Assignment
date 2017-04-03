from django.db import models
__author__ = 'aaraokar'


class AuthenticatedUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = 'users'


class Notifications(models.Model):
    header = models.CharField(max_length=150)
    content = models.CharField(max_length=300)
    image_url = models.URLField()

    class Meta:
        db_table = 'notifications'


class QueryNotificationMapping(models.Model):
    query = models.TextField()
    notification_id = models.ForeignKey(Notifications)
    timestamp = models.DateTimeField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'query_notification_mapping'
