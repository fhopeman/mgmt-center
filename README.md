# 1. Basic setup #
1. Wir laden zuerst das Raspbian Image von der offiziellen Webseite unter http://www.raspberrypi.org/downloads herunter. Nach dem Download muss die ZIP-Datei entpackt werden. In dieser befindet sich eine IMG-Datei, welche das Betriebssystem behinhaltet. Windows-Benutzer benötigen zum Überspielen des Images auf die SD-Karte das Tool Win32DiskImager in der Binary-Version (https://launchpad.net/win32-image-writer). Nach dem Download muss die ZIP-Datei entpackt werden. Benutzer mit Linux oder Mac OS X müssen sicherstellen, dass das Programm dd installiert ist.
2. 
- Windows: Öffne die soeben heruntergeladene Win32DiskImager.exe. Im Feld Image File muss man nun das heruntergelaene Raspbian Image einbinden. Im nebenstehenden Feld Device muss man den Laufwerksbuchstaben auswählen auf welches das Image Installiert werden soll. Wenn man sichergestellt hat, dass beide Angaben korrekt sind klickt man auf Write und das Image wird auf die SD-Karte geschrieben.
- Linux/Mac OS X: Zum Überspielen des Images macht man sich das Progrmm dd zu Nutze. In die Console gibt man folgenden Befehl ein. Dabei muss [IMG] durch den Pfad zum Image und [DEVICE] durch den Pfad zur SD-Karte ersetzt werden. Dieser Vorgang kann einige Minuten dauern.
		dd bs=1M if=[IMG] of=[DEVICE]
3. Stecke die SD-Karte nun in dein Raspberry Pi. Bevor du den Mini-USB-Stecker zur Stromversorgung ansteckst, stecke eine Tastatur via USB und einen Bildschirm via HDMI an.
4. Erststart von Raspberry Pi mit RaspbainNachdem (siehe Bild rechts) einige Initiierungen zum erstmaligen Start von Raspbian getätigt wurden kommt eine grau-blaue Oberfläche samt Menü, durch welche man sich mittels den Pfeiltasten, Enter und Escape auf der Tastur bewegen kann. In dieser werden nun einige Einstellungen durchgeführt.
5. Als erstes wählen wir den Punkt Expand Filesystem an, damit Raspbian den kompletten Speicherplatz auf der SD-Karte nutzt. Nach kurzer Zeit wird die Erweiterung bestätigt. Jedoch wird das Laufwerk erst beim nächsten Booten erweitert. Das kann, muss aber nicht, einige Zeit in Anspruch nehmen, in dem der Raspberry Pi nicht reagiert.
6. Nun wählen wir Internationalisation Options >> Change Keyboard Layout, damit wir eine deutsche Tastatur bekommen. Aus der Liste der Tastatur Modelle empfehle ich Classmate PC zu wählen. Daraufhin wird das Keyboad layout abgefragt, wo wir zuerst Other und darauf folgend German wählen um die Auswahlmöglichkeiten für Deutsch zu erhalten. Im Folgenden wählen wir German (ohne Zusätze). Nun werden primäre Tasten und sprachenspezifische Keyboard-Layout-Einstellungen abgefragt. Hierbei wählen wir The default for the keyboard layout. Bei der darauf folgenden Einstellung für kombinierte Tasten wählen wir No compose key. Nun wird gefrag, ob durch das Drücken von STRG + ALT + Entfernen der X server geschlossen werden soll. Ich empfehle No zu wählen.
7. Jetzt wählen wir im Menü Internationalisation Options >> Change Locale aus. In der Liste navigieren wir zu de_DE.UTF-8 UTF-8 und aktivieren diese Zeile mittels Leertaste. Anschließend klicken wir die Tab Taste und klicken auf Ok. Im Folgenden frägt das System, wie die korrekte Ausgabe von anderssprachigen Anwendungen gewährleistet werden soll. Dort wählen wir en_GB.UTF-8 zur systemweiten Sprache und bestätigen mittels Enter.
8. Darauffolgend zurück im Hauptmenü wählen wir Internationalisation Options >> Change Timezone und stellen hierbei die richtige Zeitzone ein. Bei mir wäre dies Europe und Berlin für Deutschland.
9. Zu guter Letzt wählen wir den Punkt Advanced Options >> SSH an, um den SSH-Dienst beim Start des Raspberry Pis automatisch starten zu lassen. Hierzu wählen wir Enable.
10. Alle die ihren Raspberry Pi, wie ich, am Router hängen haben und per SSH auf den Mini-Computer zugreifen möchten ziehen nun den Netzstecker und hängen den Raspberry Pi an ein LAN-Kabel, welches mit dem Router verbunden sein sollte. Diejenigen, die ihren Raspberry Pi mit HDMI betreiben möchten drücken auf Finish und werden aufgefordert den Raspberry Pi neuzustarten, dem wir zustimmen.
11. Nachdem der Raspberry Pi wieder gebootet ist aktualisieren wir den Raspberry Pi noch mittels folgender Eingabe in der Konsole. Der Standard-Benutzer hört auf den Namen pi und das Passwort lautet raspberry. Zuerst muss pi, darauf folgend raspberry eingegeben werden.
	sudo apt-get update && sudo apt-get upgrade


