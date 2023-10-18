from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from studentapp.models import *
from teacherapp.models import Assign_Marks
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.contrib.auth.hashers import check_password


# Create your views here.

def Home(request):
    return render(request, 'usertemplate/index.html')

def About(request):
    return render(request, 'usertemplate/about.html')

def Contact(request):
    return render(request, 'usertemplate/contact.html')

def UserLogin(request):
    if request.method == 'POST':
        stu_email = request.POST.get('email')
        stu_password = request.POST.get('password')
        print(stu_email,stu_password)
        user = authenticate(request=None, email = stu_email, password = stu_password)
        print(user)
        if user and user.stu_status == 'accepted':
            login(request, user)
            request.session["user"]=stu_email
            messages.success(request, 'Login successfull..')
            return redirect('studashboard')
        elif user and user.stu_status == 'pending':
            messages.info(request, 'Your status is in pending..!')
            return redirect('studentlogin')
        else:
            print('invalid')
            messages.error(request,'Invalid Credentials')
            return redirect('studentlogin')
    return render(request, 'usertemplate/login.html')

def Register(request):
    try:
        if request.method == 'POST':
            uname = request.POST.get('name')
            uemail = request.POST.get('email')
            upassword = request.POST.get('password')
            ucontact = request.POST.get('contact')
            uaddress = request.POST.get('address')
            rollnumber = request.POST.get('roll')
            ufile = request.FILES['file']
            print(ufile, uaddress, ucontact, uname, upassword)
            
            stu = MyUser.objects.create_user(uemail, upassword)
            stu.stu_name = uname
            stu.stu_photo = ufile
            stu.stu_address = uaddress
            stu.stu_contact = ucontact
            stu.stu_rollnumber = rollnumber
            stu.save()
            ftoken = str(uuid.uuid4())
            Profile.objects.create(stu_foregin = stu, forget_token = ftoken)
            messages.success(request, 'Registeration was successfully completed...')
    except IntegrityError:
        messages.warning(request,'Email Has Already Been Taken')
        return redirect('registration')
    return render(request, 'usertemplate/register.html')

@login_required(login_url="studentlogin")
def StuProfile(request):
    aa = MyUser.objects.get(email = request.user)
    if request.method == 'POST':
        pwd = request.POST.get('pwd')
        print(pwd)
        fname = request.POST.get('fname')
        contact = request.POST.get("contact")
        address = request.POST.get("address")

        if len(request.FILES) != 0:
            image = request.FILES.get("ufile")
            aa.stu_name = fname
            aa.stu_contact = contact
            aa.stu_address = address
            aa.stu_photo = image
            aa.save()
            messages.success(request, 'Profile Updated successfully...')
        else:
            aa.stu_name = fname
            aa.stu_contact = contact
            aa.stu_address = address
            aa.save()
            messages.success(request, 'Profile Updated successfully...')
        return redirect('stuprofile')
    return render(request, 'usertemplate/myprofile.html', {'stu_det' : aa})

def AdminLogin(request):
    admine = 'admin@gmail.com'
    adminp = 'admin'
    adminemail = request.POST.get('email')
    adminpwd = request.POST.get('password')
    if admine == adminemail and adminp == adminpwd:
        messages.success(request, 'Login successfull...')
        return redirect('admindash')
    return render(request, 'usertemplate/admin.html')

@login_required(login_url="studentlogin")
def StudentDashboard(request):
    return render(request, 'usertemplate/dashboard.html')

@login_required(login_url="studentlogin")
def StudentFeedback(request):
    user_d = MyUser.objects.get(email = request.user)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if not rating:
            # messages.info(request,'give rating')
            return redirect('feedback')
        sid=SentimentIntensityAnalyzer()
        score=sid.polarity_scores(review)
        sentiment=None
        if score['compound']>0 and score['compound']<=0.5:
            sentiment='positive'
        elif score['compound']>=0.5:
            sentiment='very positive'
        elif score['compound']<-0.5:
            sentiment='very negative'
        elif score['compound']<0 and score['compound']>=-0.5:
            sentiment='negative'
        else :
            sentiment='neutral'
        print(sentiment)
        Feeback.objects.create(Stu_Foregin = user_d, Sentiment = sentiment, Rating = rating, Review = review)
        messages.success(request, 'Feedback was submitted successfully...')
    return render(request, 'usertemplate/feedback.html')

