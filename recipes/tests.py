from django.contrib.auth.models import User
from .models import Recipe
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase


class RecipeListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_recipes(self):
        adam = User.objects.get(username='adam')
        Recipe.objects.create(owner=adam, title='a title')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_logged_in_user_can_create_recipes(self):
        self.client.force_authenticate(User.objects.get(username='adam'))
        response = self.client.post('/recipes/', {'title': 'a title', 'ingredients': 'Some ingredients', 'instructions': 'Some instructions'})
        count = Recipe.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_recipe(self):
        response = self.client.post('/recipes/', {'title': 'a title', 'ingredients': 'Some ingredients', 'instructions': 'Some instructions'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RecipeDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Recipe.objects.create(
            owner=adam, title='a title', ingredients='Some ingredients', instructions='Some instructions'
        )
        Recipe.objects.create(
            owner=brian, title='another title', ingredients='Some ingredients', instructions='Some instructions'
        )

    def test_can_retrieve_recipe_using_valid_id(self):
        response = self.client.get('/recipes/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_recipe_using_invalid_id(self):
        response = self.client.get('/recipes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_recipe(self):
        self.client.force_authenticate(User.objects.get(username='adam'))
        response = self.client.put('/recipes/1/', {'title': 'a better title', 'ingredients': 'Some ingredients', 'instructions': 'Some instructions'})
        recipe = Recipe.objects.filter(pk=1).first()
        self.assertEqual(recipe.title, 'a better title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_recipe(self):
        self.client.force_authenticate(User.objects.get(username='adam'))
        response = self.client.put('/recipes/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RecipeValidationTests(APITestCase):
    """Validate recipe data through the API."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="recipe_validator",
            password="TestPassword123!",
        )
        self.client.force_authenticate(self.user)

        self.valid_data = {
            "title": "Vegetable Pasta",
            "ingredients": "Pasta, tomatoes, garlic",
            "instructions": "Cook pasta and prepare sauce.",
            "cooking_time": 30,
            "difficulty_level": "Easy",
            "category": "Vegetarian",
        }

    def test_valid_recipe_can_be_created(self):
        response = self.client.post(
            "/recipes/",
            self.valid_data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data,
        )
        self.assertEqual(Recipe.objects.count(), 1)

    def test_negative_cooking_time_is_rejected(self):
        data = {**self.valid_data, "cooking_time": -20}

        response = self.client.post("/recipes/", data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("cooking_time", response.data)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_zero_cooking_time_is_rejected(self):
        data = {**self.valid_data, "cooking_time": 0}

        response = self.client.post("/recipes/", data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("cooking_time", response.data)

    def test_missing_cooking_time_is_allowed(self):
        data = {
            key: value
            for key, value in self.valid_data.items()
            if key != "cooking_time"
        }

        response = self.client.post("/recipes/", data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.data,
        )
        self.assertIsNone(response.data["cooking_time"])

    def test_whitespace_only_fields_are_rejected(self):
        for field in ("title", "ingredients", "instructions"):
            with self.subTest(field=field):
                data = {**self.valid_data, field: "   "}

                response = self.client.post(
                    "/recipes/",
                    data,
                )

                self.assertEqual(
                    response.status_code,
                    400,
                    response.data,
                )
                self.assertIn(field, response.data)

        self.assertEqual(Recipe.objects.count(), 0)

    def test_title_whitespace_is_trimmed(self):
        data = {
            **self.valid_data,
            "title": "  Vegetable Pasta  ",
        }

        response = self.client.post("/recipes/", data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Recipe.objects.get().title,
            "Vegetable Pasta",
        )

    def test_negative_cooking_time_cannot_be_updated(self):
        recipe = Recipe.objects.create(
            owner=self.user,
            title="Existing Recipe",
            ingredients="Some ingredients",
            instructions="Some instructions",
            cooking_time=30,
        )

        response = self.client.patch(
            f"/recipes/{recipe.pk}/",
            {"cooking_time": -10},
        )

        recipe.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertIn("cooking_time", response.data)
        self.assertEqual(recipe.cooking_time, 30)


class RecipeConstraintTests(TestCase):
    """Verify cooking-time validation and DB integrity."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="constraint_recipe_user",
            password="TestPassword123!",
        )

        self.recipe_data = {
            "owner": self.user,
            "title": "Test Recipe",
            "ingredients": "Tomatoes, garlic, pasta",
            "instructions": "Cook and combine.",
        }

    def test_positive_or_missing_cooking_time_is_valid(self):
        for cooking_time in (None, 1, 30):
            with self.subTest(cooking_time=cooking_time):
                recipe = Recipe(
                    **self.recipe_data,
                    cooking_time=cooking_time,
                )
                recipe.full_clean()
                recipe.save()

        self.assertEqual(Recipe.objects.count(), 3)

    def test_model_validation_rejects_invalid_time(self):
        for cooking_time in (0, -10):
            with self.subTest(cooking_time=cooking_time):
                recipe = Recipe(
                    **self.recipe_data,
                    cooking_time=cooking_time,
                )

                with self.assertRaises(ValidationError):
                    recipe.full_clean()

        self.assertEqual(Recipe.objects.count(), 0)

    def test_database_rejects_invalid_time(self):
        for cooking_time in (0, -10):
            with self.subTest(cooking_time=cooking_time):
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        Recipe.objects.create(
                            **self.recipe_data,
                            cooking_time=cooking_time,
                        )

        self.assertEqual(Recipe.objects.count(), 0)
