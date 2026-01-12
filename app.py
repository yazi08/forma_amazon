import time
from waitress import serve
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from connect_db import get_data,to_db,del_db
from parametr import products_list,brands_list,marketplace_names_list,ysell_names_list,flavor_list,things_list,type_thing_list,net_weight_g_list,net_weight_oz_list
from parametr_cosmetics import *
from parametr_supplements import *
from parametr_rebate import brands_list_rebate,type_name
from werkzeug.security import generate_password_hash, check_password_hash
from work_test.db_connect import insert_data,get_user_email
from flask_login import LoginManager,login_user,login_required,logout_user
from user_login import UserLogin
from waitress import serve

app = Flask(__name__)
#app.config['SERVER_NAME'] = 'example.com'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/bfdghweyju,msmuy.uouu;ldtyjsnrb'

login_manager=LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print ('user_loader',user_id)
    user_login = UserLogin()
    return user_login.fromDB(user_id)


@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/requests',methods=['GET','POST'])
@login_required
def request_info():
    list_items = {}

    if request.method =='POST':

        asin = request.form.get("asin")

        sku = request.form.get("sku")
        table = request.form.get("tableSelect")
        print (asin,sku,table)

        sql =f"""SELECT *
                        FROM {table}
                        where asin='{asin}' and sku = '{sku}'"""

        try:
            df=get_data(sql,'az_reports')


            list_items = df.to_dict()
            print(list_items)
        except Exception as e:
            list_items = {'sku_asin': f'{e}'}





    return render_template('requests.html',list_items= list_items)




@app.route('/pet', methods=['GET','POST'])
@login_required
def form_pet():

    dict_items ={'products_list':products_list,
                 'brands_list':brands_list,
                 'marketplace_names_list':marketplace_names_list,
                 'ysell_names_list':ysell_names_list,
                 'flavor_list':flavor_list,
                 'things_list':things_list,
                 'type_thing':type_thing_list,
                 'net_weight_g':net_weight_g_list,
                 'net_weight_oz':net_weight_oz_list}

    if request.method == 'POST':


        #sku_asin =request.form.get('sku_asin')
        sku = request.form.get('sku')
        asin=request.form.get('asin')
        open_date_full=request.form.get('datetime_picker')
        open_date = open_date_full[:10]
        product=request.form.get('product')
        flavor=request.form.get('flavor')
        thing=request.form.get('thing')
        type_thing = request.form.get('type_thing')
        net_weight_g=request.form.get('net_weight_g')
        net_weight_oz = request.form.get('net_weight_oz')
        vine=request.form.get('vine')
        stack=request.form.get('stack')
        pets=request.form.get('pets')
        brand = request.form.get('brand')
        name_marketplace = request.form.get('name_marketplace')
        name_ysell = request.form.get('name_ysell')
        channel = request.form.get('channel')


        print (open_date,type(open_date))
        df_dict = {'sku_asin':[sku.strip()+"_"+asin.strip()],
                   'sku': [sku.strip()],
                   'asin':[asin.strip()],
                   'open_date':[open_date],
                   'open_date_full': [pd.to_datetime(open_date_full).strftime('%Y-%m-%d %H:%M')],
                   'product':[product],
                   'flavor':[flavor],
                   'thing':[thing],
                   'type_thing': [type_thing],
                   'net_weight_g': [net_weight_g],
                   'net_weight_oz': [net_weight_oz],
                   'vine':[vine],
                   'stack':[stack],
                   'pet':[pets],
                   'brand':[brand],
                   'name_marketplace':[name_marketplace],
                   'name_ysell':[name_ysell],
                   'channel':[channel]}

        table_name = 'pets_directory_amazon'
        df = pd.DataFrame(df_dict)
        df['url'] = 'https://www.amazon.com/dp/'+ df['asin']
        print (df)
        to_db(df,table_name,'append','az_reports')

        # time.sleep(5)
        # sql =f"""SELECT *
        #                 FROM public.pets_directory_amazon
        #                 where asin='{asin}' and sku = '{sku}'"""
        #
        # try:
        #     df=get_data(sql,'az_reports')
        #     while len(df)==0:
        #         to_db(df, table_name, 'append', 'az_reports')
        #         print (df)
        #
        #
        #
        #
        # except Exception as e:
        #     print (e)



    return render_template('pet.html',dict_items=dict_items)



