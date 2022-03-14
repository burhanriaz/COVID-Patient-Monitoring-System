from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import login
import pyrebase
from django.core.mail import BadHeaderError, send_mail

# Create your views here.


# put your firebase api key
config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
};
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()


def home(request):
    return render(request, 'home.html')


def alertmessage(request):
    db = firebase.database()
    BedN = 1
    all_bed = db.child("Sensor").get()
    ls = []  # finding bed list here
    for users in all_bed.each():
        # print(users.key())
        ls.append(users.key())
    ls.pop(0)
    global bedno, message, email
    if request.method == "POST":
        email = request.POST.get('email')
        bedno = request.POST.get('bedno')
        message = request.POST.get('message')

        bedno = str("Alert Message From Bed No : ") + str(bedno)
        if email and bedno and message:
            try:
                send_mail(bedno, message, "burhanriaz35@gmail.com", [str(email)])
                messages.success(request, 'Message has been Sent')
            except BadHeaderError:
                # return HttpResponse('Invalid header found.')
                messages.success(request, 'Invalid header found.')

        else:
            messages.success(request, 'Invalid Message ')

    # # In reality we'd use a form class
    # # to get proper validation errors.
    #         return HttpResponse('Make sure all fields are entered and valid.')
    return render(request, 'alertmessage.html', {'ls': ls})


def Register(request):
    dtb = firebase.database()
    global C_paswd, paswd, email
    if request.method == "POST":

        email = request.POST.get('email')
        paswd = request.POST.get('password')
        C_paswd = request.POST.get('confirm_password')

        if paswd == C_paswd:
            try:
                user = authe.create_user_with_email_and_password(email, paswd)
                authe.send_email_verification(user['idToken'])
                messages.success(request, 'User Register sucsessfuly!')
            except:
                messages.success(request, 'Email Already Exist!')

        else:
            messages.success(request, 'Something was wrong Try Again!')
    return render(request, 'Registeruser.html')



def Login(request):
    dtb = firebase.database()
    global paswd, email,login
    if request.method == "POST":

        email = request.POST.get('email')
        paswd = request.POST.get('password')

        try:
            user = authe.sign_in_with_email_and_password(email, paswd)
            messages.success(request, 'Login sucsessfuly!')
            session_id = user['idToken']
            request.session['uid'] = str(session_id)

        except:
            messages.success(request, 'Wrong Email or Password')


    return render(request, 'Login.html')


def Logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def forgotpassword(request):
    global  email
    if request.method == "POST":

        email = request.POST.get('email')
        try:
            authe.send_password_reset_email(email)
            messages.success(request, 'Password Reset Email Sent!')
        except:
            messages.success(request, 'Something was Wrong try Again')
    return render(request, 'forgotpassword.html')

def PatientRegister(request):
    db = firebase.database()
    ls = []
    all_patient = db.child("Patient").get()
    if request.method == "POST":
        name = request.POST.get('name')
        fathername = request.POST.get('fathername')
        cnic = request.POST.get('CNIC')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        bedNo = request.POST.get('bedno')
        age = request.POST.get('age')

        temp = 0
        for p in all_patient.each():
            print(p.key())
            ls.append(p)
        for i in ls:
            if i.key() == cnic:
                temp = 1

        if temp == 1:

            messages.success(request, 'Already Register CNIC!!! Use other CNIC')
        else:

            data = {
                "Name": name,
                "Father Name": fathername,
                "CNIC": cnic,
                "Address": address,
                "Phone": phone,
                "Bed No": bedNo,
                "Age": age,
            }
            db.child("Patient").child(cnic).set(data)
            messages.success(request, 'Patient has been Register')

    return render(request, 'PatientRegister.html')


def Sensor(request):
    db = firebase.database()
    BedN = 1
    if request.method == "POST":
        BedN = request.POST.get('bedno')  # geting bed number from web page
    BPM = []
    SPO2 = []
    DateTime = []
    BedNo = []
    all_bed = db.child("Sensor").get()
    ls = []  # finding bed list here
    for users in all_bed.each():
        # print(users.key())
        ls.append(users.key())
    ls.pop(0)

    # for li in all_bed.each():  # fetching spcific bed data
    ind = db.child("Sensor").child(BedN).get()
    for us in ind.each():
        BPM.append(firebase.database().child("Sensor").child(BedN).child(us.key()).child('BPM').get().val())
        BedNo.append(firebase.database().child("Sensor").child(BedN).child(us.key()).child('Bed No').get().val())
        DateTime.append(firebase.database().child("Sensor").child(BedN).child(us.key()).child('DateTime').get().val())
        SPO2.append(firebase.database().child("Sensor").child(BedN).child(us.key()).child('SPO2').get().val())
        comb_lis = zip(DateTime, BPM, SPO2, BedNo)

    return render(request, 'SensorData.html', {'comb_lis': comb_lis, 'ls': ls})


def About(request):
    return render(request, 'About.html')


def Graph(request):
    return render(request, 'Graph.html')


def Patientlist(request):
    db = firebase.database()
    BedN = 1
    if request.method == "POST":
        us = request.POST.get('bedno')  # geting bed number from web page
    Name = []
    FatherName = []
    CNIC = []
    Phone = []
    Address = []
    Age = []
    Bedno = []

    all_Patient = db.child("Patient").get()
    ls = []
    for users in all_Patient.each():
        #   print(users.key())
        ls.append(users.key())

    for us in ls:
        Name.append(firebase.database().child("Patient").child(us).child('Name').get().val())
        FatherName.append(firebase.database().child("Patient").child(us).child('Father Name').get().val())
        Age.append(firebase.database().child("Patient").child(us).child('Age').get().val())
        CNIC.append(firebase.database().child("Patient").child(us).child('CNIC').get().val())
        Bedno.append(firebase.database().child("Patient").child(us).child('Bed No').get().val())
        Address.append(firebase.database().child("Patient").child(us).child('Address').get().val())
        Phone.append(firebase.database().child("Patient").child(us).child('Phone').get().val())
        comb_lis = zip(Name,FatherName,CNIC,Address,Phone,Bedno,Age)
    return render(request, 'Patientlist.html', {'comb_lis': comb_lis, 'ls': ls})

