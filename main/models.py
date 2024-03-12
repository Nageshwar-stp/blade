from django.db import models
from datetime import datetime


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year = models.IntegerField()

    def __str__(self):
        return self.name


class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        EventCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class FormData(models.Model):
    admission = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField()
    event_1 = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, related_name="event_1")
    event_2 = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="event_2")

    def __str__(self):
        return f"{self.name} [{self.course}]"


class Master(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class CategoryCoordinator(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.name}"


class CategoryCoordinatorFaculty(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.name}"


class CategoryCoordinatorStudent(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.name}"


class EventCoordinator(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.event} - {self.name}"


class LatestNews(models.Model):
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.text


# DATA-MODELS-PREPARED-FOR-COORDINATORS -------------------->

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    # HEAD FACULTY COORDINATORS
    cultural = models.CharField(max_length=100, null=True, blank=True)
    sports = models.CharField(max_length=100, null=True, blank=True)
    technical = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class EventGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class FactultyCoordinator(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(EventGroup, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.event} - {self.department}'


class StudentCoordinator(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    event = models.ForeignKey(EventGroup, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.year}'
