#-*- coding: utf-8 -*-

from flask import Flask,jsonify, request
import json

from src.service import user,table,screen

import time

app = Flask(__name__)

from flask_cors import CORS
CORS(app, supports_credentials=True)
# ToDo 添加app.after 添加状态码、返回信息 500:服务器内部错误 301：其他问题 302：用户信息有误 400： 参数问题
#--------------------------------------------用户管理---------------------------#

#登录
@app.route("/login",methods=['POST','GET'])
def login():
    login_name = request.form['login_name']
    password = request.form['password']
    ip = request.remote_addr
    userinfo = user.login(login_name,password,ip)
    r = None
    if (userinfo == None):
        r=erro('账号密码错误')
    else:
        r=success(userinfo)
    return r

#验证码获取/更新
@app.route("/getCaptcha",methods=['POST','GET'])
def getCaptcha():
    ip = request.remote_addr
    r = user.getCaptcha(ip)
    return success(r)

#--------------------------------------------数据管理---------------------------#

# 查询目录结构
@app.route("/table/find_tree",methods=['POST','GET'])
def findTree():

    email = request.email
    data = table.findTree(email)
    if(data == -1):
        return erro('服务器内部错误')
    else:
        return success(data)

# 创建文件夹
@app.route("/table/createFolder",methods=['POST','GET'])
def createFolder():

    email = request.email
    folder_name = request.form.get('folder_name')

    # 文件夹是否存在
    folder_count = table.findFolderCountByUser(email, folder_name)
    if (folder_count != 0):
        if(folder_count == -1):
            return erro('内部错误')
        else:
            return erro('文件夹已存在')


    # 创建文件夹
    r = table.createFolder(email, folder_name)
    if (r < 1):
        if(r == -1):
            return erro('内部错误')
        else:
            return erro('文件夹已存在')

    # 查询新目录

    return success(None)

# 创建表
@app.route("/table/createTable", methods=['POST', 'GET'])
def createTable():

    email = request.email
    json_data = request.json_data

    folder_name = json_data['folder_name']
    columns = json_data['columns']
    table_name = json_data['table_name']
    note = json_data['note']
    head = json_data['head']



    # 文件夹是否存在
    folder_count = table.findFolderCountByUser(email, folder_name)
    if (folder_count < 1):
        if (folder_count == -1):
            return erro('内部错误')
        else:
            return erro('文件夹不存在')

    # 创建表
    r = table.createTable(email, folder_name, table_name, columns, note, head)
    if (r < 1):
        if (r == -1):
            return erro('内部错误')
        else:
            return erro('创建失败')

    # 查询新目录

    return success(None)

# 删除文件夹
@app.route("/table/del_folder",methods=['POST','GET'])
def delFolder():

    email = request.email
    folder_name = request.form.get('folder_name')

    # 删除文件夹及表格
    r = table.delFolder(email, folder_name)
    if (r == -1):
       return erro('内部错误')
    else:
       return success({})

# 删除表
@app.route("/table/del_table", methods=['POST', 'GET'])
def delTable():

    email = request.email
    json_data = request.json_data

    folder_name = json_data['folder_name']
    table_names = json_data['table_names']

    # 删除
    r = table.delTables(email, folder_name,table_names)
    if (r == -1):
        return erro('内部错误')
    else:
        return success({})

# 导入数据
@app.route("/table/input_data", methods=['POST'])
def inputData():
    email = request.email

    json_data = request.json_data
    folder_name = json_data['folder_name']
    table_name = json_data['table_name']
    up_data = json_data['up_data']
    up_data = json.loads(up_data)


    # todo 参数校验

    r = table.input_data(email, folder_name, table_name, up_data)

    if(r==-1): return erro('erro')
    return success('success')

# 获取数据
@app.route("/table/get_table", methods=['GET'])
def getTable():
    email = request.email
    r = request
    real_name = request.args.get('real_name')
    start = request.args.get('start')
    start = int(start)
    end = request.args.get('end')
    end = int(end)

    r = table.getTable( real_name, start, end)

    if(r==-1): return erro('erro')
    return success(r)

