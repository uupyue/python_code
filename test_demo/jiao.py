import json
import pymysql
import flask
import re

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "python_demo")
server=flask.Flask(__name__)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#登录接口
@server.route('/civp/getview/api/u/queryUnify',methods=['post','get'])
def queryUnify():
    tokenid = flask.request.values.get('tokenid')
    innerIfType = flask.request.values.get('innerIfType')
    cid= flask.request.values.get('cid')
    idNumber= flask.request.values.get('idNumber')
    realName= flask.request.values.get('realName')
    authCode= flask.request.values.get('authCode')
    Authorization_id = authCode[12:18]
    if tokenid and innerIfType and cid and idNumber and realName and authCode:
        sql1 = "select encrypt_data from encrypt_data where encrypt_data ='%s';"%tokenid
        result = cursor.execute(sql1)
        if result:
            typeList = ["A3"]
            if innerIfType in typeList:
                an = re.search('^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', cid)
                if an:
                    bn = re.search('^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$',idNumber)
                    if bn:
                        cn = re.search('[\u4e00-\u9fa5]',realName)
                        if cn:
                            dn = re.search('^[A-Za-z0-9]{50}$',authCode)
                            if dn:
                                sql2 = "select company from Authorization where Authorization_id='%s'"%Authorization_id
                                result = cursor.execute(sql2)
                                if result:
                                    sql3 = "select code from jiao_moke where name='%s'and mobile = '%s'and card_id ='%s';"%(realName,cid,idNumber)
                                    result = cursor.execute(sql3)
                                    if result:
                                        code = ''.join(cursor.fetchone())
                                        res = {"error_code": 1000,"code":code, "msg": "成功"}
                                    else:
                                        res = {"error_code": 1000,"code":98,"msg": "成功"}
                                else:
                                    res = {"error_code": 2007, "msg": "授权码不存在"}
                            else:
                                res = {"error_code": 2006, "msg": "授权码不合法"}
                        else:
                            res = {"error_code": 2005, "msg": "姓名不合法"}
                    else:
                        res = {"error_code": 2004, "msg": "身份证号不合法"}
                else:
                    res = {"error_code": 2003, "msg": "手机号码不合法"}
            else:
                res = {"error_code": 2002, "msg": "接口类型不合法"}
        else:
            res = {"error_code": 2001, "msg": "tokenid未授权"}
    else:
        res = {"error_code": 2000, "msg": "参数不正确"}
    return json.dumps(res, ensure_ascii=False)
server.run(host='0.0.0.0',port=8002,debug=True)  #启动服务
