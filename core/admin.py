from django.contrib import admin
from . models import CustomUser, Company, Application, Resume, Offer, Interview, Question


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Application)
admin.site.register(Resume)
admin.site.register(Offer)
admin.site.register(Interview)
admin.site.register(Question)