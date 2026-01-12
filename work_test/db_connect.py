
import psycopg2





# SELECT pid, usename, datname, client_addr, state, query, backend_start
# FROM pg_stat_activity
# WHERE state <> 'idle';
#
#
#
#
# SELECT pg_terminate_backend('5888');
HOST = '10.197.0.221'
DATABASE='az_reports'
USER='postgres'
PASSWORD='lPmitR2Ah#yJ2j%*'

def get_db_connection():
    conn = psycopg2.connect(host=HOST,
                            database=DATABASE,
                            user=USER,
                            password=PASSWORD)
    return conn




def get_select_db(sql_string):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql_string)
        data=cur.fetchall()
        return data
    except Exception as e:
        print ('Error get_select_db',e)

    finally:
        cur.close()
        conn.close()




def create_table(sql_string):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Выполняем запрос
        cur.execute(sql_string)
        conn.commit()
    except Exception as e:
        print ('Error create_table',e)

    finally:
        cur.close()
        conn.close()



def insert_data(username,email,psw):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Выполняем запрос
        sql_string= """
                    INSERT INTO users (username, email,psw) 
                    VALUES (%s, %s,%s);
                    """
        cur.execute(sql_string, (username, email,psw))
        conn.commit()
        return True

    except Exception as e:
        print ('Error create_table',e)
        return False
    finally:
        cur.close()
        conn.close()




def get_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql_string = f"""select * from public.users where id={user_id} limit 1"""
        cur.execute(sql_string)
        data = cur.fetchone()
        if not data:
            print ('Пользователь не найден')
            return False

        return data

    except Exception as e:
        print('Error get_user', e)

    finally:
        cur.close()
        conn.close()

    return False


def get_user_email(user_email):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sql_string = f"""select * from public.users where email='{user_email}' limit 1"""
        print (sql_string)
        cur.execute(sql_string)
        data = cur.fetchone()
        print(data)
        if not data:
            print ('Пользователь не найден')
            return False

        return data

    except Exception as e:
        print('Error get_user', e)

    finally:
        cur.close()
        conn.close()

    return False



# """
#     CREATE TABLE IF NOT EXISTS users (
#         id SERIAL PRIMARY KEY,
#         username VARCHAR(50) NOT NULL,
#         email VARCHAR(100) NOT NULL UNIQUE,
#         psw VARCHAR(100) NOT NULL,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     );
#     """