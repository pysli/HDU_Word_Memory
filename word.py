import time
from collections import defaultdict
import requests
import json
import random

token = "your token"

headers = {
	"Accept": "application/json, text/plain, */*",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
	"Connection": "keep-alive",
	"Host": "skl.hdu.edu.cn",
	"Referer": "https://skl.hdu.edu.cn/?" + token,
	"Sec-Fetch-Dest": "empty",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Site": "same-origin",
	"User-Agent": "Mozilla/5.0 (Linux; Android 13; IQOO 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
	"X-Auth-Token": token,
	"sec-ch-ua-mobile": "?1",
	"sec-ch-ua-platform": "Android"
}

try:
	with open("answer_bank.json", "r", encoding="utf-8") as f:
		loaded_dict = json.load(f)
		answer_bank = defaultdict(set)
		for key, value_list in loaded_dict.items():
			answer_bank[key].update(value_list)
except FileNotFoundError:
	answer_bank = defaultdict(set)

# 考试部分
nohit = 0
def normalize_text(text):
	if not text:
		return ""
	text = text.rstrip(" .")
	return text

def create_newtest(type):
	starttime = int(time.time() * 1000)
	if type == 0:
		url = "https://skl.hdu.edu.cn/api/paper/new?type=0&week=0&startTime=" + str(starttime)
	elif type == 1:
		url = "https://skl.hdu.edu.cn/api/paper/new?type=1&week=0&startTime=" + str(starttime)
	resp = requests.get(url, headers = headers)
	if resp.status_code == 200:
		return resp.json()
	else:
		print(f"获取失败: {resp.status_code}")
		print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
		return []

def build_submit_payload(data, score_inf):
	global nohit
	payload = {
		"paperId": data["paperId"],
		"type": data["type"],
		"list": []
	}
	control_score = 1
	count = 0
	for item in data["list"]:
		count += 1
		title = item.get("title", "").rstrip(" .")
		chosen = None
		for oplettter in ["A", "B", "C", "D"]:
			if item["answer" + oplettter].rstrip(" .") in answer_bank.get(title, set()):
				chosen = oplettter
				break
		if chosen == None:
			chosen = random.choice('ABCD')
			nohit += 1
		if control_score == 1 and count - nohit >= score_inf:
			chosen = random.choice('ABCD')
		payload["list"].append({
			"input": chosen,
			"paperDetailId": item["paperDetailId"]
			})
	return payload

def respond(stdata):
	url = "https://skl.hdu.edu.cn/api/paper/save"
	resp = requests.post(url,  headers=headers, json=stdata)
	if resp.status_code == 200:
		print("success exam")
	else:
		print(f"failed: {resp.status_code}")

def single_exam(sleeptime, type, score_inf):
	global nohit
	nohit = 0
	paper = create_newtest(type)
	if not paper:
		print("create failed")
		return
	stdata = build_submit_payload(paper, score_inf)
	if not stdata:
		print("failed in transform")
		return
	print(f'nohit: {nohit}')
	time.sleep(sleeptime)
	respond(stdata)
	paper_id = paper["paperId"]
	time.sleep(1)
	paper_resp = requests.get(f"https://skl.hdu.edu.cn/api/paper/detail?paperId={paper_id}", headers=headers)
	if paper_resp.status_code == 200:
		score = paper_resp.json()["mark"]
		print(f'score: {score}')
	else:
		print("获取分数失败")


# 构建题库部分
def get_history_list():
	url = "https://skl.hdu.edu.cn/api/paper/list?type=0&week=0&schoolYear=&semester="
	resp = requests.get(url, headers=headers)
	if resp.status_code == 200:
		return resp.json()
	else:
		print(f"获取历史记录失败: {resp.status_code}")
		return []

def process_paper(paper_id):
	print(f"正在处理试卷: {paper_id}")
	detail_url = f"https://skl.hdu.edu.cn/api/paper/detail?paperId={paper_id}"
	resp = requests.get(detail_url, headers=headers)
	if resp.status_code == 200:
		data = resp.json()
		print(f"  获取详情成功，题目数: {len(data.get('list', []))}")
		for item in data['list']:
			title = item['title'].rstrip(" .")
			answer = item["answer" + item['answer']].rstrip(" .")
			print(f"{title} -> {answer}")
			answer_bank[title].add(answer)
	else:
		print(f"  获取详情失败: {resp.status_code}")
	time.sleep(1)

def process_all():
	records = get_history_list()
	if not records:
		print("未获取到历史记录")
		return

	valid_records = [r for r in records if r.get("totalTime") is not None]
	print(f"共 {len(records)} 条记录，其中 {len(valid_records)} 条 totalTime 非空")

	for record in valid_records:
		paper_id = record["paperId"]
		process_paper(paper_id)

def build_answer_bank():
	process_all()
	key_count = len(answer_bank)
	print(f'key count: {key_count}')
	serializable = {key: list(value) for key, value in answer_bank.items()}
	with open("answer_bank.json", "w", encoding="utf-8") as f:
		json.dump(serializable, f, ensure_ascii=False, indent=4)

def create_many_exam(count):
	for i in range(count):
		if i == count - 1:
			single_exam(0, 0, 0)
			return
		else:
			single_exam(300, 0, 0)
		print(f'{i + 1}/{count}')

def got_input(inf, sup, default=None):
	s = input().strip()
	if s == "":
		return default
	if s.isdigit():
		num = int(s)
	else:
		print("请输入纯数字")
		return -1
	if num >= inf and num <= sup:
		return num
	else:
		print("请输入合法的数字")
		return -1

def single_cycle():
	print("请选择你需要的功能\n1. 自测测试\n2. 考试\n3. 创建用于构建题库的自测\n4. 构建词库\n5. quit\n或直接按回车退出")
	num = got_input(1, 5, default=5)
	if num == -1:
		return 
	if num == 1:
		print("输入你想要的答题时间(range:[0, 480], defalut value: 300)")
		sleep_time = got_input(0, 480, default=300)
		if sleep_time == -1:
			return
		print("请输入想要的分数下界(range[0, 100], default value: 75)")
		score_inf = got_input(0, 100, default=75)
		if score_inf == -1:
			return
		single_exam(sleep_time, 0, score_inf)
	elif num == 2:
		print("输入你想要的答题时间(range:[360, 480], defalut value: 400)")
		sleep_time = got_input(360, 480, default=400)
		if sleep_time == -1:
			return
		print("请输入想要的分数下界(range[0, 100], default value: 75)")
		score_inf = got_input(0, 100, default=75)
		if score_inf == -1:
			return
		single_exam(sleep_time, 1, score_inf)
	elif num == 3:
		print("输入你想要的创建次数(range:[0, 300], default value: 1)")
		count = got_input(0, 300, default=1)
		create_many_exam(count)
	elif num == 4:
		build_answer_bank()
	elif num == 5:
		return -1
	return 0

def test_token():
	url = "https://skl.hdu.edu.cn/api/paper/list?type=0&week=0&schoolYear=&semester="
	resp = requests.get(url, headers=headers)
	if resp.status_code == 200:
		return 1
	else:
		print(f"获取历史记录失败: {resp.status_code}")
		print("请检查token是否正确，是否过期")
		return -1

def main():
	token_ok = test_token()
	if token_ok == -1:
		return
	while(1):
		status = single_cycle()
		if status == -1:
			break

if __name__ == "__main__":
	main()