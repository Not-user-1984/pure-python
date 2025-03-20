from flask import Flask,request,render_template,jsonify
import os 

app=Flask(__name__)

# Главная страница
@app.route('/')
def HomePage():
    html='<h1>Добро пожаловать на сайт</h1><p>Это главная страница приложения на Flask</p>'
    return html

# Обработка формы
@app.route('/submit',methods=['POST'])
def submitForm():
  name=request.form['name']
  age=request.form['age']
  if age.isdigit():
        age=int(age)
  else:
      age=0
  result=name+' '+str(age)
  return render_template('result.html',Result=result)

# API эндпоинт
@app.route('/api/data')
def getData():
    data={'user':'Иван','age':25,'city':'Москва'}
    return jsonify(data)


# Регистрация пользователя
@app.route('/register',methods=['GET','POST'])
def Register():
    if request.method=='POST':
        password=request.form['password']
        email=request.form['email']
        if len(username)>3 and len(password)>6:
            msg='Регистрация успешна для '+username+' с email '+email
            return msg
        else:
            return 'Ошибка: короткое имя или пароль'
    return render_template('register.html')



@app.route('/longexample')
def longExample():
    x=10
    y=20
    z=x+y
    print("нарушение: длинная строка, нет пробела после операторанарушение: длинная строка, нет пробела после операторанарушение: длинная строка, нет пробела после операторанарушение: длинная строка, нет пробела после оператора")