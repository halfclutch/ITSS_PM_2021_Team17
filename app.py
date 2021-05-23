import os
from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from form import CyclistInfo
from werkzeug.utils import secure_filename
from preprocessing import*
import joblib

app = Flask(__name__, template_folder='Template')

#Set secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#set paths to upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['IMAGE_UPLOADS'] = os.path.join(APP_ROOT, 'static')


@app.route('/', methods=['GET','POST'])
def index():
    form = CyclistInfo()
    if request.method == 'POST':
    
        Apparel=form.Apparel
        if  Apparel =="Skinsuit":
            Apparel = 1
        else: Apparel = 1.1
        
        Helmet=form.Helmet
        if  Helmet =="Aero-helmet":
            Helmet = 1
        else: Helmet = 1.06
        
        Frame=form.Frame
        if  Frame =="Tri-bike":
            Frame = 1
        else: Frame = 1.04
        
        Wheels=form.Wheels
        if  Wheels =="Aero-wheels":
            Wheels = 1
        else: Wheels = 1.1
        
        Bars=form.Bars
        if  Bars =="Aero-bars":
            Bars = 1
        else: Bars = 1.1
        
        Position =form.Staying_in_Position
        if  Position == 1:
            Position = 1
        else: Position = 1.05
 
        Weight = form.Weight.data
        Speed = form.Speed.data
        
        
        uploaded_file = form.Image.data
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
            uploaded_file.save(file_path)            
            single_test = test_input(file_path)
            model = tf.keras.models.load_model("model", compile=False) 
            #model = tf.keras.models.load_model("C:/Users/ASUS/Desktop/ITTS/SystemCode/model", compile=False) 
            prediction = model.predict(single_test) 
            pred_mask = create_mask(prediction)
            pred_mask = pred_mask[0]
            test = pred_mask[:,:,0]
            no_of_pixel_cyclist = np.count_nonzero(test == 1)
            no_of_pixel_wheel = np.count_nonzero(test == 2)
            normalised_area = (no_of_pixel_cyclist + no_of_pixel_wheel)/no_of_pixel_wheel 
            
            regressor = joblib.load("regressor.pkl")
            sc_X = joblib.load("sc_X.joblib")
            sc_Y = joblib.load("sc_Y.joblib")            
            actual_area = sc_Y.inverse_transform((regressor.predict(sc_X.transform(np.array([[normalised_area]])))))
            actual_area = round(actual_area[0],4)
            CoD = 0.535*Apparel*Helmet*Frame*Wheels*Bars*Position
            CoD = round(CoD, 4)
            CdA = actual_area*CoD
            CdA = round(CdA, 4)

            pow_air_resistance = 0.5*CdA*1.19*Speed**3 
            pow_air_resistance = round(pow_air_resistance, 2)
            pow_roll_resistance = 0.004*Weight*9.81*Speed
            pow_roll_resistance = round(pow_roll_resistance, 2)
            total_pow = (pow_air_resistance + pow_roll_resistance)*1.02
            total_pow = round(total_pow, 2)
            
            return render_template('result.html', image_path = filename, actual_area=actual_area, Cd=CoD, CdA=CdA, air=pow_air_resistance, rolling=pow_roll_resistance, pedaling=total_pow)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)


