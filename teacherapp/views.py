import pandas as pd
from django.shortcuts import redirect, render

from studentapp.models import Feeback, MyUser
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from teacherapp.models import *
# Create your views here.

def AdminDashboard(request):
    all_u = MyUser.objects.all().count()
    pen_u = MyUser.objects.filter(stu_status='pending').count()
    rej_u = MyUser.objects.filter(stu_status='prejected').count()
    fe_co = Feeback.objects.all().count()
    context = {'au' : all_u, 'pu' : pen_u, 'ru' : rej_u, 'fc' : fe_co}
    return render(request, 'admintemplate/dashboard.html', context)

def AdminPendingStudents(request):
    users = MyUser.objects.filter(stu_status = 'pending')
    return render(request, 'admintemplate/pending_students.html', {'u' : users})

def Acceptbtn(req, id):
    user_d = MyUser.objects.get(email=id)
    user_d.stu_status = 'accepted'
    user_d.save()
    messages.success(req, 'Student was accepted..')
    return redirect('pending_students')

def Rejectbtn(req, id):
    user_d = MyUser.objects.get(email=id)
    user_d.stu_status = 'rejected'
    user_d.save()
    messages.info(req, 'Student was rejected..')
    return redirect('pending_students')

def AdminManageStudents(request):
    users = MyUser.objects.filter(Q(stu_status='accepted') | Q(stu_status='rejected'))
    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    return render(request, 'admintemplate/manage_student.html', {'users' :post})

def ChangeStatusBtn(req, id):
    user_d = MyUser.objects.get(email=id)
    if user_d.stu_status == 'accepted':
        user_d.stu_status = 'rejected'
        user_d.save()
        messages.warning(req, 'Student was changed to rejected..')
    else:
        user_d.stu_status = 'accepted'
        user_d.save()
        messages.success(req, 'Student was changed to accepted..')
    return redirect('manage_students')

def DeleteBtn(req, id):
    MyUser.objects.get(email=id).delete()
    messages.info(req, 'Student was deleted..')
    return redirect('manage_students')

def AdminAddSubject(request):
    if request.method =='POST':
        subname = request.POST.get('subject')
        Subject.objects.create(Subject_Name = subname)
        messages.success(request, 'Subject was added successfully...')
    return render(request, 'admintemplate/addsub.html')

def AdminManageSubject(request):
    a = Subject.objects.all()
    return render(request, 'admintemplate/managesub.html', {'sub' : a})

def Delete_Subject_btn(request, id):
    Subject.objects.get(Sub_id = id).delete()
    messages.info(request, 'Subject was deleted..')
    return redirect('manage_subjects')

