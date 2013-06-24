from django.contrib import admin
from engine.models import list_object
from engine.models import object_object
from engine.models import parameter_object
from engine.models import Document

class ObjectInline(admin.StackedInline):
    model = object_object

class ParameterInline(admin.StackedInline):
    model = parameter_object

class ListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['title']}),
    ]
    inlines = [ObjectInline]

class ObjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['title', 'master_list']}),
    ]
    inlines = [ParameterInline]

class ParameterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['title','master_object']}),
    ]

class DataAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['title','docfile']}),
    ]

admin.site.register(list_object, ListAdmin)
admin.site.register(object_object, ObjectAdmin)
admin.site.register(parameter_object, ParameterAdmin)
admin.site.register(Document, DataAdmin)

