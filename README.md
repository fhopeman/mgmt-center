mgmt-center
===

## Required Software

#### General
`sudo apt-get remove --purge wolfram-engine`

`sudo apt-get install vim`

##### mysql
Note: if you use static ip, please first install mysql client and then configure the static ip. After that, configure the ip as bind-address property in /etc/mysql/my.ini. Otherwise the mysql-server could not be started!

`sudo apt-get install mysql-server mysql-client`

`sudo apt-get install python-pip`

##### mysql for flask
`sudo pip install flask-sqlalchemy`
`sudo apt-get install libmysqlclient-dev`
`sudo pip install mysql-python`

#### Flask
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world, http://flask.pocoo.org/

`sudo pip install flask`

#### DHT
`git clone https://github.com/adafruit/Adafruit_Python_DHT.git`
`cd Adafruit_Python_DHT`
`sudo apt-get upgrade`
`sudo apt-get install build-essential python-dev`
`sudo python setup.py install`

#### DS18B20

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
