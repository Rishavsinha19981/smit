from flask import Flask, render_template, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import numpy as np 
import pickle


app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost/ruv2'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://djeebqxoctxwjp:6f894176c19b0b62a6c88bff94b08a23597ee8efe69db1285df258ec884c5643@ec2-54-163-254-204.compute-1.amazonaws.com:5432/ddqscaoj65u3sq'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


model = pickle.load(open('model.pkl', 'rb'))
class Feedback(db.Model):
    __tablename__ = 'feedback'
    EmailID= db.Column(db.String(200),unique=True)
    Employee = db.Column(db.String(200),primary_key=True )
    Location = db.Column(db.String(200))
    EmployeeID = db.Column(db.String(200), unique=True)
    Designation = db.Column(db.String(200))
    Department = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self,EmailID,Employee,Location,EmployeeID,Designation, Department, rating, comments):
        self.EmailID = EmailID
        self.Employee = Employee
        self.Location = Location
        self.EmployeeID = EmployeeID
        self.Designation = Designation
        self.Department = Department
        self.rating = rating
        self.comments = comments 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
         EmailID = request.form['EmailID']
         Employee = request.form['Employee']
         Location = request.form['Location']
         EmployeeID = request.form['EmployeeID']
         Designation = request.form['Designation']
         Department = request.form['Department']
         rating = request.form['rating']
         comments = request.form['comments']
        # print(employee, department, rating, comments)
         if Employee == '' or Department == '':   
            return render_template('index.html', message='Please enter required fields')
         if db.session.query(Feedback).filter(Feedback.Employee == Employee).count() == 0:
            data = Feedback(EmailID,Employee,Location,EmployeeID,Designation, Department, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(EmailID,Employee,Location,EmployeeID,Designation, Department, rating, comments)
            return render_template('index2.html')
        
        
         return render_template('index.html', message='You have already submitted feedback')
         
@app.route('/')
def home():
    return render_template('index2.html')
    
@app.route('/predict',methods=['POST'])
    
def predict():
    ##For rendering results on HTML GUI
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)

    return render_template('index2.html', prediction_text='Employee Salary should be $ {}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    
    #For direct API calls trought request
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run()
