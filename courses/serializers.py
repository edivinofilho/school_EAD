from .models import Course
from accounts.models import Account
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from contents.serializers import ContentSerializer
from students_courses.serializers import StudentCourseSerializer


class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    students_courses = StudentCourseSerializer(many=True, read_only=True)
    name = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(
                queryset=Course.objects.all(),
                message="course with this name already exists.",
            )
        ],
    )
    
    class Meta:
        model = Course
        fields = ["id", "name", "status", "start_date", "end_date", "instructor", "contents", "students_courses"]
        extra_kwargs = {
            "contents": {
                "read_only": True
            },
            "students_courses": {
                "read_only": True
            }
        }

    # def create(self, validated_data):
    #     # instructor = validated_data.pop("instructor", None)  
    #     course = Course.objects.create(**validated_data)
        
    #     course.contents = []
    #     course.students_courses = []
        
    #     return course


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class CreateCourse(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "status", "start_date", "end_date", "instructor", "contents", "students_courses"]
        extra_kwargs = {
            "contents": {
                "read_only": True
            },
            "students_courses": {
                "read_only": True
            }
        }

    name = serializers.CharField(
        max_length=100,
        validators=[
        UniqueValidator(
            queryset=Course.objects.all(),
            message="course with this name already exists.",
        )
    ],
)
    
class AddStudentCourse(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(many=True)
    class Meta:
        model = Course
        fields = ["id", "name", "students_courses"] 
        extra_kwargs = {
            "name" : {"read_only": True}
        }

    def update(self, instance, validated_data):
        students = []
        not_found = []
        for studant_course in validated_data["students_courses"]:
            student = studant_course["student"]
            found = Account.objects.filter(email=student["email"]).first()
            if not found:
                not_found.append(student["email"])
            else:
                students.append(found)

        if not_found:
            raise serializers.ValidationError({"detail":f"No active accounts was found: {', '.join(not_found)}."})
        instance.students.add(*students)
        return instance
