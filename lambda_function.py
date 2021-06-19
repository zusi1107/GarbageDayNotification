import os
import requests

import calendar
import datetime

def get_nth_week(day):
    return (day - 1) // 7 + 1

def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)

def create_garbage_notification_message():
    
    yobi = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    date = datetime.date.today() + datetime.timedelta(days=1)
    nth_dow = get_nth_dow(date.year, date.month, date.day)

    if yobi[nth_dow[1]] in ("Wed", "Sat"):
        return str(date) + " 可燃ごみ（毎週水曜日・毎週土曜日）"
    elif yobi[nth_dow[1]] == "Tue":
        return str(date) + " 資源ごみ（毎週火曜日）"
    elif yobi[nth_dow[1]] == "Mon":
        if nth_dow[0] in (1,3):
            return str(date) + " ペットボトル（第１、第３月曜日）"
        elif nth_dow[0] in (2,4):
            return str(date) + " 不燃ごみ（第２、第４月曜日）"
        else:
            return str(date) + " ごみ出しなし"    
    else:
        return str(date) + " ごみ出しなし"

# SSM Get SecureString
import boto3
ssm = boto3.client('ssm', 'us-east-2')
def get_parameters():
    response = ssm.get_parameters(
        Names=['GarbageDayNotification-LINEhook'],WithDecryption=True
    )
    for parameter in response['Parameters']:
        return parameter['Value']

# Line Notify
ACCESS_TOKEN = get_parameters()
HEADERS = {"Authorization": "Bearer %s" % ACCESS_TOKEN}
URL = "https://notify-api.line.me/api/notify"

# Handler
def lambda_handler(event, context):
    message = create_garbage_notification_message()
    data = {'message': message}
    #lineに通知
    requests.post(URL, headers=HEADERS, data=data)