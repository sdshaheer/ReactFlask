from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Sdshafin@localhost/TestCases'
db = SQLAlchemy(app)
CORS(app)
app.app_context().push()


class Test(db.Model):
    testId = db.Column(db.Integer,primary_key = True)
    testName = db.Column(db.String(100),nullable = False)
    testTime = db.Column(db.Integer,nullable = False)
    testModule = db.Column(db.String(100),nullable = False)
    testPriority = db.Column(db.String(100),nullable = False)
    testStatus = db.Column(db.String(100),nullable = False)
    createdAt = db.Column(db.DateTime,nullable = False,default=datetime.utcnow) 

    def __init__(self,Name,Time,Module,Priority,Status):
        self.testName = Name
        self.testTime = Time
        self.testModule = Module
        self.testPriority = Priority
        self.testStatus = Status


def format_test(test):
    return {
        "testId":test.testId,
        "testName":test.testName,
        "testTime":test.testTime,
        "testModule":test.testModule,
        "testPriority":test.testPriority,
        "testStatus":test.testStatus,
        "createdAt":test.createdAt
    }

@app.route('/') 
def hello():
    return 'hello!'

@app.route('/addTest',methods=['POST'])
def add_test():
    testName = request.json['testName']
    testTime = request.json['testTime']
    testModule = request.json['testModule']
    testPriority = request.json['testPriority']
    testStatus = request.json['testStatus']

    test = Test(testName,testTime,testModule,testPriority,testStatus)
    db.session.add(test)
    db.session.commit()
    return format_test(test)

@app.route('/getAllTests',methods=['GET'])
def get_allTests():
    #tests = Test.query.all()
    tests = Test.query.order_by(Test.testId.asc()).all()
    testList = []
    for test in tests:
        testList.append(format_test(test))
    return {'tests':testList}

@app.route('/getTest/<id>',methods=['GET'])
def get_test(id):
    test = Test.query.filter_by(testId=id).one()
    return {'test':format_test(test)}

@app.route('/deleteTest/<id>',methods=['GET'])
def delete_test(id):
    test = Test.query.filter_by(testId=id).one()
    db.session.delete(test)
    db.session.commit()
    return {'test':format_test(test)}

@app.route('/updateTest/<id>',methods=['POST'])
def update_test(id):
    test = Test.query.filter_by(testId=id)
    status = request.json['testStatus']
    test.update(dict(testStatus=status,createdAt=datetime.utcnow()))
    db.session.commit()
    return {'test':format_test(test.one())}

if __name__ == '__main__':
    app.run()