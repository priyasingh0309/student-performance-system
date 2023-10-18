"""
URL configuration for performanceProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from studentapp.views import *
from teacherapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Student Url
    path('', Home, name = 'home'),
    path('contact', Contact, name = 'contact'),
    path('about', About, name = 'about'),
    path('student-login', UserLogin, name = 'studentlogin'),
    path('adminlogin', AdminLogin, name = 'adminlogin'),
    path('registration', Register, name = 'registration'),
    path('student-dashboard', StudentDashboard, name = 'studashboard'),
    path('student-profile', StuProfile, name = 'stuprofile'),
    path('feedback', StudentFeedback, name = 'feedback'),
    path('marks', Marks, name = 'marks'),
    path('prediction', performance_prediction, name = 'prediction'),
    path('change-password', Change_Password, name = 'changepwd'),
    path('forgot-password', Forgot_Password, name = 'forgotpwd'),
    path('reset-password/<str:id>/', Reset_Password, name = 'resetpwd'),
    path('user-logout', uLogout, name = 'logout'),

    # Teacher Urls
    path('admin-dashboard', AdminDashboard, name = 'admindash' ),
    path('admin-add-subject', AdminAddSubject, name = 'add_subject' ),
    path('admin-assign-marks', AdminAssignMarks, name = 'assign_marks' ),
    path('admin-feedback-graph', AdminFeedbackgraph, name = 'admin_feedback_graph' ),
    path('admin-feedback', AdminFeedback, name = 'admin_feedback' ),
    path('admin-manage-marks', AdminManageMarks, name = 'manage_marks' ),
    path('admin-manage-students', AdminManageStudents, name = 'manage_students' ),
    path('admin-manage-subject', AdminManageSubject, name = 'manage_subjects' ),
    path('admin-marks-analysis', AdminMarksAnalysis, name = 'marks_analysis' ),
    path('admin-naive', AdminNaive, name = 'naive' ),
    path('admin-pending-students', AdminPendingStudents, name = 'pending_students' ),
    path('admin-performance-analysis', AdminPerformance, name = 'performance_analysis' ),
    path('admin-sentiment-analysis', AdmiSentiment, name = 'sentiment_analysis' ),
    path('admin-svm', AdminSvm, name = 'svm' ),
    path('admin-upload-dataset', AdminUploadDataset, name = 'upload_dataset' ),
    path('admin-view-dataset', AdminViewDataset, name = 'view_dataset' ),
    path('admin-view-marks/<str:id>', AdminViewMarks, name = 'view_marks' ),
    path('admin-acceptbtn/<str:id>', Acceptbtn, name = 'acc_btn' ),
    path('admin-rejectbtn/<str:id>', Rejectbtn, name = 'rej_btn' ),
    path('admin-changebtn/<str:id>', ChangeStatusBtn, name = 'chan_btn' ),
    path('admin-deletebtn/<str:id>', DeleteBtn, name = 'del_btn' ),
    path('admin-deletesub/<int:id>', Delete_Subject_btn, name = 'del_sub' ),
    path('admin-svmbtn', SvmBtn, name = 'svmbtn' ),
    path('admin-naivebtn', NaiveBtn, name = 'naivebtn' ),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)