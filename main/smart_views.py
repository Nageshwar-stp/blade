from datetime import datetime
from django.shortcuts import render, redirect
from .models import EventGroup, Department, FactultyCoordinator, StudentCoordinator
from django.http import HttpResponse


def coordinators(request, department):
    department_instance = Department.objects.get(name=department)

    all_events = EventGroup.objects.all()
    coordinators = []
    for event in all_events:
        faculty = FactultyCoordinator.objects.filter(
            department=department_instance, event=event).all()
        students = StudentCoordinator.objects.filter(
            department=department_instance, event=event)
        item = {
            'event': event,
            'faculties': faculty,
            'students': students
        }
        coordinators.append(item)

    departments = Department.objects.all()
    data = {
        'departments': departments,
        'department': department_instance,
        'coordinators': coordinators,
    }
    return render(request, 'main/coordinators.html', data)
