from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from comments.models import Comment
from followers.models import Follower
from profiles.models import Profile
from recipes.models import Recipe
from votes.models import Vote


class ApiRegressionTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user('author', password='StrongPassword123!')
        self.reader = User.objects.create_user('reader', password='StrongPassword123!')
        self.recipe = Recipe.objects.create(owner=self.author, title='Recipe', ingredients='Salt', instructions='Mix')
        self.client.force_authenticate(self.reader)

    def test_vote_switch_remove_and_net_score(self):
        for vote_type, score in [('downvote', -1), ('upvote', 1), ('upvote', 1), ('downvote', -1)]:
            response = self.client.post('/votes/', {'recipe': self.recipe.pk, 'vote_type': vote_type})
            self.assertEqual(response.status_code, 201, response.data)
            self.assertEqual(Vote.objects.count(), 1)
            data = self.client.get(f'/recipes/{self.recipe.pk}/').data
            self.assertEqual(data['votes_count'], score)
            self.assertEqual(data['vote_type'], vote_type)
        self.client.delete(f'/votes/{data["vote_id"]}/')
        self.assertEqual(self.client.get(f'/recipes/{self.recipe.pk}/').data['votes_count'], 0)

    def test_counts_are_not_multiplied_by_comments(self):
        Vote.objects.create(owner=self.reader, recipe=self.recipe, vote_type='downvote')
        third = User.objects.create_user('third')
        Vote.objects.create(owner=third, recipe=self.recipe, vote_type='upvote')
        for _ in range(3):
            Comment.objects.create(owner=self.reader, recipe=self.recipe, content='Comment')
        data = self.client.get(f'/recipes/{self.recipe.pk}/').data
        self.assertEqual((data['votes_count'], data['upvotes_count'], data['downvotes_count'], data['comments_count']), (0, 1, 1, 3))
        voted = self.client.get(f'/recipes/?votes__owner__profile={self.reader.profile.pk}&ordering=-current_vote_created_at').data
        self.assertEqual(voted['count'], 1)
        self.assertEqual(voted['results'][0]['upvotes_count'], 1)
        self.assertEqual(voted['results'][0]['downvotes_count'], 1)

    def test_invalid_votes_are_validation_errors(self):
        for path in ['/votes/', '/votes/downvote/']:
            for recipe_id in ['not-a-number', 999999, None]:
                with self.subTest(path=path, recipe_id=recipe_id):
                    response = self.client.post(path, {'recipe': recipe_id}, format='json')
                    self.assertEqual(response.status_code, 400, response.data)

    def test_self_votes_are_rejected_on_all_write_paths(self):
        self.client.force_authenticate(self.author)
        for path in ['/votes/', '/votes/downvote/']:
            response = self.client.post(path, {'recipe': self.recipe.pk, 'vote_type': 'upvote'})
            self.assertEqual(response.status_code, 400)
        existing = Vote.objects.create(owner=self.author, recipe=self.recipe, vote_type='upvote')
        self.assertEqual(self.client.patch(f'/votes/{existing.pk}/', {'vote_type': 'downvote'}).status_code, 400)

    def test_vote_cannot_be_moved_or_changed_by_another_user(self):
        vote = Vote.objects.create(owner=self.reader, recipe=self.recipe, vote_type='upvote')
        own_recipe = Recipe.objects.create(owner=self.reader, title='Own', ingredients='x', instructions='y')
        response = self.client.patch(f'/votes/{vote.pk}/', {'recipe': own_recipe.pk})
        self.assertEqual(response.status_code, 400)
        self.client.force_authenticate(self.author)
        self.assertEqual(self.client.delete(f'/votes/{vote.pk}/').status_code, 403)

    def test_follow_uses_explicit_user_id_with_divergent_profile_id(self):
        self.author.profile.delete()
        profile = Profile.objects.create(pk=100, owner=self.author)
        data = self.client.get(f'/profiles/{profile.pk}/').data
        self.assertEqual(data['owner_id'], self.author.pk)
        self.assertNotEqual(data['id'], data['owner_id'])
        response = self.client.post('/followers/', {'followed': data['owner_id']})
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Follower.objects.get().followed_id, self.author.pk)

    def test_recipe_list_uses_constant_query_count(self):
        for number in range(8):
            Recipe.objects.create(owner=self.author, title=str(number), ingredients='x', instructions='y')
        with self.assertNumQueries(2):
            response = self.client.get('/recipes/')
            self.assertEqual(len(response.data['results']), 9)

    def test_anonymous_vote_ordering_does_not_fail(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/recipes/?ordering=-current_vote_created_at')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['results'][0]['vote_id'])

    def test_comment_profile_and_follow_ownership(self):
        comment = Comment.objects.create(owner=self.author, recipe=self.recipe, content='Original')
        following = Follower.objects.create(owner=self.author, followed=self.reader)
        for path, data in [(f'/comments/{comment.pk}/', {'content': 'Changed'}), (f'/profiles/{self.author.profile.pk}/', {'bio': 'Changed'})]:
            self.assertEqual(self.client.patch(path, data).status_code, 403)
        self.assertEqual(self.client.delete(f'/followers/{following.pk}/').status_code, 403)


class CsrfIntegrationTests(APITestCase):
    def setUp(self):
        User.objects.create_user('browser', password='StrongPassword123!')
        self.client = APIClient(enforce_csrf_checks=True)
        self.client.post('/dj-rest-auth/login/', {'username': 'browser', 'password': 'StrongPassword123!'})
        self.payload = {'title': 'Recipe', 'ingredients': 'Salt', 'instructions': 'Mix'}

    def test_fresh_session_requires_bootstrap_then_accepts_masked_token(self):
        self.assertEqual(self.client.post('/recipes/', self.payload).status_code, 403)
        response = self.client.get('/csrf/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('no-store', response['Cache-Control'])
        token = response.json()['csrfToken']
        response = self.client.post('/recipes/', self.payload, HTTP_X_CSRFTOKEN=token, HTTP_ORIGIN='http://localhost:3000')
        self.assertEqual(response.status_code, 201, response.data)

    def test_untrusted_origin_is_rejected(self):
        token = self.client.get('/csrf/').json()['csrfToken']
        response = self.client.post('/recipes/', self.payload, HTTP_X_CSRFTOKEN=token, HTTP_ORIGIN='https://untrusted.example')
        self.assertEqual(response.status_code, 403)

    def test_registration_then_login_and_logout_with_csrf(self):
        self.client.cookies.clear()
        token = self.client.get('/csrf/').json()['csrfToken']
        response = self.client.post('/dj-rest-auth/registration/', {'username': 'new_reader', 'password1': 'StrongPassword456!', 'password2': 'StrongPassword456!'}, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201, response.data)
        response = self.client.post('/dj-rest-auth/login/', {'username': 'new_reader', 'password': 'StrongPassword456!'}, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(self.client.get('/dj-rest-auth/user/').status_code, 200)
        token = self.client.get('/csrf/').json()['csrfToken']
        response = self.client.post('/dj-rest-auth/logout/', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/dj-rest-auth/user/').status_code, 401)
