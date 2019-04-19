import json
import pymysql
import flask

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "python_demo")
server=flask.Flask(__name__)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#登录接口
@server.route('/login',methods=['post','get'])
def login():
    uname=flask.request.values.get('username')
    passwd=flask.request.values.get('passwd')
    # print(uname,passwd)
# 使用 execute()  方法执行 SQL 查询
    if uname and passwd:
        sql = "select user_name,password from user where user_name='%s'" \
          " and password='%s';" % (uname, passwd)
        result = cursor.execute(sql)
        if result:
            res = {"error_code": 1000, "msg": "登录成功"}
        else:
            res = {"error_code": 3001, "msg": "帐号/密码错误"}
    elif uname:
        res = {"error_code": 3002, "msg": "passwd必填参数未填"}
    elif passwd:
        res = {"error_code": 3003, "msg": "uname必填参数未填"}

    return json.dumps(res, ensure_ascii=False)





server.run(host='0.0.0.0',port=8889,debug=True)  #启动服务

