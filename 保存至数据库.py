# coding=utf-8
import json
import pymysql

global content_dict


def Check():
	global content_dict

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
	print("Datebase version : %s " % data)  # 输出 Datebase version   : 8.0.21

	# region
	# 使用与处理语句创建表
	# title,author,mid,face,createTime,location,link,pic,duration,play,danmaku,reply,likePoint,coin,favorite,share,dislike,nowrank,hisrank,aid,cid,description

	# title
	# author
	# mid
	# face
	# create
	# pub_location
	# short_link
	# pic
	# duration
	# play
	# danmaku
	# reply
	# like
	# coin
	# favorite
	# share
	# dislike
	# now_rank
	# his_rank
	# aid
	# cid
	# description

	# 如果表 testSql 存在，则删除表
	# cursor.execute("DROP TABLE IF EXISTS testSql")
	# endregion
	# 建表，不推荐全部使用 longtext，尝试改用 int/bigint
	sql = """
	CREATE TABLE testSql(
	    id int(8) AUTO_INCREMENT,
	    title longtext,
		author longtext,
		mid longtext,
		face longtext,
		createTime longtext,
		location longtext,
		link longtext,
		pic longtext,
		duration longtext,
		play longtext,
		danmaku longtext,
		reply longtext,
		likePoint longtext,
		coin longtext,
		favorite longtext,
		share longtext,
		dislike longtext,
		nowrank longtext,
		hisrank longtext,
		aid longtext,
		cid longtext,
		description longtext,
	    PRIMARY KEY (id)
	) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
			# video['title']               '标题'
			# video['author']              '作者'
			# video['mid']                 '作者UID'
			# video['face']                '作者头像'
			# video['create']              '发布时间'
			# video['pub_location']        '发布地'
			# video['short_link']          '视频链接'
			# video['pic']                 '视频封面'
			# video['duration']            '视频时长'
			# video['play']                '播放数'
			# video['stat']['danmaku']     '弹幕数'
			# video['stat']['reply']       '评论数'
			# video['stat']['like']        '点赞数'
			# video['stat']['coin']        '硬币'
			# video['stat']['favorite']    '收藏数'
			# video['stat']['share']       '分享'
			# video['stat']['dislike']     '点踩'
			# video['stat']['now_rank']
			# video['stat']['his_rank']
			# video['aid']
			# video['cid']
			# video['description']         '简介'
			try:
				data = [(
					video['title'].replace("&amp;", "&"),
					video['author'],
					video['mid'],
					video['face'],
					video['create'],
					video['pub_location'] if 'pub_location' in video else 0,
					video['short_link'],
					video['pic'],
					video['duration'],
					video['play'],
					video['stat']['danmaku'],
					video['stat']['reply'],
					video['stat']['like'],
					video['stat']['coin'],
					video['stat']['favorite'],
					video['stat']['share'],
					video['stat']['dislike'],
					video['stat']['now_rank'],
					video['stat']['his_rank'],
					video['aid'],
					video['cid'],
					video['description']
				)]
			except:
				print("data 获取数据出错")

			try:
				# 执行 SQL 语句，插入多条数据
				cursor.executemany("insert into testSql(title,author,mid,face,createTime,location,link,pic,duration,play,danmaku,reply,likePoint,coin,favorite,share,dislike,nowrank,hisrank,aid,cid,description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",data)
			# 提交数据
				db.commit()

			except:
				print("写入数据库时发生错误")
				print(data)
				# 发生错误时回滚
				# db.rollback()

	# 关闭数据库连接
	print("已全部存入数据库")
	db.close()


if __name__ == '__main__':
	Check()
