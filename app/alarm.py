from flask import render_template, redirect
from app import app
from util_communication import slaveCall, slaveRead

from thread import start_new_thread
from datetime import datetime
import time

# config
irs = {
#   0: {"name": "Wohnzimmer", "slave": 0x04, "lastAlert": None}
}
SLAVE_CMD_ALARM = 10
SLAVE_CMD_ALARM_DIGITS = 1
READ_IRS_TIMEOUT = 4
alarmActivated = 0

@app.route("/alarm")
def alarm():
    data = {
        "irs": irs,
        "alarmActivated": alarmActivated
    }

    return render_template("alarm.html", **data)

@app.route("/alarm/state/<int:state>")
def alarm_set_state(state):
    global alarmActivated

    # activate/deactivate alarm
    alarmActivated = state
    # reset sensors if alarm has been deactivated
    if alarmActivated == 0:
        for ir_id in irs:
            irs[ir_id]["lastAlert"] = None

    return redirect("/alarm")

###### Job ######

"""
    Reads the sensor in continuous time intervals.

    timeout: defines the time interval
"""
def read_irs_loop(timeout):
    while True:
        if alarmActivated:
            for ir_id in irs:
                ir = irs[ir_id]
                # call slave for ir state
                slaveCall(ir["slave"], SLAVE_CMD_ALARM)
                # get result
                res = slaveRead(ir["slave"], SLAVE_CMD_ALARM_DIGITS)
                if res == "1":
                    ir["lastAlert"] = datetime.now()
        time.sleep(timeout)

# start job
start_new_thread(read_irs_loop, (READ_IRS_TIMEOUT,))
