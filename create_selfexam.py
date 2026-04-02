import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os

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


print(f'how many times?')
count = input()
for i in range(int(count)):
	began = WebDriverWait(wd, 150, 0.1).until(lambda wd: wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[2]/div[2]/button'))
	began.click()
	time.sleep(3)
	wd.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div[3]/span').click()
	time.sleep(0.1)
	wd.find_element(By.XPATH, '/html/body/div[4]/div[3]/button[2]').click()
	time.sleep(300)
