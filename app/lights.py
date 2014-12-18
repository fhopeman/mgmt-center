from flask import render_template
from app import app
from util_communication import slaveCall, slaveRead

# define lights (id is gpio pin)
lights = {
     0: {"name": "Wohnzimmer TV", "slave": 0x04, "id": 0, "state": 0}
#   ,1: {"name": "Wohnzimmer Regal", "slave": 0x06, "id": 0, "state": 0}
}
SLAVE_CMD_LIGHT_START = 20
SLAVE_CMD_LIGHT_DIGITS = 1

@app.route("/light")
def light():
    data = {
        "lights": lights
    }

    return render_template("light.html", **data)

@app.route("/light/<int:light>/<int:state>", methods=["POST"])
def change_light_state(light, state):
    light = lights[light]
    # change the state if it has changed
    if state != light["state"]:
        # change light state
        slaveCall(light["slave"], SLAVE_CMD_LIGHT_START + light["id"])
        # change global state dict
        light["state"] = int(slaveRead(light["slave"], SLAVE_CMD_LIGHT_DIGITS));
    else:
        print("no light changes")

    return "success"
