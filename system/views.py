from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
import numpy as np
from keras.models import load_model
import tensorflow as tf
import sklearn 
from sklearn.preprocessing import Normalizer, StandardScaler
from system.models import WaterDataSql,Prediction_save
import datetime


# Create your views here.

# Counters for each record submission
# EMAIL_ADDRESS = 'jamalkurui@gmail.com'

# contribution_id = 00;
# request_id = 00;
# response_id = 00;


def homepage(request):
    if request.method == "POST":
        scaler=StandardScaler()
        date=request.POST['date']
        average_cost=request.POST['average_cost']
        population=request.POST['population']
        household_size=request.POST['household_size']
        water_cost=request.POST['water_cost']
        x_predict=[average_cost,population,household_size,water_cost]
        x_predict=np.asarray(x_predict)
        x_predict=np.reshape(x_predict,(-1,1))
        x_predict=scaler.fit_transform(x_predict)
        x_predict=np.reshape(x_predict,(1,x_predict.shape[0]))
        x_predict=tf.convert_to_tensor(x_predict)
        model = load_model('model/IS_Project_2.h5')
        prediction=model.predict(x_predict)
        prediction=scaler.inverse_transform(prediction)
        save_pred=Prediction_save()
        save_pred.prediction_volume=prediction
        save_pred.save()
        #print(prediction)
        return redirect(dashboard)

    return render(request,'system/index.html')

# Dashboard for 2 graphs and a map image
def dashboard(request):
    data=WaterDataSql.objects.all()
    data_list_volume=[]
    format = '%d/%m/%Y'
    for iterator in range(len(data)):
        data_list_volume.append(float(data[iterator].volume))
    return render(request,'system/dashboard.html',context={'data_volume':data_list_volume})

def contribute(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        support_type = request.POST['support_type']
        description = request.POST['description']
        contribution_file=request.FILES['contribution_file']
        contribution_id = contribution_id + name[:4]
        subject = f'Contribution Request {contribution_id}'
        # try:
        #     mail = EmailMessage(subject, description, ['EMAIL_ADDRESS'], [email])
        #     mail.attach(contribution_file, attach.read(), attach.content_type)
        #     mail.send()
        #     contribution_id += 1
        # except:
        return render(request, "system/contribute.html")
    return render(request, 'system/contribute.html')
        
def support(request):
    if request.method == "POST":
        name=request.POST['name']
        email=request.POST['email']
        description=request.POST['description']
        request_file=request.FILES['request_file']
        request_id = request_id + name[:4]
        subject = f'Support Request {request_id}'
        # try:
        #     mail = EmailMessage(subject, description, ['EMAIL_ADDRESS'], [email])
        #     mail.attach(request_file, attach.read(), attach.content_type)
        #     mail.send()
        #     contribution_id += 1
        # except:
        return render(request, "system/support.html")
    return render(request, 'system/support.html')


# # To return plotted graph image to view
# def return_graph(x_label, y_label, title):
#     fig = plt.figure()
#     plt.plot(x,y)

#     imgdata = StringIO()
#     fig.savefig(imgdata, format='svg')
#     imgdata.seek(0)

#     data = imgdata.getvalue()
#     return data
