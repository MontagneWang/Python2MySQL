# coding=utf-8
import requests
import json
import os.path
import time
import random
import pymysql

global content_dict
import openpyxl, os  # 引入库
import re

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')


def Check():
	global content_dict

	#    '标题'          video['title']
	#    '作者'          video['author']
	#    '播放数'          video['play']
	#    '发布时间'          video['create']
	#    '评论数'          video['stat']['reply']
	#    '弹幕数'          video['stat']['danmaku']
	#    '点赞数'          video['stat']['like']
	#    '收藏数'          video['stat']['favorite']
	#    '视频链接'          video['short_link']
	#    '视频封面'          video['pic']
	#    '投稿人头像'          video['face']
	#    '简介'          video['description']
	#    '作者UID'          video['mid']
	#    '时长'          video['duration']
	#    '硬币'          video['stat']['coin']
	#    '分享'          video['stat']['share']
	#    '点踩'          video['stat']['dislike']

	# 打开数据库，参数依次为：主机名/IP，用户名，密码，数据库名，字符集
	db = pymysql.connect(
		host='127.0.0.1',  # 连接主机, 默认127.0.0.1
		user='root',  # 用户名
		passwd='123456',  # 密码
		port=3306,  # 端口，默认为3306
		db='python',  # 数据库名称
		charset='utf8mb4'  # 字符编码
	)

	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()

	# 使用 execute() 方法执行 SQL 查询
	cursor.execute("select version()")

	# 使用 fetchone() 方法获取单条数据
	data = cursor.fetchone()
	print("Datebase version : %s " % data)  # 输出 Datebase version : 8.0.21

	# 如果表 books 存在，则删除表
	cursor.execute("DROP TABLE IF EXISTS books")

	# 使用与处理语句创建表
	sql = """
	CREATE TABLE books (
	    id int(8) NOT NULL AUTO_INCREMENT,
	    name longtext NOT NULL,
	    category longtext NOT NULL,
	    price longtext DEFAULT NULL,
	    publish_time date DEFAULT NULL,
	    PRIMARY KEY (id)
	) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ;
	"""

	# 执行 SQL 语句
	cursor.execute(sql)

	with open('./realData.json', 'r', encoding='utf8')as fp:
		content_dict = json.load(fp)

	i = 0
	for eachReply in content_dict:  # 读取每一个返回的数据页（内含 50 个数据）
		print('正在处理第 {} 页'.format(i))
		i += 1
		for video in eachReply['data']['archives']:  # 读取每一个视频
			# print('作者：', video['author'])
			# print(video['author'])
			data = [(video['title'].replace("&amp;", "&"),
			         video['author'],
			         video['play'],
			         video['create'])]
			# try:
				# 执行 SQL 语句，插入多条数据
			cursor.executemany("insert into books(name, category, price, publish_time) values (%s, %s, %s, %s)",data)
			# 提交数据
			db.commit()
			# except:
				# 发生错误时回滚
				# print("发生错误")
				# print(data)
				# db.rollback()

	# 关闭数据库连接
	print("已全部存入数据库")
	db.close()


if __name__ == '__main__':
	Check()
