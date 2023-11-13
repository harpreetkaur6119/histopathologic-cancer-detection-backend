# Histopathologic Cancer Detection Backend App
Cancer is a disease in which cells are developed abnormally and they divide uncontrollably. This in turn has the ability to infiltrate and destroy normal body tissue. If detected early, it is highly treatable.

Deep learning in the field of image processing has shown exceptional results. The aim of this project is to do histopathologic cancer detection using Convolutional Neural Networks (CNN) and transfer learning. The goal is to create such a model that it can detect from a scan if the cancer tissue is found or not in the image, so that it is detected and appropriate medical treatment can be provided for its cure.

TensorFlow library is used for the deep learning. In this project, we will be using various CNN models such as Xception, VGG16 and resnet-50 Convolutional Neural Network (CNN). This will help us in concluding the best model for our use case.

![Screenshot 2023-08-13 162006](https://github.com/harpreetkaur6119/histopathologic-cancer-detection-backend/assets/64327716/3d12b124-dd46-4eac-8a85-bd74b05b0f98)



# Install the necessary libraries
pip install requirements.txt

# To Run
python app.py

# Creating Docker Image
docker build -t pathology_backend:1.0 .

# To Run Docker Image
docker run -d --name backend --restart on-failure -p 5000:5000 pathology_backend:1.0
