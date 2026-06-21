from django.conf import settings
from django.shortcuts import render, HttpResponse
import json
import sys
from templates.prediction import prediction1d, prediction2d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')  

        if username == "admin" and password == "admin":
            return redirect('AudioUpload.html')  
        else:
            return render(request, 'Login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'Login.html')

# Create views. # Audio Upload
def audioUpload(request):
    return render(request, 'AudioUpload.html')

def toModelSelection(request):
    file = request.GET['file']
    mood = request.GET['mood']
    fnm = {'file': file, 'mood': mood}
    return render(request, 'ModelSelection.html', {'fnm': json.dumps(fnm)})

def getBack(request):
    return render(request, 'AudioUpload.html')

def toPrediction(request):
    file = request.GET['file']
    mood = request.GET['mood']
    model = request.GET['model']
    types = ['angry','happy','relaxed','sad']  # For plotting the x-axis

    file_path = os.path.join(settings.BASE_DIR, 'static', file)

    if not os.path.exists(file_path):
        return HttpResponse(f"File not found at {file_path}", status=404)
  
    image_dir = os.path.join(settings.BASE_DIR, 'static', 'image')
    image_files = [
        os.path.join(image_dir, 'prob.png'),
        os.path.join(image_dir, 'prob1.png'),
        os.path.join(image_dir, 'prob2.png'),
        os.path.join(image_dir, 'prob3.png')
        ]

    for img_file in image_files:
        if os.path.isfile(img_file):
            os.remove(img_file)
    
    if model =='1':
        predict,prob = prediction1d(file_path)
        f=plt.figure(figsize=(12,4))
        plt.title('probabilty of being different mood types')
        plt.ylabel('probabilty')
        plt.bar(types, prob[0])
        plt.savefig(os.path.join(image_dir, 'prob.png')) 
        
    else:
        predict,prob1,prob2,prob3 = prediction2d(file_path)
        
        f = plt.figure(figsize=(12,4))
        plt.title('probabilty of being different mood types using spectrogram')
        plt.bar(types, prob1[0])
        plt.savefig(os.path.join(image_dir, 'prob1.png'))  

        f = plt.figure(figsize=(12,4))
        plt.title('probabilty of being different mood types using MFCC')
        plt.bar(types, prob2[0])
        plt.savefig(os.path.join(image_dir, 'prob2.png'))  

        f = plt.figure(figsize=(12,4))
        plt.title('probabilty of being different mood types using Mel-spectrogram')
        plt.bar(types, prob3[0])
        plt.savefig(os.path.join(image_dir, 'prob3.png'))

        

    fmm = {'file': file, 'mood': mood, 'model': model,'predict':predict}
  
    return render(request, 'Prediction.html', {'fmm': json.dumps(fmm)})

def returnModelSelection(request):
    file = request.GET['file']
    mood = request.GET['mood']
    fnm = {'file':file,'mood':mood}
    return render(request, 'ModelSelection.html', {'fnm': json.dumps(fnm)})


    










