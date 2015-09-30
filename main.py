# coding=utf-8
__author__ = 'kk'
__localhost__ = ""
__testPort__ = 27017

from flask import Flask, url_for
from flask import render_template
from flask import Markup
from flask import request
from flask import flash
from flask import send_from_directory as send

# from multiprocessing import Process
import soketService

import thread

import json

app = Flask(__name__)

ids = {'leader1':'1','member1':'1','member2':'2','member3':'3','member4':'4'}
uinfo = [{'id':'0001','name':'leader1','head':'img1.jpg','level':'1'},  \
         {'id':'0002','name':'member1','head':'img2.jpg','level':'0'},  \
         {'id':'0003','name':'member2','head':'img3.jpg','level':'0'},  \
         {'id':'0004','name':'member3','head':'img4.jpg','level':'0'},  \
         {'id':'0005','name':'member4','head':'img5.jpg','level':'0'}]
musics = [{'id':'444','name':u'这是mp3'.encode('utf-8'),'file':'13.mp3'},{'id':'555','name':u'这是wav'.encode('utf-8'),'file':'13.wav'}]

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.txt', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>/')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

def valid_login(id, pw):
    return ids[id] == pw

#username=leader1&password=2
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # .get('abc','default value')
        print request.form

        if valid_login(request.form['username'],
                       request.form['password']):
            return json.dumps({'ret':1,'val':0,'teams':[{'id':'1024','name':u'团子合奏'.encode('utf-8')},{'id':'0208','name':u'团子合奏2'.encode('utf-8')}]},ensure_ascii=False,encoding='utf-8')
        else:
            return json.dumps({'ret':0,'val':u'密码或账户错误'.encode('utf-8')},ensure_ascii=False,encoding='utf-8')
    return json.dumps({'ret':0,'val':u'这个接口用post啊汾蛋。。。。'.encode('utf-8')},ensure_ascii=False,encoding='utf-8')

#1024
@app.route('/team/<teamId>/', methods=['POST', 'GET'])
def get_team_item(teamId):
    error = None
    if request.method == 'GET':
        if teamId == '1024':
            obj = dict()
            obj['ret'] = 1
            obj['val'] = 0
            obj['members'] = uinfo
            obj['musics'] = musics
            return json.dumps(obj,ensure_ascii=False,encoding='utf-8')
        else:
            return json.dumps({'ret':0,'val':u'该团不存在，现在只有1024'.encode('utf-8')},ensure_ascii=False,encoding='utf-8')
    return json.dumps({'ret':0,'val':u'这个接口用get啊汾蛋。。。。'.encode('utf-8')},ensure_ascii=False,encoding='utf-8')

@app.route('/music/<name>')
def music(name):
    return send('C:\\sspider\\music\\',name)

@app.route('/pic/<name>')
def pic(name):
    return send('C:\\sspider\\pic\\',name)

@app.errorhandler(404)
def not_found(error):
    return u'注意链接拼写。。。404拉'.encode('utf-8')



with app.test_request_context():pass
#     print url_for('index')
#     print url_for('login')
#     print url_for('login', next='/')  ##/login?next=%2F
#     print url_for('profile', username='John Doe')
#     print url_for('music', f='13.mp3')
#     print url_for('music', f='13.wav')

def sk():
    addr = (__localhost__, __testPort__)
    #购置TCPServer对象，
    server = soketService.ThreadingTCPServer(addr, soketService.baseRequestHandlerr,bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    #启动服务监听
    print 'start,port 27017'
    server.serve_forever()

if __name__ == '__main__':
    # p=Process(target=sk).start()

    #pro = subprocess.Popen("python D:\\PyProjects\\sspider\\soketService.py", stdout=subprocess.PIPE,shell = True)

    thread.start_new_thread(sk, ())
    #pro = subprocess.Popen("python D:\\PyProjects\\sspider\\soketService.py", stdout=subprocess.PIPE,shell = True)
    app.run(host='0.0.0.0', debug=False)


    # ###梯度下降法，求解无约束优化问题最简单和最古老的方法
    # f = lambda x : x**3
    # x = 2
    # step = 0.01 #步长越小收敛速度越慢，但步长过大有可能跳过不保证每次迭代都减少，甚至不一定收敛
    # lossChange = f(x)
    # lossed = f(x)
    # print 'x:', x, 'lossChange:', lossChange, 'loss:', lossed
    # while lossChange > 0.00000001: #当变化小到一定程度是认为是局部最小
    #     x = x - step * 3 *( x**2) #减的是梯度方向上的变化
    #     lossChange = lossed - f(x)
    #     lossed = f(x)
    #     print 'x:', x, 'lossChange:', lossChange, 'loss:', lossed
    # print x
    # print f(x)