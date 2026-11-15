
from django.conf import settings
from django.db import models

from recipes.models import Recipe


class Vote(models.Model):
    CHOICES = (
        ("upvote", "Upvote"),
        ("downvote", "Downvote"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    vote_type = models.CharField(
        max_length=8,
        choices=CHOICES,
        default="upvote",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "recipe"],
                name="unique_vote_per_user_recipe",
            ),
            models.CheckConstraint(
                check=models.Q(
                    vote_type__in=["upvote", "downvote"]
                ),
                name="valid_recipe_vote_type",
            ),
        ]

    def __str__(self):
        return f"{self.owner} {self.recipe}"
