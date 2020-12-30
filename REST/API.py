from flask import Flask, jsonify
import pyodbc
from flask import Flask, jsonify
from flask_restful import Api,Resource

conn=pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=HIMANSHUMEENA0;'
                        'Database=information;'
                        'Trusted_Connection=yes;')


cursor=conn.cursor()
app=Flask(__name__)


@app.route('/')
def first():
    return "WELCOME TO API"


@app.route('/search', methods=['GET'])
def get(self):
    cursor.execute("""select*from employee where name ='joe' """)
    employee = cursor.fetchall()
    result ={"name":employee[0][0],'lastName':employee[0][1],'email':employee[0][2],'phone':employee[0][3],'dob':employee[0][4],'adress':employee[0][5]}
    return jsonify(result)



@app.route('/searchNEW/<n>', methods=['GET'])
def get_n(n):
     cursor.execute("""select*from employee where E_number ='{}'""".format(n))
     employee = cursor.fetchall()
     result  = {"name" : employee[0][0], 'lastName' : employee[0][1], 'email' : employee[0][2], 'phone' : employee[0][3],'dob' : employee[0][4], 'adress' : employee[0][5],'E_number':employee[0][6]}
     return jsonify(result)


if __name__=="__main__":
    app.run(debug=True)

