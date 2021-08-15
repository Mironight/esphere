from django import forms
from django.contrib import admin

from .models import ESP8266, ESP32, Firmware


class ESP32AdminForm(forms.ModelForm):
    class Meta:
        model = ESP32
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        choices = [(-1, 'No File')]
        for fw in Firmware.objects.filter(device_type=32):
            choices.append((fw.id, fw.file_name),)
        self.fields.get('firmware_file').choices = choices

    firmware_file = forms.ChoiceField(choices=[])


@admin.register(ESP32)
class ESP32Admin(admin.ModelAdmin):

    form = ESP32AdminForm

    list_display = ['device_name', 'mac_address', 'md5checksum', 'ip_address', 'auto_update', 'firmware_file']
    readonly_fields = ('mac_address', 'md5checksum', 'ip_address')


class ESP8266AdminForm(forms.ModelForm):
    class Meta:
        model = ESP8266
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [(-1, 'No File')]
        for fw in Firmware.objects.filter(device_type=8266):
            choices.append((fw.id, fw.file_name),)
        self.fields.get('firmware_file').choices = choices

    firmware_file = forms.ChoiceField(choices=[])


@admin.register(ESP8266)
class ESP8266Admin(admin.ModelAdmin):
    
    form = ESP8266AdminForm

    list_display = ['device_name', 'mac_address', 'md5checksum', 'ip_address', 'auto_update', 'firmware_file']
    readonly_fields = ('device_id', 'mac_address', 'md5checksum', 'ip_address')


@admin.register(Firmware)
class FirmwareAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_size', 'md5checksum']
    readonly_fields = ('file_size', 'md5checksum')
