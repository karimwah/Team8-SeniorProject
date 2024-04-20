import os
from flask import Flask, render_template, send_from_directory, url_for, request
from encode import insert_message
import matplotlib.pyplot as plt
import numpy as np
import steg_lib as slimport
import io
from PIL import Image
from io import BytesIO
from decode import read_message

ALLOWED_EXTENSIONS = {'tiff'}

# Check if the filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app(test_config=None):
    # Makes the flask instanace
    app = Flask(__name__, '/static', instance_relative_config=True)
    app.config.from_mapping(
        # Change this key later using secrets.token_hex
        SECRET_KEY='secret',
        DATABASE=os.path.join(app.instance_path, 'stegdemo.sqlite'),
    )

    if test_config is None:
        # Load the instance configuration
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test configuration
        app.config.from_mapping(test_config)

    # Make sure the instance actually exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    # Routing for pages across the website
    #@app.route('/', methods=['GET', 'POST'])
    #def home():
    #     return render_template('main.html')
    
    @app.route('/main.html', methods=['GET', 'POST'])
    def main():
        return render_template('main.html')

    @app.route('/about.html', methods=['GET', 'POST'])
    def about():
        return render_template('about.html')

    @app.route('/stegtool.html', methods=['GET', 'POST'])
    def stegtool():
        
        return render_template('stegtool.html')

    @app.route('/submit', methods=['GET', 'POST'])
    def submit_form():

    #Get form data

        #image = request.files['image']
        message = request.form['message']
        startloc = request.form['start_location']

        if 'image' not in request.files:
            return 'No file part'
        image = request.files['image']
        if image.filename == '':
            return 'No selected file'
        if image and allowed_file(image.filename):
            # Here you can save the file or perform further processing
            # For example:
            with Image.open(image) as img:
            # Process form data using imported function
                insert_message(img, message, startloc)
            return render_template('success.html')
        else:
            return render_template('invalid.html')
            #return 'Invalid file type was Uploaded. This Tool will only work with .tiff files.' 


    @app.route('/stegtooldec.html', methods=['GET', 'POST'])
    def StegToolDec():

        return render_template('stegtooldec.html')
    
    @app.route('/decode', methods=['GET', 'POST'])
    def dec():
     
        coded_image = request.files['coded_image']
        start_loc = request.form['start_loc']
        message_length = request.form['message_length']
        with Image.open(coded_image) as c_img:
            read_message(c_img, start_loc, message_length)
        return render_template('successdec.html')

    @app.route('/FAQ.html', methods=['GET', 'POST'])
    def faq():
        return render_template('FAQ.html')
    
    @app.route('/review.html', methods=['GET', 'POST'])
    def review():
        return render_template('review.html')
 
    @app.route('/auth/login.html', methods=['GET', 'POST'])
    def login():
        return render_template('/auth/login.html')
    
    @app.route('/auth/register.html', methods=['GET', 'POST'])
    def register():
        return render_template('/auth/register.html')

    @app.route('/tos.html', methods=['GET', 'POST'])
    def tos():
        return render_template('tos.html')
    
    # Imports and initializes the database
    from . import db
    db.init_app(app)


    # Imports and initializes the auth blueprints
    from . import auth
    app.register_blueprint(auth.bp)


    from . import wp
    app.register_blueprint(wp.bp)

    app.static_folder = 'static'
    return app