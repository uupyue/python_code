# import logging
#
# logging.basicConfig(filename="test.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
import json

import flask
#1、启动一个服务
#2、接收到客户端传过来的数据
#3、登录、注册、支付
#4、返回数据

#1、
#2、mock 接口
#3、不想让别人直接操作你的数据库
import tools

server=flask.Flask(__name__)  #把当前这个python文件当做一个服务

import datetime

@server.route('/xiaojun')   #定义服务
def get_time():
    now=str(datetime.datetime.now())
    return "现在的时间是%s"%now

@server.route('/hailong')
def say_hello():
    return 'hello'

@server.route('/index')
def my_page():
    f=open('index.html',encoding="utf-8")
    res=f.read()
    f.close()
    return res

   # 连接数据库，从数据库中取值
@server.route('/login',methods=['post','get'])
def login():
    uname=flask.request.values.get('username')
    passwd=flask.request.values.get('passwd')
    #args这个方法就只能获取到URL里面传的参数
    #values这个方法不管你是在url里面传参数还是 K-V传的，都可以获取到
    if uname and passwd:
        sql="select username,passwd from app_myuser where username='%s'" \
            " and passwd='%s';"%(uname,passwd)
        result=tools.my_db(sql)
        if result:
            res={"error_code":1000,"msg":"登录成功"}
        else:
            res={"error_code":3001,"msg":"帐号/密码错误"}
    else:
        res={"error_code":3003,"msg":"必填参数未填，请查看接口文档"}
    return json.dumps(res,ensure_ascii=False)



server.run(host='0.0.0.0',port=8888,debug=True)  #启动服务
#host写成0.0.0.0的话，在一个局域网里面的人都可以访问了
#debug=True 加上它 就不需要重启了，改完代码他会自动重启
