# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Путь к вашей базе данных
# app.config['SECRET_KEY'] = 'your_secret_key'
#
# db = SQLAlchemy(app)
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#
#         # Создание нового пользователя
#         new_user = User(name=name, email=email)
#
#         try:
#             # Добавление пользователя в базу данных
#             db.session.add(new_user)
#             db.session.commit()  # Подтверждение изменений в базе данных
#
#             # Проверка, произошла ли запись
#             if new_user.id:  # Если у пользователя есть id, то запись была успешной
#                 flash('Запись успешна!', 'success')
#             else:
#                 flash('Что-то пошло не так.', 'error')
#         except Exception as e:
#             db.session.rollback()  # Откат транзакции в случае ошибки
#             flash(f'Произошла ошибка: {e}', 'error')
#
#         return redirect(url_for('index'))
#
#     return render_template('index.html')
#
#
# if __name__ == '__main__':
#     db.create_all()  # Создание таблиц в базе данных
#     app.run(debug=True)
