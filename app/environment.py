from flask import render_template
from app import app, db
from util_communication import slaveCall, slaveRead

import time
from datetime import datetime
from thread import start_new_thread

# config
rooms = {
    0: {"name": "living room", "slave": 0x04, "sensor": 0, "currentTemp": None, "currentHum": None, "history": list()},
    1: {"name": "balcony", "slave": 0x04, "sensor": 1, "currentTemp": None, "currentHum": None, "history": list()}
}
SLAVE_CMD_ENVIRONMENT_START = 30
SLAVE_CMD_ENVIRONMENT_DIGITS = 10
CACHED_HISTORY_ELEMENTS = 10
READ_ENVIRONMENT_TIMEOUT = 1800
PERSIST_ENVIRONMENT_START_DELAY = 60
PERSIST_ENVIRONMENT_TIMEOUT = 10800

# define database model
class Environment(db.Model):
    __tablename__ = 'environment'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime)
    room_id = db.Column(db.SmallInteger)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)

    def __init__(self, date, room_id, temperature, humidity):
        self.date = date
        self.room_id = room_id
        self.temperature = temperature
        self.humidity = humidity

"""
    Loads the environment view.
"""
@app.route("/")
@app.route("/environment")
def environment():
    data = {
        "rooms": rooms
    }

    return render_template("environment.html", **data)

"""
    Updates all rooms with a fresh environment measurement.
"""
@app.route("/environment/update")
def environment_update_rooms():
    for room_id in rooms:
        room = rooms[room_id]
        try:
            tmpTemp, tmpHum = read_environment(room)
        except Exception as e:
            app.logger.error("'%s' while reading environment of '%s'", e, room["name"])

        if (tmpTemp):
            room["currentTemp"] = round(tmpTemp, 1)
        if tmpHum:
            room["currentHum"] = round(tmpHum, 1)

    return "success"

"""
    Persists the latest room environment measurement
    for each room.
"""
@app.route("/environment/persist")
def environment_persist_rooms():
    current_time = datetime.now();
    # persist each room environment in database
    for room_id in rooms:
        room = rooms[room_id]
        temp = room["currentTemp"];
        hum = room["currentHum"];
        db.session.add(Environment(current_time, room_id, temp, hum))
        # update room history cache
        history = room["history"];
        if len(history) >= CACHED_HISTORY_ELEMENTS:
            history.pop(0)
        history.append((current_time, temp, hum))
    db.session.commit()

    return "success"

"""
    Reads the current temperature and humidity of the definied room.
    Checks if the humidity isn't 0, because some sensors doesn't
    provide a humidity value.
"""
def read_environment(room):
    # call slave
    slaveCall(room["slave"], SLAVE_CMD_ENVIRONMENT_START + room["sensor"])
    # get response
    res = slaveRead(room["slave"], SLAVE_CMD_ENVIRONMENT_DIGITS).split(":")
    # transform response
    temp = float(res[0])
    hum = float(res[1])
    if (hum == 0):
        hum = None

    return temp, hum

###### Jobs ######

"""
    Reads the environment sensors in continuous time intervals.

    timeout: defines the execution interval
"""
def read_environment_loop(timeout):
    while True:
        environment_update_rooms()
        time.sleep(timeout)

"""
    Persist the current environment values in continuous time intervals.

    timeout: defines the execution interval
"""
def persist_environment_loop(timeout):
    time.sleep(PERSIST_ENVIRONMENT_START_DELAY)
    while True:
        environment_persist_rooms()
        time.sleep(timeout)

# start jobs
start_new_thread(read_environment_loop, (READ_ENVIRONMENT_TIMEOUT,))
start_new_thread(persist_environment_loop, (PERSIST_ENVIRONMENT_TIMEOUT,))
