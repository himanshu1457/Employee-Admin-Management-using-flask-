import urllib

import pyodbc
from flask import Flask, render_template, request, redirect,session
import json
from urllib.request import urlopen
import os


conn=pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=HIMANSHUMEENA0;'
                        'Database=information;'
                        'Trusted_Connection=yes;')



cursor=conn.cursor()



app=Flask(__name__)
app.secret_key=os.urandom(24)

headings={"Name", "LastName", "email", "phone", "Dob", "Address"}

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/Home')
def Home():
    cursor.execute('select *from employee')
    data=[]
    for row in cursor :
        data.append(row)

    conn.commit()
    if 'user_email' in session:
        return render_template('Home.html', data=data)
    else:
        return redirect('/')


@app.route('/adminWindow')
def adminWindow():
    cursor.execute('select *from employee')
    data1 = []
    for row in cursor :
        data1.append(row)
    conn.commit()
    if 'user_email' in session:
        return render_template('adminWindow.html', data=data1)
    else:
        return redirect('/')


@app.route('/updatee',methods=['POST'])
def updatee():
    name = request.form.get('name')
    Lastname = request.form.get('last')
    email = request.form.get('email')
    PN = request.form.get('phone')
    dob = request.form.get('dob')
    address = request.form.get('address')
    cursor.execute("""Update employee set name='{}',lastName='{}',email='{}',PN='{}',dob='{}',address='{}' where name='{}'""".format(name,Lastname,email,PN,dob,address,name))
    conn.commit()
    return redirect('/Home')


@app.route('/delete/<name>',methods=['POST','GET'])
def delete(name):
    cursor.execute("""delete from employee where name='{}'""".format(name))
    conn.commit()
    return redirect('/Home')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('ee')
    password=request.form.get('pp')

    rrr=request.form.get('options')
    cursor.execute("""select*from logininformation where email like '{}' and password like '{}'""".format(email,password))
    employee=cursor.fetchall()
    print(employee)

    session['user_email'] = employee[0][0]

    if len(employee)>0 and rrr==None:
        return redirect('/adminWindow')
    elif len(employee)>0 and rrr!=None:
        return redirect('/Home')
    else:
        return redirect('/')



@app.route('/addUser', methods=['POST'])
def addUSer():
    eno= request.form.get('eno')
    name=request.form.get('n')
    Lastname = request.form.get('l')
    email = request.form.get('e')
    PN=request.form.get('p')
    dob=request.form.get('d')
    address=request.form.get('a')

    cursor.execute("""Insert into employee values('{}','{}','{}','{}','{}','{}','{}')""".format(name,Lastname,email,PN,dob,address,eno))

    conn.commit()
    return render_template("register.html", message="Hi ,'{}' you have been sucessfully register".format(name))

@app.route('/add', methods=['POST'])
def add():
    eno = request.form.get('eno')
    name=request.form.get('n')
    Lastname = request.form.get('l')
    email = request.form.get('e')
    PN=request.form.get('p')
    dob=request.form.get('d')
    address=request.form.get('a')

    cursor.execute("""Insert into employee values('{}','{}','{}','{}','{}','{}','{}')""".format(name, Lastname, email , PN, dob,address,eno))

    conn.commit()
    return redirect("/Home")



@app.route('/callAPI',methods=['GET'])
def callAPI():
    emo=request.form.get('En')
    print("eNumber")
    print(emo)
    url='http://127.0.0.1:5000/searchNew/4'
    url_req=urllib.request.urlopen(url)
    json_obj=json.load(url_req)
    name=json_obj.get("name")
    lname=json_obj.get("lastName")
    emailing=json_obj.get("email")
    phone=json_obj.get("phone")
    Dob=json_obj.get("dob")
    address=json_obj.get("adress")
    data4=[]

    data4.append(name)
    data4.append(lname)
    data4.append(emailing)
    data4.append(phone)
    data4.append(Dob)
    data4.append(address)
    print(data4)

    return render_template('Home.html',data=data4)

@app.route('/logout')
def logout():
    session.pop('user_email')
    return redirect('/')



if __name__=="__main__":
    app.run(debug=True)

