from src.util import mysqlPool, mUtil
import time, random, uuid



#获取验证码
def getCaptcha(ip):
    code = random.randint(1000, 9999)
    r = mysqlPool.insert_or_update('captcha', {'code': {'val' :code, 'type': 's'}, 'ip': {'val': ip, 'type': 's'}})
    if(r):
        return code
    else:
        return False
#登录
def login(login_name, password, ip):

    token = mUtil.getUUid()

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)
    print(ip,token,login_name,password)
    try:

        r = cursor.execute("update user set last_login_ip=%s, token=%s  where email=%s and psw=%s ", [ip, token, login_name, password])

        if(r):
            cursor.execute("select * from user where email=%s and psw=%s ", [login_name, password])
            data = cursor.fetchone()

            print("Database version : %s " % data)
            return data


    except Exception as e:
        import traceback
        traceback.print_exc()
        conn.rollback()  # 事务回滚
        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()

    return None


# 根据token获取user
def findUserByToken(token):

    conn = mysqlPool.getConn()
    cursor = conn.cursor(cursor=mysqlPool.cur)

    try:
        # 根据token查询用户
        cursor.execute("select * from user where token=%s", [token])
        user = cursor.fetchone()

    except Exception as e:
        import traceback
        traceback.print_exc()
        print('事务处理失败', e)
    finally:
        cursor.close()
        conn.close()

    return user

#注册
