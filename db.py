import psycopg2
import psycopg2.extras


conn_string = "host='localhost' dbname='city' user='dev' password='dev'"
con = None


def connect():
    global con
    con = psycopg2.connect(conn_string)


connect()


def fetchall_dict(*args):
    try:
        cur = con.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(*args)
        # print(cur.query.decode())
        return [row._asdict() for row in cur.fetchall()]

    except psycopg2.InterfaceError as err:
        print(err)