@app.route('/supplements', methods=['GET','POST'])
@login_required
def form_supplements():
    dict_items = {'products_list': products_list_suppl,
                  'flavor_list':flavor_list_suppl,
                  'serving_size_list':serving_size_list_suppl,
                  'form_thing_list':form_thing_list_suppl,
                  'type_thing_list':type_thing_list_suppl,
                  'type_package_list':type_package_list_suppl,
                  'pack_q_ty_list':pack_q_ty_list_suppl,
                  'net_weight_g_list':net_weight_g_list_suppl,
                  'net_weight_oz_list': net_weight_oz_list_suppl,
                  'brands_list': brands_list_suppl ,
                  'marketplace_names_list': marketplace_names_list_suppl,
                  'ysell_names_list': ysell_names_list_suppl ,
                  'things_list': things_list_suppl , }


    if request.method == 'POST':
        # sku_asin =request.form.get('sku_asin')
        sku = request.form.get('sku')
        asin = request.form.get('asin')
        open_date_full = request.form.get('datetime_picker')
        open_date = open_date_full[:10]
        product = request.form.get('product')
        flavor = request.form.get('flavor')
        thing = request.form.get('thing')
        serving_size = request.form.get('serving_size')
        form_thing=request.form.get('form_thing')
        type_thing = request.form.get('type_thing')
        type_package = request.form.get('type_package')
        pack_q_ty=request.form.get('pack_q_ty')
        net_weight_g = request.form.get('net_weight_g')
        net_weight_oz = request.form.get('net_weight_oz')
        vine = request.form.get('vine')
        stack= request.form.get('stack')
        sugar_free=request.form.get('sugar_free')
        vegan = request.form.get('vegan')

        brand = request.form.get('brand')
        name_marketplace = request.form.get('name_marketplace')
        name_ysell = request.form.get('name_ysell')
        channel = request.form.get('channel')

        print(open_date, type(open_date))
        df_dict = {'sku_asin': [sku.strip() + "_" + asin.strip()],
                   'sku': [sku.strip()],
                   'asin': [asin.strip()],
                   'open_date': [open_date],
                   'open_date_full': [pd.to_datetime(open_date_full).strftime('%Y-%m-%d %H:%M')],
                   'product': [product],
                   'flavor':[flavor],
                   'thing': [thing],
                   'serving_size':[serving_size],
                   'form_thing':[form_thing],
                   'type_thing': [type_thing],
                   'type_package':[type_package],
                   'pack_q_ty':[pack_q_ty],
                   'net_weight_g': [net_weight_g],
                   'net_weight_oz': [net_weight_oz],
                   'vine': [vine],
                   'stack':[stack],
                   'sugar_free':[sugar_free],
                   'vegan':[vegan],
                   'brand': [brand],
                   'name_marketplace': [name_marketplace],
                   'name_ysell': [name_ysell],
                   'channel': [channel]}

        table_name = 'supplements_directory_amazon'
        df = pd.DataFrame(df_dict)
        df['url'] = 'https://www.amazon.com/dp/' + df['asin']
        print(df)
        to_db(df, table_name, 'append', 'az_reports')



    return render_template('supplements.html',dict_items=dict_items)




@app.route('/cosmetics', methods=['GET','POST'])
@login_required
def form_cosmetics():
    dict_items = {'products_list': products_list_cosmetic ,
                  'brands_list': brands_list_cosmetic ,
                  'marketplace_names_list': marketplace_names_list_cosmetic,
                  'ysell_names_list': ysell_names_list_cosmetic ,
                  'things_list': thing_list_cosmetic ,
                  'type_thing': type_thing_cosmetic ,
                  'net_weight_g': net_weight_g_list_cosmetic ,
                  'net_weight_oz': net_weight_oz_list_cosmetic }

    if request.method == 'POST':
        # sku_asin =request.form.get('sku_asin')
        sku = request.form.get('sku')
        asin = request.form.get('asin')
        open_date_full = request.form.get('datetime_picker')
        open_date = open_date_full[:10]
        product = request.form.get('product')
        thing = request.form.get('thing')
        type_thing = request.form.get('type_thing')
        net_weight_g = request.form.get('net_weight_g')
        net_weight_oz = request.form.get('net_weight_oz')
        vine = request.form.get('vine')
        brand = request.form.get('brand')
        name_marketplace = request.form.get('name_marketplace')
        name_ysell = request.form.get('name_ysell')
        channel = request.form.get('channel')

        print(open_date, type(open_date))
        df_dict = {'sku_asin': [sku.strip() + "_" + asin.strip()],
                   'sku': [sku.strip()],
                   'asin': [asin.strip()],
                   'open_date': [open_date],
                   'open_date_full': [pd.to_datetime(open_date_full).strftime('%Y-%m-%d %H:%M')],
                   'product': [product],
                   'thing': [thing],
                   'type_thing': [type_thing],
                   'net_weight_g': [net_weight_g],
                   'net_weight_oz': [net_weight_oz],
                   'vine': [vine],
                   'brand': [brand],
                   'name_marketplace': [name_marketplace],
                   'name_ysell': [name_ysell],
                   'channel': [channel]}

        table_name = 'cosmetics_directory_amazon'
        df = pd.DataFrame(df_dict)
        df['url'] = 'https://www.amazon.com/dp/' + df['asin']
        print(df)
        to_db(df, table_name, 'append', 'az_reports')



    return render_template('cosmetics.html',dict_items=dict_items)




