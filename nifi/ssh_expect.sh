#!/usr/bin/expect
spawn ssh -o StrictHostKeyChecking=no nifi@jupyter "python3 /yolov7/notebook/process_video.py"
expect "Password:"
send "password\r"
interact
