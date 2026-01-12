# save this as app_test.py
from flask import Flask,url_for,session


#url_for - возвращает ссылку страницы

app = Flask(__name__)

@app.route("/")
def hello():
    print (url_for('hello'))
    return "Hello, World!"




@app.route("/test")
def test():
    print (url_for('test'))
    return "Hello, World!"


@app.route("/test_1/<user_name>")
def test_1(user_name):
    print (session)
    return f'user_name {user_name}'



if __name__=='__main__':
    app.run(debug=True)

    # db = {"dbname": "postgres",
    #       "user": "postgres",
    #       "password": "lPmitR2Ah#yJ2j%*",
    #       "host": "192.168.88.20",
    #       "port": "5432"
    #       }




# SELECT pid, usename, datname, client_addr, state, query, backend_start
# FROM pg_stat_activity
# WHERE state <> 'idle';
#
#
#
#
# SELECT pg_terminate_backend('5888');

# def get_db_connection():
#     conn = psycopg2.connect(host='192.168.88.20',
#                             database='az_reports',
#                             user='postgres',
#                             password='lPmitR2Ah#yJ2j%*')
#     return conn
#
# conn = get_db_connection()
# cur = conn.cursor()
# cur.execute("""SELECT invoice_id, status, from_date, to_date, invoice_date, amount, currency, start_date, end_date
# 	FROM public.aldico_invoice;""")
# books = cur.fetchall()
# print (books)
# cur.close()
# conn.close()