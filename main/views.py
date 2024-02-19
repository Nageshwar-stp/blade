from datetime import datetime
from django.shortcuts import render, redirect
from .models import Event, EventCategory, FormData, Course, Master
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import csv


def index(request):
    events = Event.objects.all().order_by('name')
    event_categories = EventCategory.objects.all()
    formData = FormData.objects.all()
    courses = Course.objects.all()

    data = {
        'events': events,
        'event_categories': event_categories,
        'courses': courses
    }

    if request.method == 'POST':
        admission = request.POST.get('admission')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        course = request.POST.get('course')
        year = request.POST.get('year')
        branch = request.POST.get('branch')
        event_1 = request.POST.get('event-1')
        event_2 = request.POST.get('event-2')
        print(request.POST)
        course_instance = Course.objects.filter(name=course).first()

        if event_1 == event_2:
            messages.error(request, "Cannot Select Same Event Twice")
            return render(request, 'main/index.html', data)

        if not course_instance:
            messages.error(request, "Course does not exist.")
            return render(request, 'main/index.html', data)

        event_1_instance = Event.objects.filter(name=event_1).first()
        if not event_1_instance:
            messages.error(request, "Select atleast one Event")
            return render(request, 'main/index.html', data)

        event_2_instance = Event.objects.filter(name=event_2).first()
        if not event_2_instance:
            event_2_instance = None

        if FormData.objects.filter(admission=admission).exists():
            messages.error(request, "Admission ID already registered.")
            return render(request, 'main/index.html', data)

        if FormData.objects.filter(email=email).exists():
            messages.error(request, "Email Address already registered.")
            return render(request, 'main/index.html', data)

        if not email.endswith('@sanskar.org'):
            messages.error(
                request, "Invalid email. Only College Email is Valid.")
            return render(request, 'main/index.html', data)

        form_data = FormData(
            admission=admission,
            name=name,
            email=email,
            phone=phone,
            course=course_instance,
            year=year,
            event_1=event_1_instance,
            event_2=event_2_instance,
            gender=gender,
            branch=branch
        )
        form_data.save()
        messages.success(request, "Form submitted successfully.")
        return redirect('/success/')

    return render(request, 'main/index.html', data)


def success(request):
    return render(request, 'main/success.html')


def master(request):
    if request.session.has_key('username'):
        submissions = FormData.objects.all()
        category = EventCategory.objects.all()
        courses = Course.objects.all()
        data = {
            'submissions': submissions,
            'categories': category,
            'courses': courses
        }
        return render(request, 'main/master.html', data)
    else:
        return redirect('/master-login/')


def master_login(request):
    if request.session.has_key('username'):
        return redirect('/master/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # check if master exists
            if (Master.objects.filter(username=username, password=password).exists()):
                request.session['username'] = username
                return redirect('/master/')
            else:
                return redirect('/')
    return render(request, 'main/master-login.html')


def download_report(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            category = request.POST.get('category')
            if category is None:
                return redirect('/master/')

            if category == 'all':
                entries = FormData.objects.all()
            else:
                is_course = False
                if Course.objects.filter(name=category).exists():
                    is_course = True

                if is_course:
                    course_instance = Course.objects.filter(
                        name=category).first()
                    entries = FormData.objects.filter(
                        course=course_instance).all()
                else:
                    category_instance = EventCategory.objects.filter(
                        name=category).first()
                    entries = FormData.objects.filter(
                        Q(event_1__category=category_instance) | Q(
                            event_2__category=category_instance)
                    )

            filename = f"{category}_Euphoric2024_{datetime.now()}.csv"
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment;filename="{filename}"'

            writer = csv.writer(response)
            # Write header
            headers = ['AdmissionID', 'Name', 'Email', 'Gender',
                       'Phone', 'Course', 'Branch', 'Year', 'Event_1', 'Event_2']
            writer.writerow(headers)

            # Write data rows
            for entry in entries:
                writer.writerow([
                    str(entry.admission),
                    str(entry.name),
                    str(entry.email),
                    str(entry.gender),
                    str(entry.phone),
                    str(entry.course),
                    str(entry.branch),
                    str(entry.year),
                    str(entry.event_1),
                    str(entry.event_2),
                ])

            return response

        else:
            return redirect('/')
    return redirect('/')


def logout(request):
    try:
        del request.session['username']
    except Exception as e:
        print(e)
        pass

    return redirect('/')