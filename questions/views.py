
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from rest_framework.response import Response


from .models import *
from .serializers import *
from .services.analytics import *
from .services.crud import *
from .permissions import *
from users.throttles import *


# Skills 
@extend_schema_view(
    list=extend_schema(tags=["Skills"]),
    create=extend_schema(tags=["Skills"]),
    retrieve=extend_schema(tags=["Skills"]),
    update=extend_schema(tags=["Skills"]),
    partial_update=extend_schema(tags=["Skills"]),
    destroy=extend_schema(tags=["Skills"]),
)
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]

# Questions
@extend_schema_view(
    list=extend_schema(tags=["Questions"]),
    create=extend_schema(tags=["Questions"]),
    retrieve=extend_schema(tags=["Questions"]),
    update=extend_schema(tags=["Questions"]),
    partial_update=extend_schema(tags=["Questions"]),
    destroy=extend_schema(tags=["Questions"]),
)
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


    #perform_create (hook for ModelViewSet) is now overridden to use QuestionService for question creation logic after validation before saving.
    #parameters are self which is the viewset instance and serializer which holds validated data.
    def perform_create(self, serializer):
        QuestionService.create_question(self.request.user, serializer.validated_data)

    # Permissions
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [perm() for perm in permission_classes]

    throttle_scope = "write"  # used by ScopedPerIPThrottle, will be overridden in get_throttle() based on CRUD method

    def get_throttles(self):
        # No throttling for GET, LIST, RETRIEVE
        if self.action in ["list", "retrieve"]:
            return []

        # Rolebased & Scope throttling for POST, PUT, PATCH, DELETE
        return [
            RoleBasedUserThrottle(),
            ScopedPerIPThrottle()
        ]


# Answers
@extend_schema_view(
    list=extend_schema(tags=["Answers"]),
    create=extend_schema(tags=["Answers"]),
    retrieve=extend_schema(tags=["Answers"]),
    update=extend_schema(tags=["Answers"]),
    partial_update=extend_schema(tags=["Answers"]),
    destroy=extend_schema(tags=["Answers"]),
)
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        AnswerService.create_answer(self.request.user, question, serializer.validated_data['content'])

    # Permissions
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner, IsExpertUser, ]
        else:
            permission_classes = [IsAuthenticated, IsExpertUser, ]
        return [perm() for perm in permission_classes]

    throttle_scope = "write"

    def get_throttles(self):
        # No throttling for GET, LIST, RETRIEVE
        if self.action in ["list", "retrieve"]:
            return []

        # Rolebased & Scope throttling for POST, PUT, PATCH, DELETE
        return [
            RoleBasedUserThrottle(),
            ScopedPerIPThrottle()
        ]



'''
# Study Plans
class StudyPlanViewSet(viewsets.ModelViewSet):
    queryset = StudyPlan.objects.all()
    serializer_class = StudyPlanSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
'''

#_____________________________________  Analytics ____________________________________________#


@extend_schema_view(
    top_questions=extend_schema(tags=["Analytics"]),
    trending_questions=extend_schema(tags=["Analytics"]),
    skills_heatmap=extend_schema(tags=["Analytics"]),
    #user_progress=extend_schema(tags=["Analytics"])
)
class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    throttle_classes = [ScopedPerIPThrottle]
    throttle_scope = "analytics"

    @action(detail=False, methods=["get"], url_path="top-questions")
    def top_questions(self, request):
        limit = int(request.query_params.get('limit', 10))
        data = AnalyticsService.top_questions(limit)
        return Response(data)

    @action(detail=False, methods=["get"], url_path="trending-questions")
    def trending_questions(self, request):
        limit = int(request.query_params.get('limit', 10))
        data = AnalyticsService.trending_questions(limit)
        return Response(data)

    @action(detail=False, methods=["get"], url_path="top-skills")
    def skills_heatmap(self, request):
        data = AnalyticsService.skills_heatmap()
        return Response(data)

    '''
    @action(detail=False, methods=["get"], url_path="user-progress")
    def user_progress(self, request):
        user_id = request.query_params.get("user_id") or \
                  (request.user.id if request.user.is_authenticated else None)

        if not user_id:
            return Response({"detail": "Authentication required or provide user_id"}, status=400)

        data = AnalyticsService.user_progress(user_id)
        return Response(data)
    '''