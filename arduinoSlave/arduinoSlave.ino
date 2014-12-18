#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>

// SLAVE CONFIG
#define SLAVE_ADDRESS 0x04
int index = 0;
int resSize = 0;
char res[12];

// ### ALARM CONFIG ###
#define PIN_ALARM 6

// ### LED CONFIG ###
#define PIN_LED_0 13
int state_led_0 = LOW;

// ### ENVIRONMENT CONFIG ###
#define PIN_DS18B20 2
#define PIN_DHT22   9
typedef struct ENV {
    float temp;
    float hum;
};
ENV env[2] = {{NULL, NULL}, {NULL, NULL}};

// init DS18B20
OneWire ourWire(PIN_DS18B20);
DallasTemperature ds18b20_wire(&ourWire);

// init DHT22
DHT dht_env_0(PIN_DHT22, DHT22);

void setup() {
    // start serial for output
    Serial.begin(9600);

    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveCmd);
    Wire.onRequest(sendRes);

    // alarm
    pinMode(PIN_ALARM, INPUT);

    // led
    pinMode(PIN_LED_0, OUTPUT);

    // DS18B20
    ds18b20_wire.begin();

    // DHT22
    dht_env_0.begin();

    Serial.println("started");
}

void loop() {
    Serial.println("refreshing");
    refreshEnvironment();
    delay(300000);
}

// callback for received data
void receiveCmd(int byteCount){
    while(Wire.available()) {
        int cmd = Wire.read();
        Serial.print("cmd: ");
        Serial.println(cmd);

        switch(cmd) {
            // read ir sensor and send 0/1 to master
            case 10:
                res[0] = readSensorIR() == HIGH ? '1' : '0';
                resSize = 1;
                break;
            // toggle led (each number (0 - 9) is one led)
            case 20 ... 29:
                res[0] = toggleLed(cmd - 20) == HIGH ? '1' : '0';
                resSize = 1;
                break;
            // refresh environment
            case 3:
                refreshEnvironment();
                break;
            // get values of environment
            case 30 ... 39:
                getEnvironment(cmd - 30, res);
                resSize = 10;
                break;
        }

     }
}

// callback for sending data
void sendRes() {
    Serial.print(res[index]);
    Wire.write(res[index++]);
    if (index >= resSize) {
        index = 0;
    }
}

int readSensorIR() {
    return digitalRead(PIN_ALARM);
}

int toggleLed(int led) {
    // select pin and state of led
    int pin = NULL;
    int *state = NULL;
    switch (led) {
        case 0:
            pin = PIN_LED_0;  
            state = &state_led_0;
    }

    // toggle specified led
    if (pin != NULL) {
        if (*state == LOW){
            *state = HIGH;
        }
        else{
            *state = LOW;
        }
        digitalWrite(pin, *state);
    }

    return *state;
}

void refreshEnvironment() {
    // env 0
    readDht22(dht_env_0, 0);
    // env 1
    readDS18B20(1);
}

void readDS18B20(int env_id) {
    ds18b20_wire.requestTemperatures();
    env[env_id].temp = ds18b20_wire.getTempCByIndex(0);
    Serial.print("env_");
    Serial.print(env_id);
    Serial.print(":");
    Serial.println(env[env_id].temp);
}

void readDht22(DHT dht, int env_id) {
    // refresh values of dht
    dht.readTemperature();
    dht.readHumidity();
    delay(2000);
    // read values of dht
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (isnan(h) || isnan(t)) {
        Serial.println("could not read dht22");
    }
    else {
        Serial.print("env_");
        Serial.print(env_id);
        Serial.print(":");
        Serial.print(t);
        Serial.print(":"); 
        Serial.println(h);
        env[env_id].temp = t;
        env[env_id].hum = h;
    }
}

void getEnvironment(int env_id, char res[]) {
    float temp = env[env_id].temp;
    float hum = env[env_id].hum;

    dtostrf(temp, 3, 1, res);
    int humPos = 5;
    // one character more because of negative sign
    if (temp < 0) {
        humPos = 6;
    }
    res[humPos - 1] = ':';
    // set accuracy to 3, then all positions of res are placed
    dtostrf(hum, 3, 3, res + humPos);
}

