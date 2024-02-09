from django.db import models
from django.contrib.postgres.fields import ArrayField

class userinfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=50)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'userinfo'
    
    def __str__(self):
        return self.email  # Replace with a meaningful representation

class userteams(models.Model):
    user = models.ForeignKey(userinfo, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, max_length=50)
    followedteams = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    followplayers = ArrayField(models.CharField(max_length=100), blank=True, default=list)

    class Meta:
        db_table = "userteams"

    def __str__(self):
        return self.user