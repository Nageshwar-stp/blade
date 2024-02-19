from django.db import models


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
