
from ..models import *
from django.core.exceptions import PermissionDenied


class QuestionService:
    @staticmethod
    def create_question(user, data):
        if user.role not in ['expert', 'admin']:
            raise PermissionDenied("You cannot create a question")
        #The below 
        skills = data.pop('skills', [])
        question = Question.objects.create(created_by=user, **data)
        if skills:
            question.skills_required.set(skills)
        return question

class AnswerService:
    @staticmethod
    def create_answer(user, question, content):
        if user.role not in ['expert', 'admin']:
            raise PermissionDenied("Only experts can answer")
        return Answer.objects.create(author=user, question=question, content=content)

'''
class StudyPlanService:
    @staticmethod
    def add_question_to_plan(plan, question):
        item, created = StudyPlanItem.objects.get_or_create(plan=plan, question=question)
        return item

    @staticmethod
    def mark_item_complete(item):
        item.is_completed = True
        item.completed_at = timezone.now()
        item.save()
        return item
'''
