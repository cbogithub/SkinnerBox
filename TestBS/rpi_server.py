import json
import inspect, os, argparse, signal, sys
#import numpy as np
from bottle import get, post, run, request, static_file, route

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=imgPath)

@get('/')
def captureTopImg():
    return """<html><body><center><h1>
        Top camera not connected.
        </html></body></center></h1>
        """
@route('/derp/')
def derp():
    return "No top camera attached."

def signal_handler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='The Tempo CV Server')
    # #parser.add_argument('--settings', metavar='S',  nargs='+',
    # #                    help='Settings json file')
    # parser.add_argument('--no-camera', action='store_true',
    #                     help='Start the server with no cameras attached')
    signal.signal(signal.SIGINT, signal_handler)

    run(host='192.168.1.42', port=8080)
    exit(0)
