import time, random, uuid
def _time():
    print(time.time())


# json
def _json():
    a = {}
    a['d'] = 1
    print(a)

# if
def _if():
  if 2>8: print(True)
  else : print(False)
# for
def _for():

    n_list = [1,2,3]
    dict_list = {"a":0,"b":{"bb": 'b0'}, "c": [2,5,6]}

    for item in n_list:
        print(item)
    for i in range(len(n_list)):
        print(i)

    for key in dict_list:
        print(dict_list[key])

# class
class User:

    def __init__ (self, name):
        self.name = name
    def toJSON (self):
        r = {}
        r['name'] = self.name
        return r

def toJSON(user):
    r = user.toJSON()
    return r;
def user_list_print():
    u = User('luxiaojiang')
    u1 = User('luxiaojiang1')
    u2 = User('luxiaojiang2')

    u_l = [u, u1, u2];
    j = map(toJSON, u_l)

    print(list(j))

# String
def _string():
    s = 'sdf,'
    print(s[0:-1])

if __name__ == '__main__':
    a=None
