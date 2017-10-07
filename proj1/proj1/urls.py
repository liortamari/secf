from django.conf.urls import url
from proj1 import views


urlpatterns = [
    url(r'^students/$', views.StudentList.as_view(), name='student-list'),
    url(r'^students/(?P<pk>[a-zA-Z0-9\-]+)/$', views.StudentDetail.as_view(), name='student-detail'),
    url(r'^courses/$', views.CourseList.as_view(), name='course-list'),
    url(r'^courses/(?P<pk>[a-zA-Z0-9\-]+)/$', views.CourseDetail.as_view(), name='course-detail'),
    url(r'^enrolls/$', views.EnrollList.as_view(), name='enroll-list'),
    url(r'^enrolls/(?P<pk>[a-zA-Z0-9\-]+)/$', views.EnrollDetail.as_view(), name='enroll-detail'),

]
