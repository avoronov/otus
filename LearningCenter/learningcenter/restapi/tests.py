import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.test import APITestCase, APITransactionTestCase

from .factories import CourseFactory, TeacherFactory, StudentFactory
from .views import CourseViewSet


def _build_persons(count=3):
    result = []
    for i in range(1, count + 1):
        result.append({
            "first_name": f"First name #{i}",
            "last_name": f"Last name #{i}",
        })
    return result


class CoursesTestCase(APITestCase):
    COURSES = None
    USER = None

    @classmethod
    def setUpClass(cls):
        super(CoursesTestCase, cls).setUpClass()
        cls.USER = User()

    @classmethod
    def setUpTestData(cls):
        courses = []
        for i in range(1, 4):
            courses.append({
                "title": f"Course #{i} title",
                "description": f"Course #{i} description",
                "is_active": bool(i % 2)
            })

        for el in courses:
            course = CourseFactory(**el)
            el["id"] = course.id

        cls.COURSES = courses

    def test_courses_list(self):
        request = APIRequestFactory().get("")
        course_view = CourseViewSet.as_view({"get": "list"})
        response = course_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.COURSES)

    def test_courses_detail(self):
        course = self.COURSES[0]
        request = APIRequestFactory().get("")
        course_view = CourseViewSet.as_view({"get": "retrieve"})
        response = course_view(request, pk=course['id']).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), course)

    def test_courses_create_wo_auth(self):
        request = APIRequestFactory().post("", {}, format="json")
        course_view = CourseViewSet.as_view({"post": "create"})
        response = course_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_courses_create(self):
        actual_course = {"title": "test course created", "description": "very long text", "is_active": True}
        request = APIRequestFactory().post("", actual_course, format="json")
        force_authenticate(request, user=self.USER)
        course_view = CourseViewSet.as_view({"post": "create"})
        response = course_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        got_course = json.loads(response.content)
        self.assertIsNotNone(got_course["id"])
        got_course.pop("id")
        self.assertEqual(actual_course, got_course)

    def test_courses_update_wo_auth(self):
        request = APIRequestFactory().put("", {}, format="json")
        course_view = CourseViewSet.as_view({"put": "update"})
        response = course_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_courses_update(self):
        course = self.COURSES[0]
        actual_course = {"title": "course #1 updated", "description": "very long text", "is_active": False}
        request = APIRequestFactory().put("", actual_course, format="json")
        force_authenticate(request, user=self.USER)
        course_view = CourseViewSet.as_view({"put": "update"})
        response = course_view(request, pk=course['id']).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        got_course = json.loads(response.content)
        actual_course["id"] = course["id"]
        self.assertEqual(actual_course, got_course)

    def test_courses_partial_update_wo_auth(self):
        request = APIRequestFactory().patch("", {}, format="json")
        course_view = CourseViewSet.as_view({"put": "partial_update"})
        response = course_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_courses_partial_update(self):
        course = self.COURSES[0]
        actual_course = {"title": "course #1 updated again"}
        request = APIRequestFactory().patch("", actual_course, format="json")
        force_authenticate(request, user=self.USER)
        course_view = CourseViewSet.as_view({"patch": "partial_update"})
        response = course_view(request, pk=course['id']).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        got_course = json.loads(response.content)
        self.assertEqual(actual_course["title"], got_course["title"])

    def test_courses_delete_wo_auth(self):
        request = APIRequestFactory().delete("")
        course_view = CourseViewSet.as_view({"delete": "destroy"})
        response = course_view(request).render()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_courses_delete(self):
        course = self.COURSES[0]
        request = APIRequestFactory().delete("")
        force_authenticate(request, user=self.USER)
        course_view = CourseViewSet.as_view({"delete": "destroy"})
        response = course_view(request, pk=course['id']).render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TeachersTestCase(APITransactionTestCase):
    TEACHERS = None
    USER = None

    @classmethod
    def setUpClass(cls):
        super(TeachersTestCase, cls).setUpClass()
        cls.USER = User()

    @classmethod
    def setUp(cls):
        teachers = _build_persons()
        for el in teachers:
            teacher = TeacherFactory(**el)
            el["id"] = teacher.id

        cls.TEACHERS = teachers

    def test_teachers_list(self):
        response = self.client.get("/rest-api/teachers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.TEACHERS)

    def test_teachers_detail(self):
        teacher = self.TEACHERS[0]
        response = self.client.get(f"/rest-api/teachers/{teacher['id']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), teacher)

    def test_teachers_create_wo_auth(self):
        response = self.client.post("/rest-api/teachers/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_teachers_create(self):
        self.client.force_authenticate(user=self.USER)
        actual_person = {"last_name": "Teacher", "first_name": "New"}
        response = self.client.post("/rest-api/teachers/", actual_person, format="json")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        got_person = json.loads(response.content)
        self.assertIsNotNone(got_person["id"])
        got_person.pop("id")
        self.assertEqual(actual_person, got_person)

    def test_teachers_update_wo_auth(self):
        teacher = self.TEACHERS[0]
        response = self.client.put(f"/rest-api/teachers/{teacher['id']}/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_teachers_update(self):
        self.client.force_authenticate(user=self.USER)
        teacher = self.TEACHERS[0]
        actual_person = {"last_name": "Teacher", "first_name": "New"}
        response = self.client.put(f"/rest-api/teachers/{teacher['id']}/", actual_person, format="json")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        got_person = json.loads(response.content)
        actual_person["id"] = got_person["id"]
        self.assertEqual(actual_person, got_person)

    def test_teachers_partial_update_wo_auth(self):
        teacher = self.TEACHERS[0]
        response = self.client.patch(f"/rest-api/teachers/{teacher['id']}/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_teachers_partial_update(self):
        self.client.force_authenticate(user=self.USER)
        teacher = self.TEACHERS[0]
        actual_person = {"last_name": "Teacher"}
        response = self.client.patch(f"/rest-api/teachers/{teacher['id']}/", actual_person, format="json")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        got_person = json.loads(response.content)
        self.assertEqual(actual_person["last_name"], got_person["last_name"])

    def test_teachers_delete_wo_auth(self):
        teacher = self.TEACHERS[0]
        response = self.client.delete(f"/rest-api/teachers/{teacher['id']}/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_teachers_delete(self):
        self.client.force_authenticate(user=self.USER)
        teacher = self.TEACHERS[0]
        response = self.client.delete(f"/rest-api/teachers/{teacher['id']}/")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class StudentsTestCase(APITestCase):
    STUDENTS = None
    USER = None

    @classmethod
    def setUpClass(cls):
        super(StudentsTestCase, cls).setUpClass()
        cls.USER = User()

    @classmethod
    def setUpTestData(cls):
        students = _build_persons()
        for el in students:
            student = StudentFactory(**el)
            el["id"] = student.id

        cls.STUDENTS = students

    def test_students_list(self):
        response = self.client.get("/rest-api/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), self.STUDENTS)

    def test_students_detail(self):
        student = self.STUDENTS[0]
        response = self.client.get(f"/rest-api/students/{student['id']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), student)

    def test_students_create_wo_auth(self):
        response = self.client.post("/rest-api/students/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_students_create(self):
        self.client.force_authenticate(user=self.USER)
        actual_person = {"last_name": "Student", "first_name": "New"}
        response = self.client.post("/rest-api/students/", actual_person, format="json")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        got_person = json.loads(response.content)
        self.assertIsNotNone(got_person["id"])
        got_person.pop("id")
        self.assertEqual(actual_person, got_person)

    def test_students_update_wo_auth(self):
        student = self.STUDENTS[0]
        response = self.client.put(f"/rest-api/students/{student['id']}/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_students_update(self):
        self.client.force_authenticate(user=self.USER)
        student = self.STUDENTS[0]
        actual_person = {"last_name": "Student", "first_name": "New"}
        response = self.client.put(f"/rest-api/students/{student['id']}/", actual_person, format="json")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        got_person = json.loads(response.content)
        actual_person["id"] = got_person["id"]
        self.assertEqual(actual_person, got_person)

    def test_students_partial_update_wo_auth(self):
        student = self.STUDENTS[0]
        response = self.client.patch(f"/rest-api/students/{student['id']}/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_students_partial_update(self):
        self.client.force_authenticate(user=self.USER)
        student = self.STUDENTS[0]
        actual_person = {"last_name": "Teacher"}
        response = self.client.patch(f"/rest-api/students/{student['id']}/", actual_person, format="json")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        got_person = json.loads(response.content)
        self.assertEqual(actual_person["last_name"], got_person["last_name"])

    def test_students_delete_wo_auth(self):
        student = self.STUDENTS[0]
        response = self.client.delete(f"/rest-api/students/{student['id']}/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_delete(self):
        self.client.force_authenticate(user=self.USER)
        student = self.STUDENTS[0]
        response = self.client.delete(f"/rest-api/students/{student['id']}/")
        self.client.force_authenticate()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