@login_required(login_url="studentlogin")
def Marks(request):
    user_d = MyUser.objects.get(email=request.user)
    try:
        subject_marks = Assign_Marks.objects.filter(Stu_Rollnum=user_d.stu_rollnumber)
        labels = [subject.Sub_Name for subject in subject_marks]
        marks = [subject.Sub_marks for subject in subject_marks]
        grades = [subject.Sub_Grade for subject in subject_marks]
        print(grades)
    except:
        messages.info(request, "Didn't assign any marks..!")
        return redirect('marks')
    return render(request, 'usertemplate/marks.html', {'labels': labels, 'marks': marks, 'grades': grades})


@login_required(login_url="studentlogin")
def performance_prediction(request):
    user_d = MyUser.objects.get(email = request.user)
    if request.method == 'POST':
        Sample = request.POST.get('Sample')
        mobile = request.POST.get('mobile')
        sleep = request.POST.get('Sleep')
        extra = request.POST.get('Extracurricular')
        pscores = request.POST.get('previous-Scores')
        hstudy = request.POST.get('hours-studied')
        print(Sample, 'sample')
        ex = 0
        Sample = int(Sample)
        sleep = int(sleep)
        pscores = int(pscores)
        hstudy = int(hstudy)
        mobile = int(mobile)
        if extra == 'yes':
            ex = 1
        else:
            ex = 0
        import pickle
        # Save model to a file using pickle
        
        # Load model from file using pickle
        with open('linear1.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)

        # Now you can use the loaded_model to make predictions
        result = loaded_model.predict([[hstudy, pscores, sleep, Sample, mobile, ex]])
        print(result, 'result')
        grade = ''
        if int(result) >= 90 and int(result) <= 100:
            grade = 'A'
        elif int(result) >= 80 and int(result) <= 89:
            grade = 'B'
        elif int(result) >= 70 and int(result) <= 79:
            grade = 'C'
        elif int(result) >= 60 and int(result) <= 69:
            grade = 'D'
        else:
            grade = 'E'
        user_d = MyUser.objects.get(email=request.user)
        user_d.stu_performance = grade
        user_d.save()
        messages.success(request, f'Student Performance Grade is [{grade}]')
    return render(request, 'usertemplate/prediction.html', {'u':user_d})

@login_required(login_url="studentlogin")
def Change_Password(request):
    user = MyUser.objects.get(email = request.user)
    user_pass = user.password
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        print(old_password, new_password1, new_password2)
        if check_password(old_password, user.password):
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                print('password changed')
                messages.success(request,'Password Updated Successfully')
                return redirect('stuprofile')
            else:
                messages.warning(request,'New password and Confirm New password Should be same')
                print('New password and Confirm New password Should be same')
        else:
            messages.warning(request,'Enter your correct old password')
            print('Enter your correct old password')
    return render(request, 'usertemplate/change-password.html')

def Forgot_Password(request):
    try:
        print('try')
        if request.method == 'POST':
            email = request.POST.get('email')
            user = MyUser.objects.get(email = email)
            profile = Profile.objects.get(stu_foregin = user)
            user_email = user.email
            print(user_email)
            ftoken = profile.forget_token
            mail_message = f'Hey Your Reset Password Link is http://127.0.0.1:8000/reset-password/{ftoken}/'
            print(mail_message)
            send_mail('Password Reset Request',mail_message,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
            messages.info(request,'MAIL was sent..')
    except:
        print('except')
        messages.warning(request,"Email Does not Exist")
    return render(request, 'usertemplate/forgot-password.html')

def Reset_Password(request, id):
    if request.method == 'POST':
        password = request.POST['password']
        profile = Profile.objects.get(forget_token=id).stu_foregin
        print(profile,'profile')
        user = MyUser.objects.get(email=profile)
        user.set_password(password)
        user.save()
        messages.info(request,'Password Changed Please Login! ')
        return redirect('studentlogin')
    return render(request, 'usertemplate/reset-password.html') 

def uLogout(request):
    logout(request)
    messages.info(request, 'Logout successfull...')
    return redirect('home')