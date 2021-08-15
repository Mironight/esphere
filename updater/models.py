import os
import hashlib

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file(value):
    if value.read()[0] != 0xE9:
        raise ValidationError(_('No ESP Firmware file'))

class Firmware(models.Model):

    DEVICE_LIST = [(8266, 'ESP8266'), (32, 'ESP32')]

    file_name = models.CharField(max_length=265)
    firmware_file = models.FileField(upload_to='files/firmware', unique=True, validators=[validate_file])
    file_size = models.IntegerField(editable=False)
    device_type = models.IntegerField(null=False, choices=DEVICE_LIST, default=0)
    md5checksum = models.CharField(max_length=32, editable=False)

    def ready(self):
        from updater.models import ESP32, ESP8266

    def __str__(self):
        return self.file_name

    def set_filesize(self):
        self.file_size = self.firmware_file.size

    def set_md5_checksum(self):
        self.firmware_file.seek(0)
        self.md5checksum = hashlib.md5(self.firmware_file.read()).hexdigest()

    def save(self, *args, **kwargs):
        self.set_filesize()
        self.set_md5_checksum()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.BASE_DIR, self.firmware_file.name))
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Firmware File'


class ESP8266(models.Model):

    device_name = models.CharField(max_length=512)
    firmware_file = models.IntegerField(default=-1)
    auto_update = models.BooleanField(default=False)
    
    device_id = models.IntegerField(editable=False)
    mac_address = models.CharField(default='00:00:00:00:00', max_length=20, editable=False)
    md5checksum = models.CharField(default='00000000000000000000000000000000', max_length=32, editable=False)
    ip_address = models.GenericIPAddressField(editable=False, default='0.0.0.0')

    def __str__(self):
        return self.device_name

    def save(self, *args, **kwargs):
        if not self.device_name:
            self.device_name = 'ESP8266-' + self.mac_address.replace(':', '')[6:]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'ESP8266 Device'

class ESP32(models.Model):

    device_name = models.CharField(max_length=512)
    firmware_file = models.IntegerField(default=-1)
    auto_update = models.BooleanField(default=False)
    
    mac_address = models.CharField(default='00:00:00:00:00', max_length=20, editable=False)
    md5checksum = models.CharField(default='00000000000000000000000000000000', max_length=32, editable=False)
    ip_address = models.GenericIPAddressField(editable=False, default='0.0.0.0')

    def __str__(self):
        
        return self.device_name

    def save(self, *args, **kwargs):
        if not self.device_name:
            self.device_name = 'ESP32-' + self.mac_address.replace(':', '')[6:]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'ESP32 Device'

