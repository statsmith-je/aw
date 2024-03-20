from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .read_doc import CourseInfo
from .forms import UploadFileForm, SignUpForm, CreateCourse, UploadMultipleFilesForm
from .models import PTB, TLO, ELO, Course, Module
from django.db.models import Count, Q
from io import BytesIO
import pandas as pd

from .slide_info import Pres


def search(request):

    # Check if the request is a post request.
    if request.method == 'POST':
        
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']

        # Filter your model by the search query
        try: 
            int_q = int(search_query)
        except:
            int_q = None
        
        if int_q:
            ptb_info = PTB.objects.filter(ptb = int_q).values_list('id', flat=True)
            module_info = Module.objects.filter(ptbs__in = ptb_info)
        else:
            elo_info = ELO.objects.filter(elo__icontains = search_query).values_list('id', flat=True)
            ptb_info = PTB.objects.filter(ptb__icontains = search_query).values_list('id', flat=True)
            tlo_info = TLO.objects.filter(tlo__icontains = search_query).values_list('id', flat=True)
            comp_info = Competency.objects.filter(competency__icontains = search_query)
            multiple_q = Q(Q(ptbs__in = ptb_info) | Q(tlos__in = tlo_info) | Q(elos__in = elo_info) | Q(competencies__in = comp_info) | Q(module_title__icontains = search_query))
            module_info = Module.objects.filter(multiple_q)
           

        

        return render(request, 'db/search.html', {'query':search_query, "modules": module_info, 'ptb': int_q})
    else:
        return render(request, 'db/search.html',{})

def elo_search(request):

    # Check if the request is a post request.
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        
        # Filter model by the search query
        elo_info = ELO.objects.filter(elo__icontains = search_query)
        
        elo_output = {}
        for elo in elo_info.values():
            # elo_output[elo['elo']] = Module.objects.filter(elos__id = elo['id']).values()
            # module_info = Module.objects.filter(elos__id = elo['id']).values()
            if Module.objects.filter(elos__id = elo['id']).exists():
                elo_output[elo['elo']] = Module.objects.filter(elos__id = elo['id'])
                
        # print(elo_output)

        return render(request, 'elo.html', {'query':search_query, 'elos': elo_output})
    else:
        return render(request, 'elo.html',{})


def course(request, pk):
    
    course_info = Course.objects.get(pk = pk)
    module_info = Module.objects.order_by('module_number').filter(course__id=pk)
    module_info = module_info.annotate(total_elos = Count('elos'))
    
    return render(request, 'db/course.html',{'course': course_info, 'modules': module_info} )

def db_home(request):
    
    course_info = Course.objects.all().order_by('cadre_acronym')
    
    return render(request, 'db/home.html',{'courses': course_info})

