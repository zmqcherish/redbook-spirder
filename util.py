import sys
import os
import requests
import logging
import json
from tinydb import TinyDB, Query
import socket
import shutil
from time import sleep, strftime, time
from datetime import datetime, timedelta
from collections import defaultdict

logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', level=logging.INFO, datefmt='%m-%d %H:%M:%S')

def except_decorative(func):
	def decorator(*args, **keyargs):
		try:
			return func(*args, **keyargs)
		except Exception as e:
			logging.error(f'handle {func.__name__} error: {e}')
	return decorator


def create_folder(path):
	if os.path.exists(path):
		return
	os.mkdir(path)


def get_json_file(file_path):
	with open(file_path, 'r', encoding='utf-8') as json_file:
		return json.load(json_file)


def get_ip():
	ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]]
	num = len(ips)
	if num == 1:
		return ips[0]
	tips = '\n'.join([f"{(i + 1)} - {ips[i]}" for i in range(num)])
	while True:
		res = input(f"请选择ip...\n{tips}\n")
		if not res.isalnum():
			print('输入有误')
			continue
		res = int(res)
		if res < 1 or res > num:
			print('输入有误')
			continue
		return ips[res - 1]

def get_user_ip_port(ip=None, port=8888):
	ip = ip or get_ip()
	# ip = '10.2.147.8'
	res = ''
	while True:
		res = input(f"请输入端口号，直接回车使用默认的8888): ")
		if res == '':
			res = port
			break
		if not res.isdigit():
			print('输入有误')
			continue
		break
	return ip, int(res)


def log_info(msg1, msg2=''):
	msg = msg1 + (f", {msg2}" if msg2 else '')
	logging.info(msg + '\n')


def log_info_list(msgs):
	msg = ' '.join(msgs)
	logging.info(msg + '\n')


def get_file_data(path='file'):
	ff = os.listdir(path)
	for f in ff:
		file_path = os.path.join(path, f)
		if file_path == user_file:
			continue
		tiny_db = TinyDB(file_path, encoding="utf8", ensure_ascii=False)
		user_table = tiny_db.table('notes')
		yield user_table.all()

file_path = 'file'
user_file = f'{file_path}/users.json'