import pymysql as ps

class MysqlController:

    def __init__(self, host="j3d103.p.ssafy.io", user="root", password="1q2w3e4r", db="ssafy"):
        self.conn = ps.connect(host=host, user=user, password=password, db=db, charset='utf8')
        self.curs = self.conn.cursor(ps.cursors.DictCursor) # Dictionary 커서

    def execute(self, sql):
        self.curs.execute(sql)
        return self.curs.fetchall()

    def disconnect(self):
        self.conn.close()