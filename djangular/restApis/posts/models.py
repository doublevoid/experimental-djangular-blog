from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
   
    def publish(self, isPublished):
        if isPublished == False:
            self.published_date = None
        else:
            self.published_date = timezone.now()