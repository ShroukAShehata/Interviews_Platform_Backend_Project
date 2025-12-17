
from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer

from .models import *
from users.serializers import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']

class AnswerSerializer(serializers.ModelSerializer):

    # Nested user serializer to enrich answer response data with author details
    author = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'author', 'content', 'votes', 'created_at', 'updated_at']
        #read only fields to prevent their modification on updates/creation, because they are set automatically system side not by user.
        read_only_fields = ['id', 'author', 'votes', 'created_at', 'updated_at']


@extend_schema_serializer(
    examples = [
        OpenApiExample(
            "Create Question Example",
            value={
                "title": "Explain async programming in Python",
                "description": "Explain concurrency, event loops",
                "skills_required": ['Python', 'Asyncio'],
                "category": "Technical",
            }
        )
    ]
)
class QuestionSerializer(serializers.ModelSerializer):
    # Nested serializers to enrich question response data with related details
    created_by = UserSerializer(read_only=True)
    skills_required = SkillSerializer(many=True, read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'title', 'description', 'category', 'difficulty', 
            'created_by', 'skills_required', 'answers', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'answers', 'created_at', 'updated_at']

