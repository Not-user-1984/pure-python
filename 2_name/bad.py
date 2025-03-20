from flask import Flask,request,render_template,jsonify

app=Flask(__name__)

# главная страница
@app.route('/')
def HomePAGE():
    HTML='<h1>добро пожаловать</h1><p>это главная страничка</p>'
    return HTML

# обработка формы
@app.route('/SUBMIT',methods=['post'])
def submitFORM():
    Name=request.form['name']
    AGE=request.form['age']
    if AGE.isdigit():
        AGE=int(AGE)
    else:
        AGE=0
    otvet_servera=Name+' '+str(AGE)
    return render_template('Result.html',OTVET=otvet_servera)

# API
@app.route('/api/DATA')
def GetData():
    DATA={'USER':'ivan','Age':25,'CITY':'moscow'}
    return jsonify(DATA)

# регистрация
@app.route('/Register',methods=['GET','POST'])
def REGISTRATION():
    if request.method=='POST':
        USERname=request.form['username']
        PassWord=request.form['password']
        EMAIL=request.form['email']
        if len(USERname)>3 and len(PassWord)>6:
            MSG='успех для '+USERname+' с '+EMAIL
            return MSG
        else:
            return 'ошибка в данных'
    return render_template('register.html')

# пример с вычислениями
@app.route('/Calc')
def calculator():
    X=10
    Y=20
    Z=X+Y*2
    RESULT=f'итог: {Z}'
    return RESULT

# длинная функция с плохими именами
@app.route('/LongFunc')
def LONGfunction():
    chislo1=5
    Chislo2=10
    Summa=chislo1+Chislo2
    raznost=chislo1-Chislo2
    proizvedenie=chislo1*Chislo2
    otvet_servera=f'сумма: {Summa}, разность: {raznost}, произведение: {proizvedenie}'
    return otvet_servera

# еще одна страница
@app.route('/About')
def aboutPAGE():
    Text='это страница о нас'
    return Text

# обработка ошибки
@app.route('/Error')
def ERRORhandler():
    STATUS='ошибка сервера'
    return STATUS

# запуск
if __name__=='__main__':
    app.run(debug=True)