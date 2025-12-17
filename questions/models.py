from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Question(models.Model):
    CATEGORY_CHOICES = (
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('system_design', 'System Design'),
    )

    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='questions')

    skills_required = models.ManyToManyField(Skill, related_name="questions")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['difficulty']),
        ]

    def __str__(self):
        return self.title


class Answer(models.Model):
    
    question = models.ForeignKey( Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    votes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-votes', '-created_at']
        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"
