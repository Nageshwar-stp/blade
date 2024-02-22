from django.contrib import admin
from .models import Event, EventCategory, FormData, Course, Master, EventCoordinator, CategoryCoordinator, CategoryCoordinatorStudent

admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(FormData)
admin.site.register(Course)
admin.site.register(Master)
admin.site.register(EventCoordinator)
admin.site.register(CategoryCoordinator)
admin.site.register(CategoryCoordinatorStudent)
