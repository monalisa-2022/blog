from django.shortcuts import render,HttpResponse,redirect,loader
from login_signup.models import Users
from login_signup.models import posts
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail,EmailMultiAlternatives
import random
from datetime import datetime,timezone
# Create your views here.
name11 = ""

def checkcode(request,uemail):
    user_valid = Users.objects.get(email=uemail)
    y= user_valid.otp_creation_time
    z= datetime.now(timezone.utc)
    if request.method == 'POST':
        myotp = request.POST.get('myotp')
        x= datetime.now(timezone.utc)
        print((x-y).total_seconds())
        if (x-y).total_seconds() <= 120:
            if myotp == user_valid.otp:
                user_valid.is_verified = True
                user_valid.save()
                return redirect('/login/')
            else:
                return HttpResponse("Verification code is not correct , Try again")
        else:
            return HttpResponse("Time out !!! , Try again.")
    dic={'remaining_time':(z-y).total_seconds()}
    return render(request=request, template_name='verification.html', context=dic)

def sendmail(request,uemail):
    otp = random.randint(100000,999999)
    sub = 'Blog Post User Verification'
    msg = '<p>Your OTP : <b>'+str(otp)+'</b></p>'
    femail = 'saswatkumar059@gmail.com'
    msg = EmailMultiAlternatives(sub, msg, femail,[uemail])
    msg.content_subtype='html'
    msg.send()
    user_valid = Users.objects.get(email=uemail)
    print(user_valid.otp)
    user_valid.otp = otp
    user_valid.save()
    return redirect('/checkcode/{}'.format(uemail))

    

def HomeView(request):
    return render(request, 'index.html')


def signupAction(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        uemail = request.POST.get('email')
        # send a email with some otp to that person on this mail id.
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user_valid = Users.objects.get(email=uemail,)
                if user_valid.is_verified == True:
                    return redirect('/login/')
                else:
                    user_valid.name=uname
                    user_valid.password = password1
                    return redirect('/sendmails/{}'.format(uemail))
            except:
                user = Users.objects.create(name=uname, email=uemail, password=password1)
                user.save()
                return redirect('/sendmails/{}'.format(uemail))
      
        else:
            return HttpResponse("Your password and conform password is incorrect are not same")
    return render(request, 'signup.html')

# api for verification for otp , expiry is 2 min.
# use db with creation datetime for otp
# if otp is expired then raise an error otherwise create user.


def loginAction(request):
    if request.method == 'POST':
        uemail = request.POST.get('email')
        passwrd = request.POST.get('password')
        try:
            user = Users.objects.get(email=uemail,password=passwrd)
            if user.is_verified == True:
                global name11
                name11 = user.name
                return redirect('/home/')
            else:
                return HttpResponse("You are not verified. Verify your email first to proceed.")
        except Exception:
            return HttpResponse("Your username and password are incorrect")

    return render(request, 'login.html')


def homeAction(request):
    li=[]
    x = posts.objects.all().values()
    for i in x:
        li.append(i)
    dic={'post':li,'name':name11}
    return render(request=request,template_name='home.html',context=dic)


def createAction(request):
    if request.method == 'POST':
        head = request.POST.get('heading')
        desc = request.POST.get('desc')
        post = posts.objects.create(heading=head, author=name11, description=desc)
        post.save()
        return redirect('/home/')
    return render(request,'create.html')


def deleteAction(request,id):
    post = posts.objects.get(id=id)
    post.delete()
    return redirect('/home/')


def updateAction(request,id):
    post = posts.objects.get(id=id)
    template = loader.get_template('update.html')
    context = {'post':post}
    print(post.description)
    return HttpResponse(template.render(context,request))

def updateRecordAction(request,id):
    head = request.POST.get('heading')
    desc = request.POST.get('desc')
    post = posts.objects.get(id=id)
    post.heading = head
    post.description = desc
    post.save()
    return redirect('/home/')
