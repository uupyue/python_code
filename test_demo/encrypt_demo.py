import hashlib
import json
import pymysql
import flask
db = pymysql.connect("localhost", "root", "123456", "python_demo")
server=flask.Flask(__name__)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
#登录接口
@server.route('/encrypt',methods=['post'])
def encrypt():
    type=flask.request.values.get('type')
    data=flask.request.values.get('data')
    if type and data:
        #查询数据是否存在
        sql = "select encrypt_data from encrypt_data where type='%s'" \
          " and data='%s';" % (type, data)
        #sql查询返回行数
        result = cursor.execute(sql)
        #存在加密后数据直接返回值
        if result:
            # 列表转字符串
            encrypt_data = ''.join(cursor.fetchone())
            res = {"error_code": 1000, "data":encrypt_data,"msg": "加密成功"}
        #不存在加密后数据，加密后插入数据库再返回值
        else:
            #md5加密数据
            md5 = hashlib.md5()
            key= type +data
            md5.update(key.encode('utf-8'))
            encrypt_data=md5.hexdigest()
            sql = """INSERT INTO `encrypt_data` ( `type`, `data`, `encrypt_data`)
             VALUES ('%s', '%s', '%s');"""%(type,data,encrypt_data)
            # print(sql)
            try:
                #插入加密后的数据
                cursor.execute(sql)
                db.commit()
            except:
                # 插入异常处理
                db.rollback()
            res = {"error_code": 3001,"data":encrypt_data,"msg": "加密成功"}
    elif type:
        res = {"error_code": 3002, "msg": "data必填参数未填"}
    elif data:
        res = {"error_code": 3003, "msg": "type必填参数未填"}

    return json.dumps(res, ensure_ascii=False)
server.run(host='0.0.0.0',port=8001,debug=True)  #启动服务
