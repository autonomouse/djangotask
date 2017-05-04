from rest_framework import serializers
from incling import models


class SchoolSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.School
        fields = ('uuid', 'name', 'address')


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Student
        fields = ('uuid', 'firstname', 'middlenames', 'lastname', 'is_active',
                  'is_suspended')


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    school = SchoolSerializer()
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Classroom
        fields = ('uuid', 'name', 'school', 'students')
