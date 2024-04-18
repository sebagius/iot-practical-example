import psycopg2
import time

DB_HOST_ADDR = 'localhost'
DB_HOST_PORT = 5432

class EdgeDatabase:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._conn = psycopg2.connect(database="iot",
                                      host=host,
                                      port=port,
                                      user='postgres',
                                      password='iot')
    def _convertUid(self, uid):
        return ':'.join('{:02x}'.format(b) for b in uid)

    def checkAuth(self, uid): # uid as bytes
        uidString = self._convertUid(uid)
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM allowed WHERE uid=%s", (uidString,))
        res = cur.fetchone()
        cur.close()
        return res != None

    def log(self, uid): #uid as bytes
        uidString = self._convertUid(uid)
        cur = self._conn.cursor()
        cur.execute("INSERT INTO access_log VALUES (%s, %s)", (uidString, time.time()*1000))
        self._conn.commit()
        cur.close()

    def getLogs(self, amount=10):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM access_log ORDER BY time;")
        res = cur.fetchmany(amount)
        cur.close()
        return res

    def getAllowed(self):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM allowed;")
        res = cur.fetchall();
        cur.close()
        return res;

    def addAllowed(self, uid): # uid is str
        cur = self._conn.cursor()
        cur.execute("INSERT INTO allowed VALUES (%s)", (uid,))
        self._conn.commit()
        cur.close()
        
    def removeAllowed(self, uid): # uid is str
        cur = self._conn.cursor()
        cur.execute("DELETE FROM allowed WHERE uid=%s;", (uid,))
        self._conn.commit()
        cur.close()

def test():
    testdb = EdgeDatabase(DB_HOST_ADDR, DB_HOST_PORT)
    testuid = bytearray([0xbb, 0x8c, 0x93])
    testdb.checkAuth(testuid)

if __name__ == "__main__":
    print("Running DB Tests....")
    test()

