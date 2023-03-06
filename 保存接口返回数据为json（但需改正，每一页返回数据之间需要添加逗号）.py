# coding=utf-8
import requests
import json

global content_dict


def Check():
	global content_dict

	for i in range(0, 6527):
		i += 1
		code = 1
		# 可能失败 需要多尝试几次
		while not code == 0:
			url = 'https://api.bilibili.com/archive_rank/getarchiverankbypartion?jsonp=jsonp&tid=30&pn={}&ps=50'.format(i)

			r = requests.get(url)
			content = r.content.decode('utf-8')  # <class 'str'>
			content_dict = json.loads(content)  # <class 'dict'>
			code = content_dict['code']
			print('code ',code)
			print('现在是第 {} 页'.format(i))

		with open('title.json', 'a', encoding='utf8') as f2:
			json.dump(content_dict, f2, ensure_ascii=False, indent=2)

		print('第 {} 页保存成功'.format(i))


if __name__ == '__main__':
	Check()
