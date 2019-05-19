from bottle import route, run, template, static_file, request
import sys, os, io
import subprocess


var = dict()
var["light"] = "off"
var["page"] = "index.html"
var["switch_1"] = "false"
var["switch_2"] = "false"
var["switch_a"] = "false"
var["switch_b"] = "false"
var["light_0"] = 40
var["light_1"] = 40
var["light_2"] = 80
var["color_0"] = "e66465"
var["color_1"] = "e66465"
var["color_2"] = "e66465"

@route("/favicon.ico")
def icon():
    return static_file("favicon.ico", root='static')

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')

@route('/static/css/<filename>')
def server_static_css(filename):
    return static_file(filename, root='static/css')

@route('/')
def index():
	return template(var["page"], **var)

@route('/<page>')
def switch(page):
    var["page"] = page

    if page == "weather":
        try:
            #var["temperature"] = command("/etc/openhab2/scripts/weatherstation.py temperature")
            with open("/sys/bus/w1/devices/28-8000002b2904/w1_slave") as file:
                var["temperature"] = float(file.readlines()[1].split("=")[1]) / 1000
        except:
            var["temperature"] = "ERROR"
            pass

        try:
            var["humidity"] = command("/etc/openhab2/scripts/weatherstation.py humidity")
        except:
            var["humidity"] = "ERROR"
        

    return template(var["page"] + ".html", **var)

@route('/<device>/<action>')
def hello(device, action):
    if device == "light":
        var["light"] = action

    return template(var["page"], **var)

@route('/receiver/<key>/<value>', method = 'POST')
def worker(key, value):
    #print(key, value, file=sys.stderr)
    var[key] = value

    if key == "infrarot":
        os.system("irsend SEND_ONCE PioneerAVR " + value)
    elif key == "light":
        x = value.split("-")
        pins = x[0].split(",")
        value = x[1]
        red, green, blue = hex_to_rgb(value)
        
        os.system("pigs p " + pins[0] + " " + str(red))
        os.system("pigs p " + pins[1] + " " + str(green))
        os.system("pigs p " + pins[2] + " " + str(blue))
    elif key == "switch":
        x = value.split("-")
        key = x[0]
        value = "ON" if x[1] == "true" else "OFF"
        
        os.system("/opt/433Utils/RPi_utils/run.sh " + key + " " + value)



def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def command(cmd):
    out = subprocess.Popen(cmd.split(" "), 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    return stdout.split()[0]


if __name__ == '__main__':   
    #run(debug=True, reloader=True, port=5000)
    run(host="192.168.1.68", debug=True, reloader=True, port=5000)
