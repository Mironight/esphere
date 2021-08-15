import os
import hashlib
import ipaddress

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotModified, FileResponse

from .models import ESP8266, ESP32, Firmware

def updater(request):

    #
    #  ESP8266 Devices
    #
    if request.headers['User-Agent'] == 'ESP8266-http-Update':
        remote_ip = request.headers["X-Real-IP"]
        try:
            device = ESP8266.objects.get(mac_address=request.headers["x-ESP8266-STA-MAC"])
            device.md5checksum = request.headers["x-ESP8266-sketch-md5"]
            device.ip_address = remote_ip
        except (KeyError, ESP8266.DoesNotExist) as e:
            device = ESP8266(
                mac_address=request.headers["x-ESP8266-STA-MAC"],
                md5checksum=request.headers["x-ESP8266-sketch-md5"],
                device_id=request.headers["x-ESP8266-Chip-ID"],
                ip_address=remote_ip,
            )
        finally:
            device.save()

        try:
            fw = Firmware.objects.get(id=device.firmware_file)
            
            # serve firmware file
            if fw.md5checksum != request.headers["x-ESP8266-sketch-md5"] and device.auto_update:
                fwfile = open(fw.firmware_file.name, 'rb')
                resp = FileResponse(fwfile)
                resp['Content-Length'] = fw.file_size
                return resp
            else:
                return HttpResponseNotModified()
        except Firmware.DoesNotExist as e:
            return HttpResponseNotModified()

    #
    #  ESP32 Devices
    #
    if request.headers['User-Agent'] == 'ESP32-http-Update':
        remote_ip = request.META.get("REMOTE_ADDR")
        try:
            device = ESP32.objects.get(mac_address=request.headers["X-Esp32-Sta-Mac"])
            device.md5checksum = request.headers["X-Esp32-Sketch-Md5"]
            device.ip_address = remote_ip
        except (KeyError, ESP32.DoesNotExist) as e:
            device = ESP32(
                mac_address=request.headers["X-Esp32-Sta-Mac"],
                md5checksum=request.headers["X-Esp32-Sketch-Md5"],
                ip_address=remote_ip,
            )
        finally:
            device.save()
        
        try:
            fw = Firmware.objects.get(id=device.firmware_file)

            # serve firmware file
            if fw.md5checksum != request.headers["X-Esp32-Sketch-Md5"] and device.auto_update:
                fwfile = open(fw.firmware_file.name, 'rb')
                resp = FileResponse(fwfile)
                resp['Content-Length'] = fw.file_size
                return resp
            else:
                return HttpResponseNotModified()

        except Firmware.DoesNotExist as e:
            return HttpResponseNotModified()

    else:
        return HttpResponse("No OTA Update for your device")
