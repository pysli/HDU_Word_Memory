import time
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

print(f'start?')
is_c = input()
if is_c:
	testresult = WebDriverWait(wd, 15, 0.5).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[3]/div[2]'))
	direct_divs = testresult.find_elements(By.XPATH, "./div")
	count = len(direct_divs)
	print(count)
	for i in range(126):
		testresult = WebDriverWait(wd, 15, 0.5).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[3]/div[2]'))
		current_div = testresult.find_elements(By.XPATH, "./div")[i]
		crt_check = current_div.find_element(By.XPATH, "./div")
		crt_attr = crt_check.get_attribute("class")
		if "unfinished" in crt_attr.split():
			continue
		current_div.click()
		time.sleep(3)
		for j in range(100):
			title = WebDriverWait(wd, 15, 0.1).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]'))
			optitle = title.text
			optitle = optitle.rstrip(" .")
			option_list = WebDriverWait(wd, 15, 0.1).until(lambda wd:wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div[2]'))
			correct_option = option_list.find_element(By.CLASS_NAME, "correct-ans")
			option_text = correct_option.find_element(By.CLASS_NAME, "option-text")
			optext = option_text.text
			optext = optext.rstrip(" .")
			print(f'{optitle}, {optext}')
			data[optitle].add(optext)
			if j != 99:
				wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/i').click()
		wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[1]').click()
		print(f'complete:{i}/{count}')
		time.sleep(1)

key_count = len(data)
print(f'key count: {key_count}')
if is_c:
	serializable = {key: list(value) for key, value in data.items()}
	with open("answer_bank.json", "w", encoding="utf-8") as f:
		json.dump(serializable, f, ensure_ascii=False, indent=4)