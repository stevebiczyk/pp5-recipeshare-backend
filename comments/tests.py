from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from comments.models import Comment
from recipes.models import Recipe


class CommentQueryTests(APITestCase):
    def test_comment_list_has_constant_query_count(self):
        owner = User.objects.create_user(username='comment-owner')
        recipe = Recipe.objects.create(
            owner=owner,
            title='Recipe',
            ingredients='Salt',
            instructions='Mix',
        )
        for number in range(8):
            Comment.objects.create(
                owner=owner,
                recipe=recipe,
                content=f'Comment {number}',
            )

        with self.assertNumQueries(3):
            response = self.client.get(f'/comments/?recipe={recipe.pk}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 8)
