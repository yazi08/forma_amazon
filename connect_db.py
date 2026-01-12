import psycopg2
import pandas as pd
from sqlalchemy import create_engine
#from parameter import date_start,date_end,date_32


db ={"dbname" : "postgres",
"user" : "postgres",
"password" : "lPmitR2Ah#yJ2j%*",
"host" : "10.197.0.221",
"port" : "5432"
}





def con_db(dbname):
    try:
        connection = psycopg2.connect(user=db['user'], password=db['password'], host=db['host'], port=db['port'],
                                      dbname=dbname)
        print('Parameters are correct, data loading starts')
        cursor = connection.cursor()
        return connection, cursor
    except (Exception, psycopg2.Error) as error:
        print('Failed to connect:', error)
        return None, None

def get_data(sqlline,dbname):
    # sqlline = f"""select * FROM public.test_orders_amazon
    # where "PurchaseDate" between '{date_start}' and '{date_end}'
    # """
    #print (date_start,date_end)
    connection, cursor = None, None
    try:
        connection, cursor = con_db(dbname)
        if cursor:
            cursor.execute(sqlline)
            data = pd.DataFrame(cursor.fetchall())
            colnames = [desc[0] for desc in cursor.description]
            data.columns = colnames
            print('Data loading ends')
            return data
    except (Exception, psycopg2.Error) as error:
        print('Something broke:', error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print('Connection closed')



def del_db(sql_del,dbname):
    # sql_del = f"""DELETE FROM public.test_orders_amazon
    # WHERE "PurchaseDate" BETWEEN '{date_start}' and '{date_end}'
    # """
    connection, cursor = None, None
    try:
        connection, cursor = con_db(dbname)
        if cursor:
            cursor.execute(sql_del)
            connection.commit()  # Commit the transaction to apply changes
            print('Deletion completed')
    except (Exception, psycopg2.Error) as error:
        print('Something broke:', error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print('Connection closed')



def to_db(df,name_table,if_exists,dbname):  #amazon_attribution_performance if_exists{‘fail’, ‘replace’, ‘append’}
    db_uri = 'postgresql://' + db['user'] + ':' + db['password'] + '@' + db['host'] + ':' + db['port'] + '/' + dbname
    engine = create_engine(db_uri)
    df.to_sql(name_table, con=engine, if_exists=if_exists, index=False)




