from bottle import route, run, template, static_file, request
import sys, os, io


var = dict()
var["light"] = "off"
var["page"] = "index.html"
var["switch_1"] = "false"
var["switch_2"] = "false"
var["switch_a"] = "false"
var["switch_b"] = "false"
var["light_1"] = 40
var["light_2"] = 80
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
    if os.path.isfile('/path/to/file'):
        pass

    html = template(var["page"] + ".html", **var)
    return html

@route('/<device>/<action>')
def hello(device, action):
    if device == "light":
        var["light"] = action

    return template(var["page"], **var)

@route('/receiver/<key>/<value>', method = 'POST')
def worker(key, value):
    #print(key, value, file=sys.stderr)
    var[key] = value


if __name__ == '__main__':   
    run(debug=True, reloader=True, port=5000)
