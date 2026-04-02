import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import json
from collections import defaultdict

try:
	with open("answer_bank.json", "r", encoding="utf-8") as f:
		loaded_dict = json.load(f)
		data = defaultdict(set)
		for key, value_list in loaded_dict.items():
			data[key].update(value_list)
except FileNotFoundError:
	data = defaultdict(set)

mobile_emlation = {
	'deviceMetrics': {
		'width': 1707,
		'height': 773,
		'pixelRatio': 1.0
	},
	'userAgent': 'Mozilla/5.0 (Linux; Android 13; IQOO 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
}
edge_options = Options()
edge_options.add_experimental_option('mobileEmulation', mobile_emlation)
wd = webdriver.Edge(service=Service('./msedgedriver.exe'), options=edge_options)
wd.get('https://skl.hduhelp.com/?type=5#/english/list')
wd.maximize_window()
time.sleep(2.5)


answer_count = len(data)
print(f'answer count: {answer_count}')

if answer_count < 1000:
	print(f'insufficient data')
	exit()


print(f'start test?')
is_start = input()
nohit = 0
if is_start:
	# 关闭自动下一题, 获取剩余时间
	auto_next = WebDriverWait(wd, 15, 0.5).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div/div'))
	auto_attr = auto_next.get_attribute("class")
	if "van-switch--on" in auto_attr.split():
		WebDriverWait(wd, 15, 0.5).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div/span')).click()
	time_remain_str = WebDriverWait(wd, 15, 0.5).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[3]/div[1]/div')).text
	minutes, seconds = map(int, time_remain_str.split(':'))
	time_remain = minutes * 60 + seconds
	start = time.time()
	for i in range(100):
		question = WebDriverWait(wd, 15, 0.1).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]'))
		optionA = WebDriverWait(wd, 15, 0.1).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]'))
		optionB = WebDriverWait(wd, 15, 0.1).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]'))
		optionC = WebDriverWait(wd, 15, 0.1).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div[2]/div[3]/div[2]'))
		optionD = WebDriverWait(wd, 15, 0.1).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div[2]/div[4]/div[2]'))
		q_text = question.text.rstrip(" .")
		a_text = optionA.text.rstrip(" .")
		b_text = optionB.text.rstrip(" .")
		c_text = optionC.text.rstrip(" .")
		d_text = optionD.text.rstrip(" .")
		print(f'---{i + 1}\n{q_text}\nA.{a_text}\nB.{b_text}\nC.{c_text}\nD.{d_text}')
		if i > 87 and i <99 and nohit < 10:
			rand = random.randint(0, 3)
			if rand == 0:
				optionA.click()
			elif rand == 1:
				optionB.click()
			elif rand == 2:
				optionC.click()
			elif rand == 3:
				optionD.click()
			wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/i').click()
			time.sleep(0.2)
			# 随机选择避免正确率过高
			continue
		if a_text in data.get(q_text, set()):
			optionA.click()
		elif b_text in data.get(q_text, set()):
			optionB.click()
		elif c_text in data.get(q_text, set()):
			optionC.click()
		elif d_text in data.get(q_text, set()):
			optionD.click()
		else:
			print(f'no hit')
			optionA.click()
			nohit += 1

		if i != 99:
			wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/i').click()
		
		result = None
		time.sleep(0.1)

	end = time.time()
	# 等待至时间还剩一分钟
	if (time_remain - (end - start) - 60) > 0:
		time.sleep(time_remain - (end - start) - 60)
	wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[3]/span').click()
	time.sleep(0.1)
	wd.find_element(By.XPATH, '/html/body/div[4]/div[3]/button[2]').click()

print(f'no hit:{nohit}')
print("输入任意键以结束")
input()





	
