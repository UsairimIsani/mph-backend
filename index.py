import serial
import syslog
import time
import requests


api_key = ''

port = '/dev/ttyUSB0'
# port = '/dev/ttyACM0'
api_url = 'https://api.pushbullet.com/v2'
ard = serial.Serial(port, 9600, timeout=5)

with open('api_key.txt') as f:
    api_key = f.readline().strip("\n")


# def get_devices():
#     return get_response('/devices')


def get_response(url):
    return requests.get(api_url+url,  params={'q': 'requests+language:python'},
                        headers={'Access-Token': api_key},).json()


def send_request(url, data):
    return requests.post(api_url+url,  params={'q': 'requests+language:python'},
                         headers={'Access-Token': api_key}, data=data).json()


def send_push(title, body):
    print(title,body)
    # send_request("/pushes", {
    #     "type": "note",
    #     "title": title,
    #     "body": body
    # })


# send_push("Anees", "Acha Bacha or Harami")


def parse_serial(msg):
    msg = msg.split(",")
    vals = []
    for i in msg:
        vals.append(int(i.split("=")[1]))
    determine_msg(vals)



def determine_msg(val):
    if val[0] in range(10, 17) and val[1] in range(0, 10) and val[2] in range(0, 10):
            send_push("patient Said:", "I Need Biryani")
    elif val[1] in range(10, 17):
            send_push("patient Said:", "I Need Kofta")
    elif val[2] in range(10, 17):
            send_push("patient Said:", "I Need Machli")


while (True):
    msg = ard.readline().decode("ascii")
    print(msg)
    parse_serial(msg)
