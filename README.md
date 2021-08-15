# ESP Sphere
A Django app to manage, provide firmware files for ESP8266 and ESP32 based micro controllers

## Set up your microcontroller 

### ESP8266

[Official ESP8266 Arduino Documentation](https://arduino-esp8266.readthedocs.io/en/latest/ota_updates/readme.html#advanced-updater)

### ESP32 

The official EPS32 Arduino [documentation](https://docs.espressif.com/projects/arduino-esp32/en/latest/) has no entries as the ESP8266 about `httpUpdate`, but there is an [example for it](https://github.com/espressif/arduino-esp32/blob/master/libraries/HTTPUpdate/examples/httpUpdate/httpUpdate.ino#L74-L76).

## Start this Application local

Set the empty string `SECRET_KEY` in `settings.py` with an unique, unpredictable value.

Example:
```bash
tr -dc [:graph:] </dev/urandom |  head -c 50; echo
```
Checkout this repo to your favourite location path like `/var/www/` and make your app ready.

```bash
cd /path/to/your/app/dir
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser
```
 
### uWSGI and NGINX

Prepare your nginx installation and create a new vhost from the `esphere.conf` templete.
Afterards edit the systemd files to and copy them to `/etc/systemd/system`. Next reload the service files `systemd daemon-reload`.
If you wish to autostart the esphere service on boot `systemctl enable esphere.service`

Finally:
```bash
systemctl start esphere.service
systemctl restart nginx.service
```

### non-productive 

run the app with the build in django runserver command `./manage.py runserver`

