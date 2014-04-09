#!/usr/bin/env python
import sys, os, signal, time
from bottle import route, run, static_file, template, view, post, get, error, SimpleTemplate
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import datetime as dt
import gevent
from modules.HardwareInterface import *
from modules.CameraInterface import *
from modules.DataInterface import *
from modules.ProtocolRunner import *
import picamera
import json


def send_msg(name,value,color=None):
    now = dt.datetime.now()
    msg = {}
    msg['time'] = "{0} {1}".format(now.date(),now.time())
    msg['data'] = '{0}'.format(name)
    msg['value'] = '{0}'.format(value)
    msg['color'] = '{0}'.format(color)
    for u in users:
        u.send(json.dumps(msg))

def notify_buzz():
    send_msg("Buzzer Sound",None)

def notify_feed():
    send_msg("Food Dispensed",None,"success")

def notify_click():
    send_msg("Button Press",None,"warning")

def notify_motion(change):
    send_msg("Activity",change,None)

def notify_start():
    send_msg("Experiment","starting",None)

def notify_pass():
    send_msg("Experiment Result","PASS","success")

def notify_fail():
    send_msg("Experiment Result","FAIL","warning")

# create our objects    
myData = DataInterface()
myhw = HardwareInterface()
myci = CameraInterface('./img/live.png')
mypr = ProtocolRunner(myhw,myData)

# experiment notifications
mypr.add_on_pass_cb(myData.log_success)
mypr.add_on_pass_cb(notify_pass)
mypr.add_on_fail_cb(myData.log_fail)
mypr.add_on_fail_cb(notify_fail)
mypr.add_on_start_cb(myData.log_start)
mypr.add_on_start_cb(notify_start)
mypr.add_on_end_cb(myData.log_stop)

# button notifications
myhw.on_button_up(notify_click)
myhw.on_button_up(myData.log_press)

# buzz notifications
myhw.on_buzz(myData.log_buzz)
myhw.on_buzz(notify_buzz)

# feed notifications
myhw.on_feed(myData.log_food)
myhw.on_feed(notify_feed)

# motion notifications
myci.set_motion_callback(notify_motion)
myci.set_motion_callback(myData.log_activity)

# button notifications
myhw.on_button_up(mypr.button_callback)


# OKAY GO!
myci.start()
myhw.start()
mypr.start()


# these route requests to our static bootstrap files
@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./js')

@route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./img')

@route('/css/<filename>')
def img_static(filename):
    return static_file(filename, root='./css')

@error(404)
def error404(error):
    with open('./views/fourohfour.tpl','r') as fp:
        data = fp.read()
        template = SimpleTemplate(data)
        return template.render(error=error,title="ruh roh!")
    

@post("/buzz")
def buzz():
    myhw.buzz_once()
    for u in users:
        u.send("buzz")

@post("/feed")
def dispense():
    myhw.dispense()
    for u in users:
        u.send("feed")


@route("/pics")
@view("live")
def live():
    return dict(title = "Live Pictures", button="derp2", content = "")

@route("/activity")
@view("activity")
def activity():
    myData.generateActivity('./img/activity.png')
    return dict(title = "Activity Monitor", button="", content = "")

@route("/passfail")
@view("plot")
def live():
    myData.generatePassFail()
    return dict(title = "Test Pass / Fail Results",
                image = '/img/pass_fail.png',
                route = '/passfail',
                content = "")


def make_table(data,title):
    retVal = ''
    retVal += '<div class="table-responsive"> '
    retVal += '<table class="table table-bordered table-hover table-striped" id="messages">'  
    retVal += '<thead><tr><td><b>{0}'.format(title)
    retVal += '</b></td></tr></thead>'
    retVal += '<tbody>'
    for k,v in data.items():
        retVal += '<tr>' 
        retVal += '<td>{0}</td>'.format(k) 
        retVal += '<td>{0}</td>'.format(v) 
        retVal += '</tr>' 
    retVal += '</tbody>'
    retVal += '</table>'
    retVal += '</div>'
    return retVal

@route("/stats")
@view("stats")
def live():
    stats=myData.generateStats()
    return dict(title = "Today's Stats",
                experiments = make_table(stats['experiments'],"Experiment Results"),
                events = make_table(stats['events'],"Today's Events"),
                activity = make_table(stats['activity'],"Today's Activity")
                )

@route("/about")
@view("about")
def about():
    return dict(title = "About")

@route("/controls")
@view("controls")
def controls():
    return dict(title = "Controls")


@route("/")
@view("main")
def main():
    return dict(title = "Live Feed", button="", content = "")

users = set()
@get('/websocket', apply=[websocket])
def chat(ws):
    users.add(ws)
    while True:
        msg = ws.receive()
        print msg
        if msg is not None:
            for u in users:
                u.send(msg)
        else: 
            break
    users.remove(ws)    

def signal_handler(signal, frame):
    mypr.shutdown()
    time.sleep(2)
    mypr.join()
    myci.shutdown()
    time.sleep(2)
    myci.join()
    myhw.shutdown()
    time.sleep(2)
    myhw.join()
    sys.exit(0)

if __name__ == "__main__":
    # on ctrl-c try to exit clean
    signal.signal(signal.SIGINT, signal_handler)
    port = int(os.environ.get("PORT", 5000))
    run(host='0.0.0.0', port=port, server=GeventWebSocketServer)
     

