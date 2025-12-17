
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .services.analytics import CACHE_PREFIX
from .models import Question, Answer

def invalidate_top_questions_cache():
    """
    Delete all cached top questions keys.
    """
    keys = cache.keys(f"{CACHE_PREFIX}top_questions:*")
    for key in keys:
        cache.delete(key)

def invalidate_trending_cache():
    """
    Delete all cached trending questions keys.
    """
    keys = cache.keys(f"{CACHE_PREFIX}trending:*")
    for key in keys:
        cache.delete(key)

def invalidate_skills_heatmap_cache():
    """
    Delete skills heatmap cache.
    """
    key = f"{CACHE_PREFIX}skills:heatmap"
    cache.delete(key)

def invalidate_user_progress_cache(user_id):
    """
    Delete cached user progress.
    """
    key = f"{CACHE_PREFIX}user:progress:{user_id}"
    cache.delete(key)


# Signal handlers

@receiver(post_save, sender=Question)
def question_post_save(sender, instance, created, **kwargs):
    """
    Invalidate analytics caches when a Question is created/updated.
    """
    if created:
        invalidate_top_questions_cache()
        invalidate_trending_cache()
        invalidate_skills_heatmap_cache() 


@receiver(post_save, sender=Answer)
def answer_post_save(sender, instance, created, **kwargs):
    """
    Invalidate analytics caches when an Answer is created.
    """
    if created:
        invalidate_top_questions_cache()   
        invalidate_trending_cache()      
        invalidate_user_progress_cache(instance.author_id)
