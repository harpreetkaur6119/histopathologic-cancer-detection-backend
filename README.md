# Histopathologic Cancer Detection Backend App

# Install the necessary libraries
pip install requirements.txt

# To Run
python app.py

# Creating Docker Image
docker build -t pathology_backend:1.0 .

# To Run Docker Image
docker run -d --name backend --restart on-failure -p 5000:5000 pathology_backend:1.0
