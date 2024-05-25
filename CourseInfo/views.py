from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.core.mail import send_mail

def insights(request):
    
    return render(request, 'landing_page/insights/insights.html', {})

def home(request):
    
    return render(request, 'landing_page/home.html', {})


def about(request):
    
    return render(request, 'landing_page/about.html', {})

def contact(request):
    # CONTACT FORM
    if request.method == 'POST':
        name = f"{request.POST.get('lname')} {request.POST.get('fname')}"
        email = request.POST.get('email')
        reason = request.POST.get('reason')
        message = request.POST.get('message')
        form_data = {
            'name':name,
            'email':email,
            'reason':reason,
            'message':message,
        }
        message = f'''
        From:\n\t\t{form_data['name']}\n
        Reason:\n\t\t{form_data['reason']}\n
        Message:\n\t\t{form_data['message']}\n
        Email:\n\t\t{form_data['email']}\n
        reason
        '''
        send_mail('Message from website!', message, '', ['jesmithstats@gmail.com']) 
        return render(request, 'landing_page/contact.html', {})
    else:

        return render(request, 'landing_page/contact.html', {})

def blog(request):
    
    return render(request, 'landing_page/insights/blog.html', {})


def blog(request):
    
    return render(request, 'landing_page/insights/blog.html', {})


def learninganalytics(request):
    
    return render(request, 'landing_page/services/learninganalytics.html', {})


def ai(request):
    
    return render(request, 'landing_page/services/ai.html', {})


def data_analytics(request):
    
    return render(request, 'landing_page/services/data.html', {})


def secure_tech(request):
    
    return render(request, 'landing_page/services/it.html', {})

def consulting(request):
    
    return render(request, 'landing_page/services/consulting.html', {})

def capability(request):
    
    return render(request, 'landing_page/capability.html', {})


class InsightsView(DetailView):
    model = None
    template_name = 'insights_post.html'

def services(request):
    
    return render(request, 'landing_page/services/list.html', {})



class Services(DetailView):
    model = None
    template_name = 'list.html'