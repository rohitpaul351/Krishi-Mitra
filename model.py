from flask import Flask, request, render_template, redirect, url_for
import pickle
from flask import *  
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
import json
from flask_mail import Mail
from pymongo.mongo_client import MongoClient
import json

app = Flask(__name__)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# scaler = pickle.load(open("model/standardScalar.pkl", "rb"))
# model = pickle.load(open("model/ModelForTesting.pkl", "rb"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fertilizers.html', methods=['GET'])
def fertilizers():
    return render_template('fertilizers.html')
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/fertilizers.html', methods=['GET'])
# def fertilizers():
#     return render_template('fertilizers.html')

with open ('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = True

#app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']

)
mail = Mail(app)

app.config['SECRET_KEY'] = 'supersecretkey'
# app.config['UPLOAD_FOLDER'] = 'static'
# app.config['SECRET_KEY'] = 'pretty print'

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/krishi-mitra'
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12), nullable=True)

    

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        # Add entry to the database
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contact(name = name, email = email, msg = message, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from'+name, sender=email, recipients=[params['gmail-user']], body=message) 
    return render_template('contact.html')

scaler = pickle.load(open("model/standardScalar.pkl", "rb"))
model = pickle.load(open("model/ModelForTesting.pkl", "rb"))


@app.route('/predict.html', methods=['GET', 'POST'])
def predict_datapoint():
    result = ""
    reviews = []

    if request.method == 'POST':
        Nitrogen = int(request.form.get("Nitrogen"))
        Phosphorous = int(request.form.get('Phosphorous'))
        Potassium = int(request.form.get('Potassium'))
        Temperature = float(request.form.get('Temperature'))
        Humidity = float(request.form.get('Humidity'))
        pH_level = float(request.form.get('pH level'))
        Rainfall = float(request.form.get('Rainfall'))

        new_data = scaler.transform([[Nitrogen, Phosphorous, Potassium, Temperature, Humidity, pH_level, Rainfall]])
        predict = model.predict(new_data)

        crops = [
            'Rice', 'Maize', 'Chickpea', 'Kidneybeans', 'Pigeonpeas', 'Mothbeans', 'Mungbean', 'Blackgram',
            'Lentil', 'Pomegranate', 'Banana', 'Mango', 'Grapes', 'Watermelon', 'Muskmelon', 'Apple', 'Orange',
            'Papaya', 'Coconut', 'Cotton', 'Jute', 'Coffee'
        ]
        result = crops[predict[0] - 1]

        try:
            mydict = {"Nitrogen": Nitrogen, "Phosphorous": Phosphorous, "Potassium": Potassium,
                      "Temperature": Temperature, "Humidity": Humidity, "pH Level": pH_level,
                      "Rainfall": Rainfall}
            reviews.append(mydict)

            uri = "mongodb+srv://<your-mongodb-uri>"
            client = MongoClient(uri)
            db = client['Krishi_Mitra']
            review_col = db['Krishi_Mitra']
            review_col.insert_one(reviews)
        except:
            pass

        # Redirect to the appropriate page based on the recommended crop
        if result == 'Rice':
            return redirect(url_for('rice_page'))
        elif result == 'Maize':
            return redirect(url_for('maize_page'))
        elif result == 'Mango':
            return redirect(url_for('mango_page'))
        elif result == 'Chickpea':
            return redirect(url_for('chickpea_page'))
        elif result == 'Kidneybeans':
            return redirect(url_for('Kidneybeans_page'))
        elif result == 'Pigeonpeas':
            return redirect(url_for('Pigeoneas_page'))
        elif result == 'Mothbeans':
            return redirect(url_for('mothbeans_page'))
        elif result == 'Mungbeans':
            return redirect(url_for('Mungbeans_page'))
        elif result == 'Blackgram':
            return redirect(url_for('Blackgram_page'))
        elif result == 'Lentil':
            return redirect(url_for('Lentil_page'))
        elif result == 'Pomegranate':
            return redirect(url_for('pomegranate_page'))
        elif result == 'Banana':
            return redirect(url_for('banana_page'))
        elif result == 'Grapes':
            return redirect(url_for('grapes_page'))
        elif result == 'Watermelon':
            return redirect(url_for('Watermelon_page'))
        elif result == 'Muskmelon':
            return redirect(url_for('Muskmelon_page'))
        elif result == 'Apple':
            return redirect(url_for('apple_page'))
        elif result == 'Orange':
            return redirect(url_for('orange_page'))
        elif result == 'Papaya':
            return redirect(url_for('Papaya_page'))
        elif result == 'Coconut':
            return redirect(url_for('coconut_page'))
        elif result == 'Cotton':
            return redirect(url_for('cotton_page'))
        elif result == 'Jute':
            return redirect(url_for('jute_page'))
        elif result == 'Coffee':
            return redirect(url_for('coffee_page'))
        else:
            return redirect(url_for('default_page'))

       
    
    else:
        return render_template('predict.html')

@app.route('/rice.html', methods=['GET'])
def rice_page():
    return render_template('rice.html')

@app.route('/maize.html', methods=['GET'])
def maize_page():
    return render_template('maize.html')

@app.route('/mango.html', methods=['GET'])
def mango_page():
    return render_template('mango.html')
@app.route('/chickpea.html', methods=['GET'])
def chickpea_page():
    return render_template('chickpea.html')
@app.route('/kidneybeans.html', methods=['GET'])
def Kidneybeans_page():
    return render_template('kidneybeans.html')
@app.route('/mothbeans.html', methods=['GET'])
def Mothbeans_page():
    return render_template('mothbeans.html')
@app.route('/mungbeans.html', methods=['GET'])
def Mungbeans_page():
    return render_template('mungbeans.html')
@app.route('/backgram.html', methods=['GET'])
def Blackgram_page():
    return render_template('backgram.html')
@app.route('/lentil.html', methods=['GET'])
def Lentil_page():
    return render_template('lentil.html')
@app.route('/pomegranate.html', methods=['GET'])
def pomegranate_page():
    return render_template('pomegranate.html')
@app.route('/banana.html', methods=['GET'])
def banana_page():
    return render_template('banana.html')
@app.route('/grapes.html', methods=['GET'])
def grapes_page():
    return render_template('grapes.html')
@app.route('/watermelon.html', methods=['GET'])
def Watermelon_page():
    return render_template('watermelon.html')
@app.route('/muskmelom.html', methods=['GET'])
def Muskmelon_page():
    return render_template('muskmelom.html')
@app.route('/apple.html', methods=['GET'])
def apple_page():
    return render_template('apple.html')
@app.route('/orange.html', methods=['GET'])
def orange_page():
    return render_template('orange.html')
@app.route('/papaya.html', methods=['GET'])
def Papaya_page():
    return render_template('papaya.html')
@app.route('/coconut.html', methods=['GET'])
def coconut_page():
    return render_template('coconut.html')
@app.route('/cotton.html', methods=['GET'])
def cotton_page():
    return render_template('cotton.html')
@app.route('/jute.html', methods=['GET'])
def jute_page():
    return render_template('jute.html')
@app.route('/coffee.html', methods=['GET'])
def coffee_page():
    return render_template('coffee.html')
@app.route('/default.html', methods=['GET'])
def default_page():
    return render_template('default.html')





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