@app.route('/delete_table', methods = ['GET','POST'])
@login_required
def delete_table():
    dict_items = {}
    if request.method =='POST':
        asin = request.form.get('asin')
        sku = request.form.get('sku')
        db_table = request.form.get('db_table')
        print (asin,sku,db_table)

        dict_items = {'asin': [asin],
                      'sku': [sku],
                      'db_table':[db_table]}


        sql_string = f"""delete from public.{db_table} where asin='{asin}' and sku='{sku}'"""
        del_db(sql_string,'az_reports')




    return render_template('delete_asin_sku.html',dict_items=dict_items)




@app.route('/create_product', methods = ['GET','POST'])
@login_required
def create_name_product():
    dict_items ={}

    if request.method =='POST':
        product = request.form.get('product')
        name_market_place = request.form.get('name_market_place')
        brand = request.form.get('brand')
        name_ysell = request.form.get('name_ysell')



        try:
            dict_items = {'product':[product],
                          'name_market_place':[name_market_place],
                          'brand':[brand],
                          'name_ysell':[name_ysell]}


        except:
            None




    return render_template('create_product.html',dict_items=dict_items)





@app.route('/rebate', methods=['GET','POST'])
@login_required
def form_rebate():
    dict_items = {
                  'brands_list': brands_list_rebate,'type':type_name,
                   }
    if request.method == 'POST':
        sku = request.form.get('sku')
        asin = request.form.get('asin')
        open_date_full = request.form.get('datetime_picker')
        open_date = open_date_full[:10]
        rebate_q = request.form.get('rebate_q')
        rebate_vallue = request.form.get('rebate_vallue')
        brand = request.form.get('brand')
        type_rebaid = request.form.get('type')


        print(open_date, type(open_date))
        df_dict = {
                   'sku': [sku.strip()],
                   'asin': [asin.strip()],
                   'open_date': [open_date],
                   'open_date_full': [pd.to_datetime(open_date_full).strftime('%Y-%m-%d %H:%M')],
                   'rebate_q': [int(rebate_q.strip())],
                   'rebate_vallue': [float(rebate_vallue.strip().replace(',','.'))],
                    'type':[type_rebaid.strip()],
                    'brand': [brand.strip()]}

        table_name = 'rebate_directory_amazon'
        df = pd.DataFrame(df_dict)
        df['url'] = 'https://www.amazon.com/dp/' + df['asin']
        print(df)
        to_db(df, table_name, 'append', 'az_reports')

        time.sleep(2)
        sql_list = f"""SELECT *
	                    FROM public.rebate_directory_amazon
	                    where asin='{asin}' and sku = '{sku}' and open_date='{open_date}' and type='{type_rebaid}'
	                    """
        print(sql_list)
        try:
            df=get_data(sql_list,'az_reports')


            list_items = df.to_dict()
            print(list_items)
        except Exception as e:
            list_items = {'sku_asin': f'{e}'}

        dict_items['list_items']=list_items
    return render_template('rebate.html', dict_items=dict_items)


@app.route('/login', methods=['GET','POST'])
def form_login():
    if request.method=='POST':
        print ('Попытка входа')
        user=get_user_email(request.form.get('email'))
        if user and check_password_hash(user[3],request.form.get('password')):
            userlogin=UserLogin().create(user)
            print (userlogin)
            login_user(userlogin)
            return redirect(url_for('home'))

        flash('неверный логин или пароль','error')
        print('неверный логин или пароль')
    return render_template('login.html')


# @app.route('/register', methods=['GET','POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         password_repeat = request.form.get('password_repeat')
#         if password == password_repeat:
#             hash = generate_password_hash(password)
#             db_data=insert_data(name, email, hash)
#             print (db_data)
#
#             if db_data:
#                 flash('Регистрация прошла успешно','success')
#                 return redirect(url_for('form_login'))
#
#             else:
#                 flash('Ошибка регистрации','error')
#
#
#         else:
#             flash('Пароли не совпадают', 'error')
#
#     return render_template('register.html')

# @app.route('/logout')
# @login_required
# def log_out():
#     logout_user()
#     flash('вы вышли из аккаунта','success')
#     return redirect(url_for('form_login'))



if __name__ == '__main__':
    #app.run(host ='10.197.0.221',port='50333')
    serve(app, host='10.197.0.221', port=5001)
    #app.run(debug=True,host='127.0.0.1',port='5001')
    #app.run(debug=True)