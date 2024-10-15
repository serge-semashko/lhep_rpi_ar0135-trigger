import sys
import base64
import traceback
import json
import time
import threading 
from pymemcache.client.base import Client
import os
from os import listdir
from flask import request
from flask import Flask
from flask import make_response
from procshot import *
app = Flask(__name__)

fbr = open('last_br.txt', 'r')
b = int(fbr.readlines()[0])
client = Client(('127.0.0.1', 11211))
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
        client = Client(('127.0.0.1', 11211))
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
            if file_name.endswith('.png'):
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
            if i[-3:] == 'txt':
                if i[:3] !='202':
                    continue
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
    resp.headers['content-type'] = 'image/png'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp

@app.route('/get_file', methods=['GET'])
def get_file():
    print("connect")
    params = {}
    for i in request.args:
        params[str(i)] = request.args[i]
    inprm = str(params)
    print("connect 1" + inprm)
    try:
        file_name = params['file']
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
    resp.headers['content-type'] = ' text/html; charset=utf-8'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp

@app.route('/get_oneshot', methods=['GET'])
def get_oneshot():
    print("connect")
    params = {}
    for i in request.args:
        params[str(i)] = request.args[i]
    inprm = str(params)
    print("connect 1" + inprm)
    try:
        file_name = params['file']
        shot_src = file_name.split('.')[0]
        file_name = 'one_shot.html'
        ff = open(file_name, 'r')
        bin = ff.read()
        bin = bin%(shot_src);
        resp = make_response(bin, 200)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** format_exc, first and last line:")
        res_data = traceback.format_exc().splitlines()
        print(res_data)
        resp = make_response(res_data, 400)
    resp.headers['content-type'] = ' text/html; charset=utf-8'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp


@app.route('/get_all_shots', methods=['GET'])
def get_all_shots():
    print("connect")
    import subprocess
    process = subprocess.Popen('zip all_arch 202*.*', shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)
    file_name = 'all_arch.zip'
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

    resp.headers['content-type'] = 'application/zip'
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
    resp.headers['content-type'] = 'image/png'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return resp

def process_shots():
    print('process_shots():')
    files_ok = []
    while 1==1:
        a=1
        flist = listdir('.')
        # print(str(flist))
        for i in flist:
            if i[-3:] != 'png':
                continue
            # print(i)
            if i[:3] !='202':
                    continue
            # print(i)
            if i.find('bar') >-1:
                    continue
            # print(i)
            if i.find('mark') >-1:
                    continue
            # print(i)
            if i in files_ok:
                continue
            # print(i)
            fname = i.split('.')[0]
            # print(os.path.isfile(fname+'-bar.png'))
            # print( os.path.isfile(fname+'-barh.png'))
            # print( os.path.isfile(fname+'-markup.png'))
            if os.path.isfile(fname+'-bar.png') and os.path.isfile(fname+'-barh.png') and  os.path.isfile(fname+'-markup.png') and os.path.isfile(fname+'.txt'):
                continue
            # kx = (2 ** 0.5) / 2
            # ky = 1 / 2
    #                process_shot(kx, ky, 260, 284, 644, 762, 100, 70, 16, 12, imname, 4, 2, 1))
            # kx =(1* (2 ** 0.5) )/ 2
            # ky = 1/2 
            # xl=538
            # yu=358
            # xr=799
            # yd=600
            # x_len=100
            # y_len=70
            # x_tab=16
            # y_tab=12
            # w1=4
            # w2=1
            # w3=1

            process_shot(kx, ky, xl, yu, xr, yd, x_len, y_len, x_tab, y_tab, i, w1, w2, w3)
            files_ok.append(i)    
            print('processed '+i)
        time.sleep(1)


# kx = (2 ** 0.5) / 2
# ky = 1 / 2
# process_shots()
print('aaaaa')
pro_shots  = threading.Thread(target=process_shots, args=(),daemon=False)
pro_shots.start()
app.run(debug=False, host="0.0.0.0", port=80)


