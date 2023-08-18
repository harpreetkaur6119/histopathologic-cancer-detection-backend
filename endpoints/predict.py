import os
import numpy as np
from flask import request, jsonify
from flask_restx import Namespace, Resource, reqparse
from utils.load_classifier import get_classifier
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from tensorflow.keras import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from flask_cors import cross_origin

from config import UPLOAD_FOLDER
from utils.file_validations import allowed_file

api = Namespace('Prediction APIs', description='Predict and classify the object')

classifier:Model = get_classifier()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tif'}

CATEGORIES = ['Metastatic Tissue Not Found', 'Metastatic Tissue Found']

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, location='files', required=True, )

@api.route('/prediction')
# @cross_origin()
class predict(Resource):
    @api.expect(upload_parser)
    def post(self):
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message' : 'No file selected for prediction'})
            resp.status_code = 400
            return resp
        if not os.path.exists(os.path.join(UPLOAD_FOLDER,'pred')):
            os.makedirs( os.path.join(UPLOAD_FOLDER,'pred'))
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            imgDim =96
            filename = secure_filename(file.filename)
            
            file_path = os.path.join(UPLOAD_FOLDER,'pred', filename)
            file.save(file_path)
            file.close()
            predGenerator = ImageDataGenerator(rescale = 1./255)
            predData = predGenerator.flow_from_directory(
                UPLOAD_FOLDER, 
                target_size = (imgDim, imgDim),
                batch_size = 48, 
                class_mode = 'categorical')
            # img_ = image.load_img(file_path, target_size=(299, 299))
            # img_array = image.img_to_array(img_)
            # img_processed = np.expand_dims(img_array, axis=0) 
            # img_processed /= 255.  
            
            # return predData.filenames
            predictions = classifier.predict_generator(predData)
            print (predictions)
            # return None
            # predictions = classifier.predict(img_processed)
            pred = predictions[0]
            predicted_class = CATEGORIES[ np.argmax(pred)]
            os.remove(file_path)
            resp = jsonify({
                'classes': CATEGORIES,
                'prediction': list(map(lambda x : float(x), list(pred))),
                'predicted_class' : str(predicted_class),
                'file_name' : filename,
                })
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message' : f'Allowed file types are {ALLOWED_EXTENSIONS}'})
            resp.status_code = 400
            return resp
    