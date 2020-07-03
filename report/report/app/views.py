from django.shortcuts import render
import time
from app import mysql
import xlwt
import io
import base64

sql = mysql.Mysql()
personnel_list = sql.get_personnel_list()
team_list = sql.get_team_list()
score_list = sql.get_score_list()
score_new = {'t_num': 0,
         't_name': '',
         'judges': '',
         'date': '',
         'p_name': '',
         'score_all': 0,
         'score_1': 0,
         'score_2': 0,
         'score_3': 0,
         'score_4': 0,
         'score_5': 0,
         'score_6': 0,
         'score_7': 0,
         'score_8': 0,
         'score_9': 0,
         'score_10': 0}
score = score_new
Judges = ''

#进入首页
def index(request):
    global Judges
    global team_list
    global score
    global score_new
    score = score_new
    return render(request, 'index.html', context={'team_list': team_list, 'Judges': Judges})

#设置评委
def setJudges(request):
    global Judges
    global team_list
    if request.POST:
        Judges = request.POST['Judges']
    return render(request, 'index.html', context={'team_list': team_list, 'Judges': Judges})

#首页点击队伍进入打分画面
def scoring(request):
    global Judges
    global team_list
    global personnel_list
    global score
    global score_new
    score = score_new
    photo_list = []
    if request.POST:
        team = request.POST['team']
    for i in team_list:
        if i[0] == team:
            sql_1 = mysql.Mysql()
            # 确认是否已存在评分，存在则读取，不存在则初始化
            score_team_judges = sql_1.get_score(team, Judges)
            if score_team_judges:
                score = score_team_judges
                score['date'] = time.strftime("%Y-%m-%d", time.localtime())
            else:
                score['t_num'] = i[1]
                score['t_name'] = i[0]
                score['judges'] = Judges
                score['date'] = time.strftime("%Y-%m-%d", time.localtime())
    for i in personnel_list:
        if i['team'] == team:
            photo_list.append([i['name'], base64.b64encode(i['image'])])
    return render(request, 'scoring.html', context={'photo_list': photo_list, 'score': score})

#打分画面点击照片获取详细信息
def personnel_info(request):
    global Judges
    global personnel_list
    global score
    isfollow = False
    if request.POST:
        name = request.POST['name']
    for i in personnel_list:
        if i['name'] == name:
            if score['p_name'] == name:
                isfollow = True
            return render(request, 'scoring.html', context={'personnel_info': i, 'isfollow': isfollow})

#详细信息画面点关注
def follow(request):
    global score
    if request.POST:
        name = request.POST['name']
    if score['p_name'] == name:
        score['p_name'] = ''
        isfollow = False
    else:
        score['p_name'] = name
        isfollow = True
    for i in personnel_list:
        if i['name'] == name:
            return render(request, 'scoring.html', context={'personnel_info': i, 'isfollow': isfollow})

#提交评分
def scored(request):
    global score
    global Judges
    global team_list
    global score_list
    score_all = 0
    if request.POST:
        for i in range(1, 11):
            score['score_'+str(i)] = request.POST['score_'+str(i)]
            score_all += request.POST['score_'+str(i)]
        score[score_all] = score_all
    sql_1 = mysql.Mysql()
    #确认是否已存在评分，存在则修改，不存在则添加
    score_team_judges = sql_1.get_score(score['t_name'], score['judges'])
    if score_team_judges:
        sql_1.set_score(score)
    else:
        sql_1.add_score(score)

    score_list = sql_1.get_score_list()
    return render(request, 'index.html', context={'team_list': team_list, 'Judges': Judges})

#进入统计画面
def statistics(request):
    global score_list
    sql_1 = mysql.Mysql()
    score_list = sql_1.get_score_list()
    return render(request, 'statistics.html', context={'score_list': score_list})

#点击修改总分
def update(request):
    global score_list
    if request.POST:
        score_all = request.POST['score_all']
        team = request.POST['team']
        Judges = request.POST['Judges']
    sql_1 = mysql.Mysql()
    sql_1.set_score_all(team, Judges, score_all)
    score_list = sql_1.get_score_list()
    return render(request, 'statistics.html', context={'score_list': score_list,})

#导出表格
def excel(request):
    global score_list
    sql_1 = mysql.Mysql()
    score_list = sql_1.get_score_list()
    wb = xlwt.Workbook()
    wb.encoding = 'utf8'
    ws = wb.add_sheet('1')
    ws.write(0, 0, '组')
    ws.write(0, 1, '组名')
    ws.write(0, 2, '评委')
    ws.write(0, 3, '创建时间')
    ws.write(0, 4, '关注成员')
    ws.write(0, 5, '总分')
    ws.write(0, 6, '布局美观')
    ws.write(0, 7, '活跃气氛')
    ws.write(0, 8, '熟悉内容')
    ws.write(0, 9, '时间安排')
    ws.write(0, 10, '案例出彩')
    ws.write(0, 11, '逻辑清晰')
    ws.write(0, 12, '剖析深刻')
    ws.write(0, 13, '口齿清晰')
    ws.write(0, 14, '目光交流')
    ws.write(0, 15, '表现力强')
    a = 1
    for i in score_list:
        ws.write(a, 0, i['t_num'])
        ws.write(a, 1, i['t_name'])
        ws.write(a, 2, i['judges'])
        ws.write(a, 3, i['date'].strftime('%Y-%m-%d'))
        ws.write(a, 4, i['p_name'])
        ws.write(a, 5, i['score_all'])
        for j in range(1, 11):
            ws.write(a, 5+j, i['score_'+str(j)])
        a += 1
    sio = io.BytesIO()
    wb.save(sio)
    return render(request, 'statistics.html', context={'score_list': score_list, 'excel': sio.getvalue() })

