# -*- coding: utf-8 -*-
import datetime
import pymysql
import time

class Mysql:
    # 初始化方法的参数，创建类时，必须给足
    def __init__(self):
        print('Mysql init')
        self.host = '172.25.47.230'
        self.port = 3306
        self.database = 'report'
        self.user = 'root'
        self.password = 'root'
        self.conn = None
        self.cur = None

    def db_open(self):        
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.database, user=self.user,
                                    password=self.password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        print('db_open connect')
        self.cur = self.conn.cursor()
        print('db_open cursor')
        return True

    def db_close(self):
        self.cur.close()
        print('db_close cursor')
        self.conn.close()
        print('db_close connect')
        return True

    def get_personnel_list(self):
        Mysql.db_open(self)
        self.cur.execute("select * from personnel")
        personnel_list = self.cur.fetchall()
        for i in personnel_list:
            print(i["name"],i["team"],i["sex"],i["age"],i["politic"])
        Mysql.db_close(self)
        return personnel_list

    def get_team_list(self):
        team_list=[]
        Mysql.db_open(self)
        self.cur.execute("select * from team")
        results_team = self.cur.fetchall()
        for i in results_team:
            self.cur.execute("select name from personnel where team = %s", (i["name"]))
            results_personnel = self.cur.fetchall()
            name_list = []
            for j in results_personnel:
                name_list.append(j['name'])
            team_list.append([i["name"], i["num"], len(name_list), name_list])
        Mysql.db_close(self)
        print(team_list)
        return team_list

    def get_score_list(self):
        Mysql.db_open(self)
        self.cur.execute("select * from score")
        score_list = self.cur.fetchall()
        Mysql.db_close(self)
        print(score_list)
        return score_list

    def get_score(self, t_name, judges):
        Mysql.db_open(self)
        self.cur.execute("select * from score where t_name = %s and judges = %s", (t_name, judges))
        score = self.cur.fetchall()
        Mysql.db_close(self)
        if score:
            print(score)
        else:
            print('No Data')
        return score

    def add_score(self, score):
        Mysql.db_open(self)
        self.cur.execute("insert into score (t_num,t_name,judges,date,p_name,score_all,\
        score_1,score_2,score_3,score_4,score_5,score_6,score_7,score_8,score_9,score_10) values (\
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (score['t_num'], score['t_name'], score['judges'],
                                                            score['date'], score['p_name'], score['score_all'],
                                                            score['score_1'], score['score_2'], score['score_3'],
                                                            score['score_4'], score['score_5'], score['score_6'],
                                                            score['score_7'], score['score_8'], score['score_9'],
                                                            score['score_10']))
        self.conn.commit()
        Mysql.db_close(self)
        return True

    def set_score(self, score):
        Mysql.db_open(self)
        self.cur.execute("update score set date=%s,p_name=%s,score_all=%s,\
        score_1=%s,score_2=%s,score_3=%s,score_4=%s,score_5=%s,score_6=%s,score_7=%s,score_8=%s,score_9=%s,score_10=%s \
        where t_name = %s and judges = %s", (score['date'], score['p_name'], score['score_all'], score['score_1'],
                                             score['score_2'], score['score_3'], score['score_4'], score['score_5'],
                                             score['score_6'], score['score_7'], score['score_8'], score['score_9'],
                                             score['score_10'], score['t_name'], score['judges']))
        self.conn.commit()
        Mysql.db_close(self)
        return True

    def set_score_all(self, team, judges, score_all):
        Mysql.db_open(self)
        self.cur.execute("update score set date=%s,score_all=%s where t_name = %s and judges = %s",
                         (time.strftime("%Y-%m-%d", time.localtime()), score_all, team, judges))
        self.conn.commit()
        Mysql.db_close(self)
        return True

def write(self):
    fp = open(r"C:\Users\Gusion\Desktop\photo\马丙辉.jpg", mode='rb')
    img = fp.read()
    fp.close()
    Mysql.db_open(self)
    self.cur.execute("insert into personnel (name,team,sex,age,\
    politic,native,address,education,university,speciality,stage1,stage2,stage3,\
    stage4,excellent,image) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                     ('马丙辉', '控制器工程小分队', '男', '27', '共青团员', '江苏盐城',
                      '上海市上海浦东新区祝桥镇凉亭路91弄', '研究生', '南京理工大学', '电力电子与电力传动',
                      '软件 ', '工厂实习', '软件 ', '软件 ',
                      'S:输出大量测试数据报表给客户，耗费工时。\nT:E50项目的测试数据需按照固有格式输出，原有手工输出方式效率低。\nA:将固定式输出操作交给机器代码执行。\nR:通过代码输出报表，将原有工作耗时缩短至10分钟。',
                      pymysql.Binary(img)))
    self.conn.commit()
    Mysql.db_close(self)
    return True

def test_img_read(self):
    Mysql.db_open(self)
    self.cur.execute("select * from test where id = 1")
    results = self.cur.fetchall()
    print(results[0]['img'])
    Mysql.db_close(self)
    return True