# 2. Software #

### General ###
`sudo apt-get remove --purge wolfram-engine`

`sudo apt-get install vim`

### mysql ###
Note: if you use static ip, please first install mysql client and then configure the static ip. After that, configure the ip as bind-address property in /etc/mysql/my.ini. Otherwise the mysql-server could not be started!

`sudo apt-get install mysql-server mysql-client`

`sudo apt-get install python-pip`

##### mysql for flask ##### 
`sudo pip install flask-sqlalchemy`

`sudo apt-get install libmysqlclient-dev`

`sudo pip install mysql-python`

### Flask ###
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world, http://flask.pocoo.org/

`sudo pip install flask`

### DHT ###
`git clone https://github.com/adafruit/Adafruit_Python_DHT.git`

`cd Adafruit_Python_DHT`

`sudo apt-get upgrade`

`sudo apt-get install build-essential python-dev`

`sudo python setup.py install`

### DS18B20 ###

Activate 1-wire on GPIO 4

`/etc/modules`

`w1-gpio pullup=1`

`w1-therm`

#### Wiring
Red -> Vdd; Black -> GND; White -> DQ
Wiring intern: Red -> GreenRed; White -> WhiteRed; Black -> White


# 3. Development folder #
`sudo mount -t cifs -o username=NAME,password=PW //IP_ADDRESS/mgmt-center ~/mgmt-center_dev`

# 4. WLAN #

### static wlan (/etc/network/interfaces) ###
auto wlan0

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet static
address 192.168.0.120
netmask 255.255.255.0
gateway 192.168.0.254
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp


### default wlan (/etc/network/interfaces) ###
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp

### default without wlan ###

auto lo eth0
iface lo inet loopback

iface eth0 inet dhcp

# 5. Mgmt-Center #

### Jobs ###

There are several jobs which have to be executed. A first approach is to use cron based jobs by calling the action url. But then, the jobs aren't defined inside the tool itself and you have to synchronize the cron tab with the tool. A second approach is to use thread based scheduling inside the mgmt-center code.

#### 1. Cron based config ####

##### Update environment values #####
`0 */3 * * * curl http://localhost/environment/update`

##### Persist current environment values #####
`0 */3 * * * curl http://localhost/environment/persist`

#### 2. Scheduling with threads ####
The thread based scheduling is active by default. The environment update and environment persisting is executed automatically. If you will use the cron based solution, please modify your code and disable the event loops.

# 6. I2C Raspberry to Arduino Nano #

### 6.1 Setup ###

Remove i2c from blacklist:
`$ cat /etc/modprobe.d/raspi-blacklist.conf`
`# blacklist spi and i2c by default (many users don't need them)`
`blacklist spi-bcm2708`
`#blacklist i2c-bcm2708`

Add this to the end of /etc/modules: 
`i2c-dev`

Install i2c tools and allow access to user pi:
`sudo apt-get install i2c-tools`
`sudo adduser pi i2c`

Then reboot and check the bus:
`i2cdetect -y 1`

Install python support:
`sudo apt-get install python-smbus`

### 6.2 Wiring ###

pi(IO2) <-> nano(A4) <-> nano2(A4) <-> ..
pi(IO3) <-> nano(A5) <-> nano2(A5) <-> ..
pi(GND) <-> nano(GND) <-> nano2(GND) <-> ..

### 6.3 Protocol ###
CMD: 10 -> read ir sensor -> res: 0/1
CMD: 20 ... 29 -> toggle led with id (cmd - 20) -> res: 0/1
CMD: 3 -> refresh environment -> res: nothing
CMD: 30 ... 39 -> read environment with id (cmd - 30) -> res: -11.1:99.9 (temp and hum delemitted by :)