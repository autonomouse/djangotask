from rest_framework import serializers
from incling import models


class SchoolSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.School
        fields = ('uuid', 'name', 'address')


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    school = SchoolSerializer()

    class Meta:
        model = models.Classroom
        fields = ('uuid', 'name', 'school')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    classroom = ClassroomSerializer()

    class Meta:
        model = models.Student
        fields = ('uuid', 'firstname', 'middlenames', 'lastname', 'is_active',
                  'is_suspended', 'classroom')
