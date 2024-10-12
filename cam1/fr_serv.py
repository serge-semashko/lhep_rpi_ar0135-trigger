import sys
import base64
import traceback
import json
import time
import memcache
import os
from os import listdir
from flask import request
from flask import Flask
from flask import make_response

app = Flask(__name__)

fbr = open('last_br.txt', 'r')
b = int(fbr.readlines()[0])
client = memcache.Client([('127.0.0.1', 11211)])
client.set('Value', b)
fbr.close()
print(b)


@app.route('/set_brightness', methods=['GET'])
def set_bright():
    print("connect")
    params = {}
    for i in request.args:
        params[str(i)] = request.args[i]
    inprm = str(params)
    print("connect 1" + inprm)
    try:
        br = int(params['brightness'])
        client = memcache.Client([('127.0.0.1', 11211)])
        client.set('Value', br)
        fbr = open('last_br.txt', 'w')
        fbr.write(str(br))
        fbr.close()
        resp = make_response('OK', 200)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** format_exc, first and last line:")
        res_data = traceback.format_exc().splitlines()
        print(res_data)
        resp = make_response(res_data, 400)
    resp.headers['content-type'] = 'text/html'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp

@app.route('/delete_frames', methods=['GET'])
def del_frames():
    print('connect')
    try:
        flist = listdir('.')
        for file_name in flist:
            if file_name.endswith('.jpg'):
                os.remove(file_name)
        resp = make_response('OK', 200)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** format_exc, first and last line:")
        res_data = traceback.format_exc().splitlines()
        print(res_data)
        resp = make_response(res_data, 400)
    resp.headers['content-type'] = 'text/html'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp


@app.route('/', methods=['GET'])
def get_index():
    try:
        file_name = 'frames_brightness.html' 
        ff = open(file_name, 'r')
        bin = ff.read()
        resp = make_response(bin, 200)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** format_exc, first and last line:")
        res_data = traceback.format_exc().splitlines()
        print(res_data)
        resp = make_response(res_data, 400)
    resp.headers['content-type'] = 'text/html'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp



@app.route('/get_frames_list', methods=['GET'])
def get_frames_list():
    try:
        flist = listdir('.')
        rez_arr = []
        for i in flist:
            if i[-3:] == 'jpg':
                rez_arr.append(i)
        rez_arr.sort(reverse=True)
        rr = str(rez_arr).replace('\'', '\"')
        print(json.dumps(rr))
        resp = make_response(json.dumps(rr), 200)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** format_exc, first and last line:")
        res_data = traceback.format_exc().splitlines()
        print(res_data)
        resp = make_response('{"rc":-1}', 200)
    resp.headers['content-type'] = 'text/html'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'

    return resp


@app.route('/get_frame', methods=['GET'])
def get_frame():
    print("connect")
    params = {}
    for i in request.args:
        params[str(i)] = request.args[i]
    inprm = str(params)
    print("connect 1" + inprm)
    try:
        file_name = params['file']
        ff = open(file_name, 'rb')
        bin = ff.read()
        resp = make_response(bin, 200)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** format_exc, first and last line:")
        res_data = traceback.format_exc().splitlines()
        print(res_data)
        resp = make_response(res_data, 400)
    resp.headers['content-type'] = 'image/jpeg'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp

@app.route('/get_shot/<file_name>', methods=['GET'])
def get_shot(file_name):
    print("connect")
    try:
        ff = open(file_name, 'rb')
        bin = ff.read()
        resp = make_response(bin, 200)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** format_exc, first and last line:")
        res_data = traceback.format_exc().splitlines()
        print(res_data)
        resp = make_response(res_data, 400)
    resp.headers['content-type'] = 'image/jpeg'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp



app.run(debug=False, host="0.0.0.0", port=80)


