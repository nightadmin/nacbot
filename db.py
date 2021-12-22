class DB:
    def __init__(self, path):
        self.path = path
    def find(self, user_id):
        f = open(f'{self.path}/db.json', 'r')
        f = eval(f.read())
        ans = []
        for q in f:
            if q["user_id"] == user_id:
                ans.append(q)
        return ans
    def remove(self, content):
        if self.find(content["user_id"]) != []:
            f = open(f'{self.path}/db.json', 'r')
            f = eval(f.read())
            for i in range(len(f)):
                if f[i]["user_id"] == content["user_id"]:
                    f.pop(i)
                    break
            fn = open(f'{self.path}/db.json', 'w')
            fn.write(str(f))
            fn.close()
    def write(self, content):
        user_id = content["user_id"]
        if self.find(user_id) != []:
            self.remove(content)
        f = open(f'{self.path}/db.json', 'r')
        f = eval(f.read())
        f.append(content)
        fn = open(f'{self.path}/db.json', 'w')
        fn.write(str(f))
        fn.close()
    def findall(self):
        f = open(f'{self.path}/db.json', 'r')
        f = eval(f.read())
        ans = []
        for q in f:
            ans.append(q["user_id"])
        return ans
db = DB(".")

def exists(user_id):
    res = db.find(user_id)
    if res != []:
        return res
    else:
        return False

def subscribe_need_start(user_id):
    ex = exists(user_id)
    if ex == False: return True
    if ex[0]["subscribe"] == False: return True
    return False
    