def AdminAssignMarks(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        rollnum = request.POST.get('rollNumber')
        sub = request.POST.get('subject')
        marks = request.POST.get('marks')
        year = request.POST.get('year')
        # print(marks, sub, rollnum, year)
        try:
            print('try')
            a = MyUser.objects.get(stu_rollnumber = rollnum)
            print(a)
            grade = ''
            if int(marks) >= 90 and int(marks) <= 100:
                grade = 'A'
            elif int(marks) >= 80 and int(marks) <= 89:
                grade = 'B'
            elif int(marks) >= 70 and int(marks) <= 79:
                grade = 'C'
            elif int(marks) >= 60 and int(marks) <= 69:
                grade = 'D'
            else:
                grade = 'E'
            Assign_Marks.objects.create(Stu_Rollnum = rollnum, Sub_Name = sub, Sub_marks = marks, year = year, Stu_foregin = a, Sub_Grade = grade)
            messages.success(request, f'Marks assigned successfully to {rollnum}')
        except:
            print('except')
            messages.warning(request, 'Student Rollnumber not found')
    return render(request, 'admintemplate/assignmark.html', {'sub' : subjects})

def AdminFeedbackgraph(request):
    vn = Feeback.objects.filter(Sentiment = 'very negative').count()
    n = Feeback.objects.filter(Sentiment = 'negative').count()
    vp = Feeback.objects.filter(Sentiment = 'very positive').count()
    p = Feeback.objects.filter(Sentiment = 'positive').count()
    ne = Feeback.objects.filter(Sentiment = 'neutral').count()
    return render(request, 'admintemplate/feedback_graph.html', {'vn' : vn, 'n': n, 'vp' : vp, 'p' : p, 'ne' : ne})

def AdminFeedback(request):
    fee = Feeback.objects.all()
    return render(request, 'admintemplate/feedback.html', {'fe' : fee})

def AdmiSentiment(request):
    a = Feeback.objects.all()
    return render(request, 'admintemplate/sentiment_analysis.html', {'fe' : a})

def AdminManageMarks(request):
    all_marks = Assign_Marks.objects.values_list('Stu_Rollnum', flat=True).distinct()
    students_info = []
    for roll_num in all_marks:
        student_data = Assign_Marks.objects.filter(Stu_Rollnum=roll_num).first()
        if student_data:
            students_info.append(student_data)

    return render(request, 'admintemplate/manage_marks.html', {'m': students_info})



def AdminViewMarks(request, id):
    a = Assign_Marks.objects.filter(Stu_Rollnum = id)
    return render(request, 'admintemplate/view_marks.html', {'marks' : a})

def AdminUploadDataset(request):
    if request.method == 'POST':
        ud = request.FILES['file']
        Upload_Dataset.objects.create(Upload_Dataset = ud)
        messages.success(request, 'Dataset was uploaded successfully...')
    return render(request, 'admintemplate/upload_data.html')

def AdminMarksAnalysis(request):
    return render(request, 'admintemplate/marks_analysis.html')

def AdminNaive(request):
    return render(request, 'admintemplate/naive.html')

def AdminPerformance(request):
    if request.method == 'POST':
        Sample = request.POST.get('Sample')
        mobile = request.POST.get('mobile')
        sleep = request.POST.get('Sleep')
        extra = request.POST.get('Extracurricular')
        pscores = request.POST.get('previous-Scores')
        hstudy = request.POST.get('hours-studied')
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
        messages.success(request, f'Student Performance Grade is [{grade}]')
    return render(request, 'admintemplate/performence_analysis.html')

def AdminSvm(request):
    return render(request, 'admintemplate/svm.html')

def AdminViewDataset(request):
    data = Upload_Dataset.objects.last()
    file = str(data.Upload_Dataset)
    df = pd.read_csv(f'./media/{file}', encoding='latin-1')
    table = df.to_html(table_id = 'data_table')
    return render(request, 'admintemplate/view_dataset.html', {'d' : table})

def SvmBtn(req):
    file = Upload_Dataset.objects.last()
    df = pd.read_csv(file.Upload_Dataset.path)
    X=pd.get_dummies(df.drop('Performance Index',axis=1),drop_first=True)

    y=df['Performance Index']
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    X_train.shape, X_test.shape
    import numpy as np
    from sklearn.metrics import mean_absolute_error
    from sklearn.svm import SVR
    from sklearn.metrics import r2_score, mean_squared_error
    from sklearn.model_selection import cross_val_score
    # Create an SVM regressor
    svm_regressor = SVR()
    # Fit the model
    svm_regressor.fit(X_train, y_train)

    # Predictions
    train_prediction = svm_regressor.predict(X_train)
    test_prediction = svm_regressor.predict(X_test)
   
    name = 'SVM'
    r2 = r2_score(y_test, test_prediction)
    amse = (mean_absolute_error(y_test, test_prediction))
    mse = (mean_squared_error(y_test, test_prediction))
    rmse = np.sqrt(mean_squared_error(y_test, test_prediction))
    print(r2)
    messages.success(req, 'Algorithm exicuted successfully...')
    return render(req,'admintemplate/svm.html', {'r2' : r2, 'rmse' : rmse, 'amse' : amse, 'mse' : mse, 'name':name})

def NaiveBtn(req):
    from sklearn.linear_model import LinearRegression
    file = Upload_Dataset.objects.last()
    df = pd.read_csv(file.Upload_Dataset.path)
    X=pd.get_dummies(df.drop('Performance Index',axis=1),drop_first=True)

    y=df['Performance Index']
    

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    X_train.shape, X_test.shape
    import numpy as np
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    print('*'*10)

    # prediction
    train_prediction= lr.predict(X_train)
    test_prediction= lr.predict(X_test)
    print('*'*10)
    # evaluation

    from sklearn.metrics import accuracy_score
    from sklearn.metrics import r2_score

    name = 'LinearRegression'
    r2 = r2_score(y_test, test_prediction)
    amse = (mean_absolute_error(y_test, test_prediction))
    mse = (mean_squared_error(y_test, test_prediction))
    rmse = np.sqrt(mean_squared_error(y_test, test_prediction))
    messages.success(req, 'Algorithm exicuted successfully...')
    return render(req, 'admintemplate/naive.html',{'r2' : r2, 'rmse' : rmse, 'amse' : amse, 'mse' : mse, 'name':name})