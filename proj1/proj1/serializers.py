from django.contrib.auth.models import User
from proj1.models import Student, Course, Enroll
from rest_framework.serializers import ModelSerializer
from rest_framework_mongoengine.serializers import DocumentSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class StudentSerializer(DocumentSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name')
        depth = 2


class CourseSerializer(DocumentSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'points')
        depth = 2


class EnrollSerializer(DocumentSerializer):
    class Meta:
        model = Enroll
        fields = ('id', 'student', 'course', 'score')
        depth = 2