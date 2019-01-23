import time, random, uuid

# 获取唯一标识
def getUUid():

    uid = uuid.uuid4().urn
    uid = uid[9:-1]
    uid = uid.replace('-', '')
    return uid