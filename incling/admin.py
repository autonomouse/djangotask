from django import forms
from incling import models
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper


def get_obj_attribute(obj, fields):
    """ The following allows to both 'obj.name' and 'obj.relatedobj.name'
    """
    for lvl in fields.split('.'):
        obj = getattr(obj, lvl)
    return obj

def add_related_field_wrapper(form, col_name):
    """ Register models with custom settings
    """
    rel_model = form.Meta.model
    rel = rel_model._meta.get_field(col_name).rel
    form.fields[col_name].widget = RelatedFieldWidgetWrapper(
        form.fields[col_name].widget, rel, admin.site, can_add_related=True)


class CustomModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        self.field_to_return = kwargs.pop('field_to_return')
        super(CustomModelChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return get_obj_attribute(obj, self.field_to_return)


class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['uuid', 'name', 'address']
    ordering = ['name']

admin.site.register(models.School, SchoolAdmin)


class ClassroomForm(forms.ModelForm):
    school = CustomModelChoiceField(
        field_to_return='name', queryset=models.School.objects.all())

    class Meta:
        model = models.Classroom
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClassroomForm, self).__init__(*args, **kwargs)
        add_related_field_wrapper(self, 'school')


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'school_name']

    def school_name(self, obj):
        return get_obj_attribute(obj, "school.name")

    search_fields = ['uuid', 'name']
    ordering = ['name']
    form = ClassroomForm

admin.site.register(models.Classroom, ClassroomAdmin)


class StudentForm(forms.ModelForm):
    classroom = CustomModelChoiceField(
        field_to_return='name', queryset=models.Classroom.objects.all())

    class Meta:
        model = models.Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        add_related_field_wrapper(self, 'classroom')


class StudentAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'classroom_name', 'school_name']

    def classroom_name(self, obj):
        return get_obj_attribute(obj, 'classroom.name')

    def school_name(self, obj):
        return get_obj_attribute(obj, 'classroom.school.name')

    search_fields = ['uuid', 'firstname', 'lastname']
    ordering = ['lastname', 'firstname']
    form = StudentForm

admin.site.register(models.Student, StudentAdmin)


# Register any models that have not been explicitly registered:
for name, model in apps.all_models['incling'].items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
