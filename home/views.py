from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.metrics import precision_score,recall_score,f1_score
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,"home.html")
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name, last_name=last_name)
                user.save()
                print("User Created")
                return redirect('signin')
        else:
            messages.info(request, 'Password not matching..')
            return redirect('signup')
        return redirect('/')
    else:
        return render(request, 'signup.html')
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('predict')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
def predict(request):
    if (request.method == 'POST'):
        frame_number = int(request.POST['frame_number'])
        frame_time = int(request.POST['frame_time'])
        frame_len = int(request.POST['frame_len'])
        eth_src = int(request.POST['eth_src'])
        eth_dst = int(request.POST['eth_dst'])
        ip_src = int(request.POST['ip_src'])
        ip_dst = int(request.POST['ip_dst'])
        ip_proto = int(request.POST['ip_proto'])
        ip_len = int(request.POST['ip_len'])
        tcp_len = int(request.POST['tcp_len'])
        tcp_srcport = int(request.POST['tcp_srcport'])
        tcp_dstport = int(request.POST['tcp_dstport'])
        #label = int(request.POST['label'])
        df = pd.read_csv(r"C:\Users\aksha\Downloads\Project code\Source Code\static\dataset\Cyberthreat_data")
        labels = df.columns[0:-2]
        X = df[labels]
        X = np.asarray(X, dtype='float64')
        Y = df['normality']
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=1)
        reg = RandomForestClassifier()
        reg.fit(X_train, Y_train)
        model = reg
        predic = np.array([[frame_number,frame_time,frame_len,eth_src,eth_dst,ip_src,ip_dst,ip_proto,ip_len,tcp_len,tcp_srcport,tcp_dstport]])
        predic.reshape(-1,1)
        pred = model.predict(predic)
        Threat = pred[0]
        if (Threat == 1):
            r = "DOS Attack"
        elif(Threat == 2):
            r= "Phishing"
        elif(Threat == 3):
            r= "SQL Injection"
        elif (Threat == 4):
            r= "Spyware"
        elif (Threat == 5):
            r= "MITM Attack"
        else:
            r = "Ransomeware"
        messages.info(request, r)
    return render(request,"predict.html")
def logout(request):
    auth.logout(request)
    return redirect('/')

