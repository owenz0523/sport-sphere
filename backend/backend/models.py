from django.db import models

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