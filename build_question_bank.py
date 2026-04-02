import time
import requests
import json
from collections import defaultdict

token = "请输入你的 token"

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
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
	"X-Auth-Token": token,
	"sec-ch-ua-mobile": "?0",
}

try:
	with open("data.json", "r", encoding="utf-8") as f:
		loaded_dict = json.load(f)
		answer_data = defaultdict(set)
		for key, value_list in loaded_dict.items():
			answer_data[key].update(value_list)
except FileNotFoundError:
	answer_data = defaultdict(set)

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
			answer_data[title].add(answer)
	else:
		print(f"  获取详情失败: {resp.status_code}")
	time.sleep(1)


def main():
	records = get_history_list()
	if not records:
		print("未获取到历史记录")
		return

	valid_records = [r for r in records if r.get("totalTime") is not None]
	print(f"共 {len(records)} 条记录，其中 {len(valid_records)} 条 totalTime 非空")

	for record in valid_records:
		paper_id = record["paperId"]
		process_paper(paper_id)
	

if __name__ == "__main__":
	main()
	key_count = len(answer_data)
	print(f'key count: {key_count}')
	serializable = {key: list(value) for key, value in answer_data.items()}
	with open("data.json", "w", encoding="utf-8") as f:
		json.dump(serializable, f, ensure_ascii=False, indent=4)
