# core/analytics_service.py
import json
from django.core.cache import cache
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from ..models import Question, Skill, Answer
from users.throttles import *
from django.conf import settings
import math

CACHE_PREFIX = "analytics:"
DEFAULT_TTL = 60 * 10  # 10 minutes


class AnalyticsService:
    

    @staticmethod
    def _cache_get(key):
        val = cache.get(key)
        if val is None:
            return None
        try:
            return json.loads(val)
        except Exception:
            return val

    @staticmethod
    def _cache_set(key, value, ttl=DEFAULT_TTL):
        cache.set(key, json.dumps(value), ttl)


    #_________________________________ Analysis _______________________________________#

    @staticmethod
    def top_questions(limit=10):
        key = f"{CACHE_PREFIX}top_questions:{limit}"
        result = AnalyticsService._cache_get(key)
        if result is not None:
            return result

        #Questions by answers count
        qs = Question.objects.annotate(answers_count=Count("answers")).order_by("-answers_count")[:limit]
        result = [ {"id": q.id, "title": q.title, "answers_count": q.answers_count}  for q in qs]

        AnalyticsService._cache_set(key, result)

        return result


    @staticmethod
    def skills_heatmap():
        key = f"{CACHE_PREFIX}skills:heatmap"
        result = AnalyticsService._cache_get(key)
        if result is not None:
            return result

        #Skills by questions count
        qs = Skill.objects.annotate(questions_count=Count("questions")).order_by("-questions_count")
        result = [{"skill_id": s.id, "name": s.name, "count": s.questions_count} for s in qs]

        AnalyticsService._cache_set(key, result, ttl=60*60)  # 1 hour

        return result


    @staticmethod
    def trending_questions(limit=10, decay_hours=48):
        """
        Create a trending score combining:
          - answers count
          - votes on answers
          - time decay (newer items favored)
        """
        key = f"{CACHE_PREFIX}trending:{limit}:{decay_hours}"
        result = AnalyticsService._cache_get(key)
        if result is not None:
            return result

        now = timezone.now()
        recent_threshold = now - timedelta(days=7) 
        # consider only questions during last 7 days
        qs = Question.objects.annotate(answers_count=Count("answers")).filter(created_at__gte=recent_threshold)

        scored = []
        for q in qs:

            #Total votes on answers of evry question
            answer_votes = q.answers.aggregate(total_votes=Count("votes"))['total_votes'] or 0
            #Age (in hours) of every question
            age_hours = max((now - q.created_at).total_seconds() / 3600.0, 1.0)

            #Scoring based on weight for each factor
            score = (q.answers_count * 4.0) + (answer_votes * 5.0)
            # time decay: divide by log(age + e) to give newer Q higher score than old, So old Q must have huge engagement to still trend 
            score = score / (math.log(age_hours + 2))

            scored.append((score, q))

        scored.sort(key=lambda x: x[0], reverse=True)

        result = [{"id": q.id, "title": q.title, "score": round(score, 3)} for score, q in scored[:limit] ]

        AnalyticsService._cache_set(key, result, ttl=60*15)  # 15 minutes

        return result

    '''
    @staticmethod
    def user_progress(user_id):
        key = f"{CACHE_PREFIX}user:progress:{user_id}"
        result = AnalyticsService._cache_get(key)
        if result is not None:
            return result

        # customize what you compute: number of plans, completed items, percentage
        total = StudyPlanItem.objects.filter(plan__user_id=user_id).count()
        completed = StudyPlanItem.objects.filter(plan__user_id=user_id, is_completed=True).count()
        pct = (completed / total * 100) if total else 0
        result = {"total_items": total, "completed": completed, "percentage": pct}
        AnalyticsService._cache_set(key, result, ttl=60*5)  # 5 minutes
        return result
    '''