def module(request, pk):
    
    module_info = Module.objects.get(pk = pk)
    return render(request, 'db/module.html', {'modules': module_info})


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            test = CourseInfo(form.cleaned_data["file"])
            test.course_id(str(form.cleaned_data["code"]))
            test.read_ig()
            test.get_ptbs()
            test.get_tlo()
            test.get_elos()
            test.get_dhs()

            module = form.cleaned_data["module"]
            module_title = form.cleaned_data["module_title"]
            minutes_to_complete = form.cleaned_data["minutes_to_complete"]
            number_of_slides = form.cleaned_data["number_of_slides"]
            number_of_activities = form.cleaned_data["number_of_activities"]

            course_info = Course.objects.get(code = test._course_id)
            module_info = Module.objects.filter(course__id=course_info.id).filter(module_number=module)

            print(module_info)
            if not module_info.exists():
                print('adding module')
                module_info = Module.objects.create(course = course_info, module_number = module, module_title = module_title, minutes_to_complete = minutes_to_complete, number_of_slides = number_of_slides, number_of_activities = number_of_activities)
            else:
                module_info = module_info[0]
                # print(module_info)
                
            for comp in test.dhs:
                if not Competency.objects.filter(competency=comp).exists():
                    # print(f'{ptb_num}: {ptb_text} does not exists')
                    Competency.objects.create(competency = comp)

                comp_id = Competency.objects.get(competency = comp)
                
                if not Module.objects.filter(course__id=course_info.id).filter(module_number=module).filter(competencies__id=comp_id.id).exists():
                    print(f"Attaching DSH Competency {comp_id.id} to module")
                    module_info.competencies.add(comp_id.id)
            
            for ptb_num, ptb_text in test.ptb.items():
                ptb_num = int(ptb_num)
                if not PTB.objects.filter(ptb=ptb_num).exists():
                    print(f'{ptb_num}: {ptb_text} does not exists')
                    PTB.objects.create(ptb = ptb_num, description=ptb_text)
                
                ptb_id = PTB.objects.get(ptb = ptb_num)
                if not Module.objects.filter(course__id=course_info.id).filter(module_number=module).filter(ptbs__id=ptb_id.id).exists():
                    print(f"Attaching PTB {ptb_num} to module")
                    module_info.ptbs.add(ptb_id.id)

            for tlo in test.tlo:
                if not TLO.objects.filter(tlo=tlo).exists():
                    # print(f'{ptb_num}: {ptb_text} does not exists')
                    TLO.objects.create(tlo = tlo)

                tlo_id = TLO.objects.get(tlo = tlo)
                if not Module.objects.filter(course__id=course_info.id).filter(module_number=module).filter(tlos__id=tlo_id.id).exists():
                    print(f"Attaching TLO {tlo_id.id} to module")
                    module_info.tlos.add(tlo_id.id)

            for elo in test.elos:
                if not ELO.objects.filter(elo=elo).exists():
                    # print(f'{ptb_num}: {ptb_text} does not exists')
                    ELO.objects.create(elo = elo)
                
                elo_id = ELO.objects.get(elo = elo)
                
                if not Module.objects.filter(course__id=course_info.id).filter(module_number=module).filter(elos__id=elo_id.id).exists():
                    print(f"Attaching ELO {elo_id.id} to module")
                    module_info.elos.add(elo_id.id)

            return HttpResponseRedirect(reverse('modules', args=(module_info.pk,)))
    else:
        form = UploadFileForm()
    return render(request, "db/upload.html", {"form": form})

def add_course(request):
    # context ={}
    if request.method == "POST":
    # create object of form
        form = CreateCourse(request.POST or None, request.FILES or None)
        
        # check if form data is valid
        if form.is_valid():
            # save the form data to model
            new = form.save()

        # context['form']= form
        
            
            return redirect('db_home')
    else:
        form = CreateCourse()
        return render(request, "db/add_course.html", {"form": form})
    
def home(request):
    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in. Please try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

#Logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return render(request, 'home.html', {})

#register
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})


def edit_course(request, pk):
    if request.user.is_authenticated:
        course_info = Course.objects.get(pk = pk)
        form = CreateCourse(request.POST or None, instance = course_info)
        if form.is_valid():
            form.save()
            messages.success(request, ("Course updated"))
            return redirect('db_home')

        return render(request, 'db/edit_course.html', {'form': form, 'course': course_info})
    else:
        messages.success(request, ("You must be logged in"))
    return redirect('home')


#Slide info
def slide_titles(request):
    if request.method == "POST":
        form = UploadMultipleFilesForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES["file"]
            module = form.cleaned_data['modules']
            modules = [m.strip() for m in module.split(",")]
            file_name = form.cleaned_data['file_name']

            ppt_info = Pres(modules, files)
            slide_info = ppt_info.info
            with BytesIO() as b:
                # Use the StringIO object as the filehandle.
                writer = pd.ExcelWriter(b, engine='xlsxwriter')
                slide_info.to_excel(writer, sheet_name='Sheet1', index = False)
                writer.close()
                filename = file_name
                content_type = 'application/vnd.ms-excel'
                response = HttpResponse(b.getvalue(), content_type=content_type)
                response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
                messages.success(request, f"Titles successfully extracted!")
                return response
    else:
        form = UploadMultipleFilesForm()
    return render(request, "automation/slide_titles.html", {"form": form})