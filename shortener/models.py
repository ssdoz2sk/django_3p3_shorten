import json
from django.db import models

# Create your models here.
from account.models import ShortenUser
from django.conf import settings

host_url = settings.HOST_URL

if not host_url.endswith('/'):
    host_url += '/'

class Shorten(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField()
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=20, default='system')
    counter = models.IntegerField(default=0)
    create_user = models.ForeignKey(ShortenUser, on_delete=models.SET_NULL, default=None, null=True)
    creater_ip = models.CharField(max_length=100, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def short_url(self):
        return '{}{}'.format(host_url, self.code)

    def __str__(self):
        data = {
            'long_url': self.url,
            'short_url': self.short_url,
            'create_time': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
            'clicks': self.counter
        }
        return json.dumps(data)
