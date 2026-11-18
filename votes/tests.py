from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from recipes.models import Recipe
from votes.models import Vote

User = get_user_model()

class VoteAPITests(APITestCase):
    """Regression tests for the Vote API endpoints."""
    
    def setUp(self):
        # Create three users and two recipes.
        self.author = User.objects.create_user(
            username="author",
            password="TestPassword123!",
        )
        self.voter = User.objects.create_user(
            username="voter",
            password="TestPassword123!",
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            password="TestPassword123!",
        )

        self.recipe = Recipe.objects.create(
            owner=self.author,
            title="Test Pasta",
            ingredients="Pasta, tomatoes, olive oil",
            instructions="Cook pasta and prepare sauce.",
        )
        self.other_recipe = Recipe.objects.create(
            owner=self.author,
            title="Test Soup",
            ingredients="Carrots, onions, stock",
            instructions="Cook vegetables in stock.",
        )

        self.votes_url = "/votes/"
        self.recipe_url = f"/recipes/{self.recipe.pk}/"

    def authenticate(self, user=None):
        """Authenticate a user without using the login endpoint."""
        self.client.force_authenticate(
            user=user or self.voter
        )

    def create_vote(self, user=None, vote_type="upvote"):
        """Create a vote directly for test setup."""
        return Vote.objects.create(
            owner=user or self.voter,
            recipe=self.recipe,
            vote_type=vote_type,
        )

    def test_anonymous_user_cannot_vote(self):
        response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "upvote",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Vote.objects.count(), 0)

    def test_authenticated_user_can_upvote(self):
        self.authenticate()

        response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "upvote",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Vote.objects.count(), 1)

        vote = Vote.objects.get()
        self.assertEqual(vote.owner, self.voter)
        self.assertEqual(vote.recipe, self.recipe)
        self.assertEqual(vote.vote_type, "upvote")

    def test_authenticated_user_can_downvote(self):
        self.authenticate()

        response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "downvote",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Vote.objects.get().vote_type,
            "downvote",
        )

    def test_invalid_vote_type_is_rejected(self):
        self.authenticate()

        response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "neutral",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Vote.objects.count(), 0)

    def test_legacy_downvote_endpoint_updates_vote(self):
        self.authenticate()
        vote = self.create_vote(vote_type="upvote")

        response = self.client.post(
            "/votes/downvote/",
            {"recipe": self.recipe.pk},
        )

        vote.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(vote.vote_type, "downvote")
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(response.data["id"], vote.pk)

    def test_vote_defaults_to_upvote(self):
        self.authenticate()

        response = self.client.post(
            self.votes_url,
            {"recipe": self.recipe.pk},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Vote.objects.get().vote_type,
            "upvote",
        )

    def test_user_cannot_vote_on_own_recipe(self):
        self.authenticate(self.author)

        response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "upvote",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(Vote.objects.count(), 0)

    def test_repeated_vote_does_not_create_duplicate(self):
        self.authenticate()

        first_response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "upvote",
            },
        )

        second_response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "upvote",
            },
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(
            first_response.data["id"],
            second_response.data["id"],
        )

    def test_user_can_change_upvote_to_downvote(self):
        self.authenticate()
        vote = self.create_vote()

        response = self.client.post(
            self.votes_url,
            {
                "recipe": self.recipe.pk,
                "vote_type": "downvote",
            },
        )

        vote.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(vote.vote_type, "downvote")
        self.assertEqual(response.data["id"], vote.pk)

    def test_user_can_remove_own_vote(self):
        self.authenticate()
        vote = self.create_vote()

        response = self.client.delete(
            f"/votes/{vote.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Vote.objects.filter(pk=vote.pk).exists()
        )

    def test_user_cannot_delete_another_users_vote(self):
        vote = self.create_vote(user=self.other_user)
        self.authenticate()

        response = self.client.delete(
            f"/votes/{vote.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Vote.objects.filter(pk=vote.pk).exists()
        )

    def test_user_cannot_modify_another_users_vote(self):
        vote = self.create_vote(user=self.other_user)
        self.authenticate()

        response = self.client.patch(
            f"/votes/{vote.pk}/",
            {"vote_type": "downvote"},
        )

        vote.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(vote.vote_type, "upvote")

    def test_user_cannot_move_vote_to_another_recipe(self):
        self.authenticate()
        vote = self.create_vote()

        response = self.client.patch(
            f"/votes/{vote.pk}/",
            {"recipe": self.other_recipe.pk},
        )

        vote.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(vote.recipe_id, self.recipe.pk)

    def test_recipe_vote_counts_and_net_score(self):
        # Two upvotes and one downvote give a net score of +1.
        self.create_vote(user=self.voter, vote_type="upvote")
        self.create_vote(user=self.other_user, vote_type="upvote")

        fourth_user = User.objects.create_user(
            username="fourth_user",
            password="TestPassword123!",
        )
        Vote.objects.create(
            owner=fourth_user,
            recipe=self.recipe,
            vote_type="downvote",
        )

        response = self.client.get(self.recipe_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["upvotes_count"], 2)
        self.assertEqual(response.data["downvotes_count"], 1)
        self.assertEqual(response.data["votes_count"], 1)


class VoteConstraintTests(TestCase):
    """Verify vote integrity at the database level."""

    def setUp(self):
        self.author = User.objects.create_user(
            username="constraint_author",
            password="TestPassword123!",
        )
        self.voter = User.objects.create_user(
            username="constraint_voter",
            password="TestPassword123!",
        )
        self.recipe = Recipe.objects.create(
            owner=self.author,
            title="Constraint Test Recipe",
            ingredients="Test ingredients",
            instructions="Test instructions",
        )

    def test_duplicate_vote_is_rejected(self):
        Vote.objects.create(
            owner=self.voter,
            recipe=self.recipe,
            vote_type="upvote",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(
                    owner=self.voter,
                    recipe=self.recipe,
                    vote_type="downvote",
                )

        self.assertEqual(Vote.objects.count(), 1)

    def test_null_vote_type_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(
                    owner=self.voter,
                    recipe=self.recipe,
                    vote_type=None,
                )

        self.assertEqual(Vote.objects.count(), 0)

    def test_invalid_vote_type_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Vote.objects.create(
                    owner=self.voter,
                    recipe=self.recipe,
                    vote_type="invalid",
                )

        self.assertEqual(Vote.objects.count(), 0)
