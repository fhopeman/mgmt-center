Mgmt-center
===

Mgmt-center is an open source project to make your home more intelligent. The main features are the management of temperature, humidity, light and alarm.

# Required Software

First of all, you have to install some additional software which is needed for the management center.

##### mysql

If you use static ip, please first install mysql client and then configure the static ip. After that, configure the ip as bind-address property in /etc/mysql/my.ini. Otherwise the mysql-server could not be started!

`sudo apt-get install mysql-server mysql-client`

##### mysql for flask

Flask is a lightweight python web framework which is a good choice for raspberry applications. Most of the additional software is loaded by [pip](https://pypi.python.org/pypi/pip) (`sudo apt-get install python-pip`).

`sudo pip install flask-sqlalchemy`

`sudo apt-get install libmysqlclient-dev`

`sudo pip install mysql-python`

#### Flask

There are several tutorials for flask available, e.g. [this](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) or [this](http://flask.pocoo.org).

`sudo pip install flask`

#### DHT

DHT is the first environment component which is used to feel your home. It's responsible for temperature and humidity.

`git clone https://github.com/adafruit/Adafruit_Python_DHT.git`

`cd Adafruit_Python_DHT`

`sudo apt-get upgrade`

`sudo apt-get install build-essential python-dev`

`sudo python setup.py install`

I have written a [script](https://github.com/fhopeman/mgmt-center/tree/master/scripts/readTempHumDHT22.py) for testing the DHT sensor.

#### DS18B20

The DS18B20 is an 1-wire temperature sensor. 1-wire has to be activated on your raspberry pi.

The file `/etc/modules` has to be appended with following content:

`w1-gpio pullup=1`

`w1-therm`

I have written a [script](https://github.com/fhopeman/mgmt-center/tree/master/scripts/readTempDS18B20.py) to test the sensor.

##### Wiring
If you have bought a standard sensor, the wiring is as follows:
Red -> Vdd; Black -> GND; White -> DQ
Wiring intern: Red -> GreenRed; White -> WhiteRed; Black -> White

## Development Setup

For convenience reasons I prefer to develop on my computer and push the current files to the raspberry as soon as possible. For that I mount the development folder from my computer to the raspberry. On the raspberry I start the sever with reload mode enabled. So a fresh server with all changes is guaranteed any time.

`sudo mount -t cifs -o username=NAME,password=PW //IP_ADDRESS/mgmt-center ~/mgmt-center_dev`

# Mgmt-center How to

### Jobs

There are several jobs which have to be executed. A first approach is to use cron based jobs by calling the action url. But then, the jobs aren't defined inside the tool itself and you have to synchronize the cron tab with the tool. A second approach (which I use) is to use thread based scheduling inside the mgmt-center code.

The thread based scheduling is active by default. The environment update and environment persisting is executed automatically. If you will use the cron based solution, please modify your code and disable the event loops.

### I2C Raspberry to Arduino Nano

The raspberry (master) is communicating with several arduino nanos (slaves). For that, the I2C protocol is used. The setup and some other thing are described below. To test your I2C connection, you can use [this](https://github.com/fhopeman/mgmt-center/tree/master/scripts/i2cCommandLine.py) script.

#### Setup

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

#### Wiring

pi(IO2) <-> nano(A4) <-> nano2(A4) <-> ..

pi(IO3) <-> nano(A5) <-> nano2(A5) <-> ..

pi(GND) <-> nano(GND) <-> nano2(GND) <-> ..

#### Protocol

CMD: 10 -> read ir sensor -> res: 0/1

CMD: 20 ... 29 -> toggle led with id (cmd - 20) -> res: 0/1

CMD: 3 -> refresh environment -> res: nothing

CMD: 30 ... 39 -> read environment with id (cmd - 30) -> res: -11.1:99.9 (temp and hum delemitted by :)
