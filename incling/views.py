from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets, filters
from config import APP_VERSION, AUTHORS, PRIMARY_APP_NAME
from incling import models, serializers


def main_page(request):
    return render(request, 'index.html', {
        'app_name': PRIMARY_APP_NAME,
        'TMYear': datetime.now().year,
        'version': APP_VERSION,
        'authors': " ".join(AUTHORS), })


class SchoolViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows schools to be viewed or edited.
    """
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('uuid', 'name', 'address', )


class ClassroomViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows classrooms to be viewed or edited.
    """
    queryset = models.Classroom.objects.all().order_by('name')
    serializer_class = serializers.ClassroomSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('uuid', 'name',  'school__name', )


class StudentViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows students to be viewed or edited.
    """
    queryset = models.Student.objects.all().order_by('lastname', 'firstname')
    serializer_class = serializers.StudentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('uuid', 'firstname', 'middlenames', 'lastname',
                     'is_active', 'is_suspended', 'classroom__name', )
