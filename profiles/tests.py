from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from followers.models import Follower


class ProfileQueryTests(APITestCase):
    def test_profile_list_has_constant_query_count(self):
        reader = User.objects.create_user(username='reader')
        followed = User.objects.create_user(username='followed')
        for number in range(8):
            User.objects.create_user(username=f'user-{number}')
        following = Follower.objects.create(owner=reader, followed=followed)
        self.client.force_authenticate(reader)

        with self.assertNumQueries(2):
            response = self.client.get('/profiles/')

        self.assertEqual(response.status_code, 200)
        followed_profile = next(
            item for item in response.data['results']
            if item['owner'] == followed.username
        )
        self.assertEqual(followed_profile['following_id'], following.pk)
