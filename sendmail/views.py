from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
import os
from .main import Core

temp_path = 'https://github.com/microsoft/vscode/issues/'
results = {}

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#@staticmethod
def sendmail(request):
    project_name = request.GET['project_name']
    user_manual = request.GET['user_manual']
    issue_data = request.GET['issue_data']

    issue_start_number = request.GET['issue_start_number']
    if not issue_start_number :
        issue_start_number = 1

    issue_end_number = request.GET['issue_end_number']
    if not issue_end_number :
        issue_end_number = 10

    e_mail = request.GET['e_mail']

    if not project_name or not user_manual or not issue_data or not e_mail :
        if not project_name:
            messages.add_message(request, 70, 'Make sure Project_Name field is entered.')
        if not user_manual:
            messages.add_message(request, 20, 'Make sure User_Manual is entered.')
        if not issue_data:
            messages.add_message(request, 30, 'Make sure Issue_Data field is entered.')
        if not e_mail or not ('@' in e_mail and '.' in e_mail) :
            messages.add_message(request, 40, 'Make sure E-mail field is entered and valid.')
        return render(request, 'home.html')

    #send_mail('Notification', 'Mail will send in a few minutes.', 'kej0755@gmail.com', [e_mail])
    #messages.add_message(request, 50, 'Please wait. Mail will send in a few minutes.')
    #return render(request, 'home.html')
    #return project_name, user_manual, issue_data, issue_start_number, issue_end_number, e_mail
    

#def classi(*args):
   # project_name, user_manual, issue_data, issue_start_number, issue_end_number, e_mail = args

    core = Core()
    core.set_params(project_name, user_manual, issue_data)
    htmls = core.data_manage(zip_path='./' + project_name + '.zip')

    global temp_path
    global results

    temp_path = 'https://github.com/microsoft/vscode/issues/'
    results = {'accessibility':[3, [temp_path+'68943', temp_path+'18109', temp_path+'9456']], 'codebasics':[4,[temp_path+'57113', temp_path+'55780', temp_path+'59961', temp_path+'67841']]}
    #os.system('python C:/Users/asd07/Documents/likelion/sendmail_7/sendmail/main.py --project_name {0} --user_manual {1} --issues {2}'.format(project_name, user_manual, issue_data))

    print('\nStart sending\n')
    print(results)
    #return results

    
    #f = open("project_name.html", 'w')

    mail_title = "Project_Name___{0}____".format(project_name)
    mail_body = 'User_Manual : ' + user_manual + '\n' + 'Issue_Data : ' + issue_data + '\n' + 'Result : ' + 'http://127.0.0.1:8000/result/'

    if project_name and user_manual and issue_data and e_mail :
        try:
            mail = EmailMessage(mail_title, mail_body, 'kej0755@gmail.com', [e_mail])
            mail.attach_file('C:/Users/asd07/Documents/likelion/sendmail_7/' + project_name + '.zip')
            mail.send()
            print('\nMail successfully sent.\n')
            return render(request, 'new.html', {'data':results})
        except:
            print('\nMail fail sent.\n')
            messages.add_message(request, 60, 'Make sure E-mail field is valid.')
            return render(request, 'home.html')
        #return render(request, 'result.html', {'htmls':htmls.items()})

def result(request):
    global results
    result = results
    return render(request,'result.html', {'data':result})

def new(request):
    return render(request, 'new.html')