#-------------------------图表管理--------------------------#
# 获取数据
@app.route("/chart/get_tree", methods=['GET'])
def getChartTree():
    email = request.email
    r = request
    real_name = request.args.get('real_name')
    start = request.args.get('start')
    start = int(start)
    end = request.args.get('end')
    end = int(end)

    r = table.getTable( real_name, start, end)

    if(r==-1): return erro('erro')
    return success(r)

#---------------------------大屏幕---------------------#

# 获取数据
@app.route("/screen/find_tree", methods=['GET'])
def getScreenTree():
    email = request.email

    r = screen.findTree( email )

    if(r==-1): return erro('erro')
    return success(r)


# 创建文件夹
@app.route("/screen/create_folder",methods=['POST','GET'])
def createScreenFolder():

    email = request.email
    folder_name = request.form.get('folder_name')

    # 文件夹是否存在
    folder_count = screen.findFolderCountByUser(email, folder_name)
    if (folder_count != 0):
        if(folder_count == -1):
            return erro('内部错误')
        else:
            return erro('文件夹已存在')


    # 创建文件夹
    r = screen.createFolder(email, folder_name)
    if (r < 1):
        if(r == -1):
            return erro('内部错误')
        else:
            return erro('文件夹已存在')

    # 查询新目录

    return success(None)

# 创建大屏幕
@app.route("/screen/create_screen", methods=['POST', 'GET'])
def createScreen():

    email = request.email
    json_data = request.json_data

    folder_name = json_data['folder_name']
    screen_name = json_data['screen_name']
    note = json_data['note']
    option = json_data['option']
    img = json_data['img']



    # 文件夹是否存在
    folder_count = screen.findFolderCountByUser(email, folder_name)
    if (folder_count < 1):
        if (folder_count == -1):
            return erro('内部错误')
        else:
            return erro('文件夹不存在')

    # 创建表
    r = screen.createScreen(email, folder_name, screen_name, option, img, note )
    if (r < 1):
        if (r == -1):
            return erro('内部错误')
        else:
            return erro('创建失败')

    # 查询新目录

    return success(None)

# 删除文件夹
@app.route("/screen/del_folder",methods=['POST','GET'])
def delScreenFolder():

    email = request.email
    folder_name = request.form.get('folder_name')

    # 删除文件夹及表格
    r = screen.delFolder(email, folder_name)
    if (r == -1):
       return erro('内部错误')
    else:
       return success({})

# 删除表
@app.route("/screen/del_screen", methods=['POST', 'GET'])
def delScreen():

    email = request.email
    json_data = request.json_data

    folder_name = json_data['folder_name']
    table_names = json_data['table_names']

    # 删除
    r = screen.delScreen(email, folder_name,table_names)
    if (r == -1):
        return erro('内部错误')
    else:
        return success({})


#-------------------------------拦截器-----------------------#

# 拦截尝试连接请求
@app.before_first_request
def before_first_request():
   pass

# 处理请求前
@app.before_request
def before_request():
    path = request.path

    if( request.method != 'OPTIONS' and path != '/login') :

        # no.1 获取header
        token = request.headers.get('user-token')

        # no.2查询用户、保存用户信息
        u = user.findUserByToken(token)
        if (u == None):
            return erro('用户信息异常'), 302
        else:
            email = u['email']
            request.__setattr__('email',email)
            request.__setattr__('user', u)

        # no.3 如果有json参数 格式化
        try:

            data = request.get_data()
            code = data.decode("utf-8")

            json_data = json.loads(code)
            request.__setattr__('json_data', json_data)

        except Exception as e:
            print('param not a dict')




# todo @app.after_request 处理异常


@app.route("/test", methods=['GET'])
def test():

    r = request.remote_addr
    return jsonify({})


def success(data,msg='success'):
    return jsonify({'code': 200, 'data': data, 'msg': msg})
def erro(msg='error'):
    return jsonify({'code': 400, 'msg': msg})


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=True)
    #mysql.createTable('a','r')
    #mysql.delTable('a')
    #print (time.time())
