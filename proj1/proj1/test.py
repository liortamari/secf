from django.test import TestCase
from django.http import QueryDict
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient
from proj1.models import Student, Course, Enroll
import random
from django.core.urlresolvers import reverse
from rest_framework import status


class MyTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.students = []
        self.students.append(Student(name="student-1"))
        self.students.append(Student(name="student-2"))
        self.students.append(Student(name="student-3"))
        for s in self.students:
            s.save()
        self.courses = []
        self.courses.append(Course(name="course-1", points=2))
        self.courses.append(Course(name="course-2", points=1))
        self.courses.append(Course(name="course-3", points=2))
        for c in self.courses:
            c.save()
        self.enrolls = []
        self.enrolls.append(Enroll(student=self.students[0].id, course=self.courses[0].id))
        self.enrolls.append(Enroll(student=self.students[0].id, course=self.courses[1].id))
        self.enrolls.append(Enroll(student=self.students[1].id, course=self.courses[0].id))
        for e in self.enrolls:
            e.save()

    def tearDown(self):
        Student.objects.all().delete()
        Course.objects.all().delete()
        Enroll.objects.all().delete()

    def test_get_students(self):
        url = reverse('student-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), len(self.students))

    def test_get_student(self):
        student = random.choice(Student.objects.all())
        url = reverse('student-detail', kwargs={'pk': student.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('id'), str(student.id))

    def test_post_student(self):
        payload = {'name': get_random_string()}
        resp = self.client.post(reverse('student-list'), data=payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_del_student(self):
        student = random.choice(Student.objects.all())
        url = reverse('student-detail', kwargs={'pk': student.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_courses(self):
        url = reverse('course-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), len(self.courses))

    def test_get_course(self):
        course = random.choice(Course.objects.all())
        url = reverse('course-detail', kwargs={'pk': course.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('id'), str(course.id))

    def test_post_course(self):
        payload = {'name': get_random_string(), 'points': random.randint(1, 5)}
        resp = self.client.post(reverse('course-list'), data=payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_del_course(self):
        course = random.choice(Course.objects.all())
        url = reverse('course-detail', kwargs={'pk': course.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_enrolls(self):
        url = reverse('enroll-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), len(self.enrolls))

    def test_get_enroll(self):
        enroll = random.choice(Enroll.objects.all())
        url = reverse('enroll-detail', kwargs={'pk': enroll.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('id'), str(enroll.id))

    def test_post_enroll(self):
        student = random.choice(Student.objects.all())
        course = random.choice(Course.objects.all())
        payload = {'student_id': student.id, 'course_id': course.id}
        resp = self.client.post(reverse('enroll-list'), data=payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_del_enroll(self):
        enroll = random.choice(Enroll.objects.all())
        url = reverse('enroll-detail', kwargs={'pk': enroll.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_enroll(self):
        enroll = random.choice(Enroll.objects.all())
        url = reverse('enroll-detail', kwargs={'pk': enroll.id})
        payload = {'score': random.randint(0, 100)}
        resp = self.client.patch(url, data=payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('score'), payload['score'])

    def test_get_student_filter(self):
        student = random.choice(Student.objects.all())
        url = reverse('student-list')
        query_params = '{}={}'.format('name', student.name)
        resp = self.client.get(url, data=QueryDict(query_params))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0].get('id'), str(student.id))

    def test_get_course_filter(self):
        url = reverse('course-list')
        query_params = '{}={}'.format('points', 2)
        resp = self.client.get(url, data=QueryDict(query_params))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)
        for c in resp.data:
            self.assertEqual(c.get('points'), 2)

    def test_get_enroll_filter(self):
        url = reverse('enroll-list')
        self.enrolls.append(Enroll(student=self.students[1].id, course=self.courses[0].id))
        query_params = '{}={};{}={}'.format('student', self.students[1].id, 'course', self.courses[0].id)
        resp = self.client.get(url, data=QueryDict(query_params))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0].get('student').get('name'), self.students[1].name)
        self.assertEqual(resp.data[0].get('course').get('name'), self.courses[0].name)


class MyBadTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_del_student(self):
        student = Student(name="student")
        student.save()
        student.delete()
        url = reverse('student-detail', kwargs={'pk': student.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_del_course(self):
        course = Course(name="course", points=1)
        course.save()
        course.delete()
        url = reverse('course-detail', kwargs={'pk': course.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_del_enroll(self):
        student = Student(name="student")
        student.save()
        student.delete()
        course = Course(name="course", points=1)
        course.save()
        course.delete()
        enroll = Enroll(student=student, course=course)
        enroll.save()
        enroll.delete()
        url = reverse('enroll-detail', kwargs={'pk': enroll.id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

