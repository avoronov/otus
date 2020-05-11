from graphene_django.utils.testing import GraphQLTestCase
from learningcenter.schema import schema
from .models import Course, Teacher, Student


class GQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpTestData(cls):
        Course(
            title="Title",
            description="Description",
        ).save()

        Teacher(
            first_name="First name",
            last_name="Last name",
        ).save()

        Student(
            first_name="First name",
            last_name="Last name",
        ).save()

    def test_courses_list(self):
        response = self.query(
            '''
            query {
              courses {
                id
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)

    def test_course_detail(self):
        response = self.query(
            '''
            query {
              course(id:1) {
                id
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)

    def test_teachers_list(self):
        response = self.query(
            '''
            query {
              teachers {
                id
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)

    def test_teacher_detail(self):
        response = self.query(
            '''
            query {
              teacher(id:1) {
                id
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)

    def test_students_list(self):
        response = self.query(
            '''
            query {
              students {
                id
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)

    def test_student_detail(self):
        response = self.query(
            '''
            query {
              student(id:1) {
                id
              }
            }
            '''
        )

        self.assertResponseNoErrors(response)
