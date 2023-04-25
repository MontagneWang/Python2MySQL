# coding=utf-8
import requests
import json

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
}
global content_dict


def Check():
	global content_dict
	with open('test0425Vocaloid.json', 'a', encoding='utf8') as f2:
		f2.write('[')

	i = 0
	while True:
		i = i + 1
		code = 1
		# 可能失败 需要多尝试几次
		while code != 0:
			url = f'https://api.bilibili.com/archive_rank/getarchiverankbypartion?jsonp=jsonp&tid=28&pn={i}&ps=50'

			r = requests.get(url, headers=headers)
			content = r.content.decode('utf-8')  # <class 'str'>
			content_dict = json.loads(content)  # <class 'dict'>
			code = content_dict['code']
			if code != 0:
				print(f'第{i}页获取出错，code 为：{code}')



		with open('test0425Vocaloid.json', 'a', encoding='utf8') as f2:
			# 说明已经遍历完毕
			if content_dict['data']['page']['count'] == 0:
				f2.write(']')
				break
			json.dump(content_dict, f2, ensure_ascii=False, indent=2)
			# fixme 需要去除最后一个逗号（可以考虑添加顺序为先逗号再数据[这样需要去除第一个逗号]）
			f2.write(',')

		print('第 {} 页保存成功'.format(i))

	print('所有数据保存成功')


if __name__ == '__main__':
	Check()
