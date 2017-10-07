from django.http import Http404
from proj1.models import Student, Course, Enroll
from proj1.serializers import StudentSerializer, CourseSerializer, EnrollSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status


class ListView(ListCreateAPIView):

    def created(self, obj):
        return Response(self.serializer_class(instance=obj).data, status.HTTP_201_CREATED)

    def get_kwargs_for_filtering(self):
        filtering_kwargs = {}
        for field in getattr(self, 'my_filter_fields', []):
            field_value = self.request.query_params.get(field)
            if field_value:
                filtering_kwargs[field] = field_value
        return filtering_kwargs

    def get_queryset(self):
        queryset = self.model.objects.all()
        filtering_kwargs = self.get_kwargs_for_filtering()
        if filtering_kwargs:
            queryset = self.model.objects.filter(**filtering_kwargs)
        return queryset


class StudentList(ListView):

    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    my_filter_fields = ['name']

    def create(self, request, *args, **kwargs):
        obj = Student.objects.create(name=request.data.get('name'))
        return self.created(obj)


class CourseList(ListView):

    model = Course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    my_filter_fields = ['name', 'points']

    def create(self, request, *args, **kwargs):
        obj = Course.objects.create(name=request.data.get('name'), points=request.data.get('points'))
        return self.created(obj)


class EnrollList(ListView):

    model = Enroll
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    my_filter_fields = ['student', 'course']

    def create(self, request, *args, **kwargs):
        obj = Enroll.objects.create(student=request.data.get('student_id'), course=request.data.get('course_id'))
        return self.created(obj)


class DetailView(RetrieveUpdateDestroyAPIView):

    def get_object(self):
        try:
            return self.model.objects.get(pk=self.kwargs.get('pk'))
        except self.model.DoesNotExist:
            raise Http404

    def update(self, request, *args, **kwargs):
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


class StudentDetail(DetailView):

    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseDetail(DetailView):

    model = Course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollDetail(DetailView):

    model = Enroll
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.score = request.data['score']
        obj.save()
        return self.get(request, args, kwargs)
