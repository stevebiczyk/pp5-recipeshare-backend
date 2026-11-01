from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe


class Vote(models.Model):
    CHOICES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )
    #     (1, '1 Star'),
    #     (2, '2 Stars'),
    #     (3, '3 Stars'),
    #     (4, '4 Stars'),
    #     (5, '5 Stars'),
    # )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='votes'
        )
    vote_type = models.CharField(choices=CHOICES, max_length=8, null=True)
    # rating = models.IntegerField(
    # choices=RATING_CHOICES, null=True, blank=True
    # )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'recipe']

    def __str__(self):
        return f'{self.owner} {self.recipe}'
