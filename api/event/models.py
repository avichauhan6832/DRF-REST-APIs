from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):

    title = models.CharField(max_length=100, null=False)
    event_date = models.DateField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.IntegerField(default=100)
    registered_user = models.ManyToManyField(User, related_name='registered_user')
    invited_user = models.ManyToManyField(User, related_name='invited_user')
    public = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s %s %s %s %s' % \
               (self.title, self.event_date, self.author, self.limit, self.registered_user, self.invited_user)





