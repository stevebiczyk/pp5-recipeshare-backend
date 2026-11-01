from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from pp5_backend_sb.permissions import IsOwnerOrReadOnly
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeList(generics.ListCreateAPIView):
    """
    List recipes or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.annotate(
        votes_count=Count('votes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'votes__owner__profile',
        'owner__profile',
        'category',
        'difficulty_level',
    ]
    search_fields = [
        'owner__username',
        'title',
        'difficulty_level',
        'category',
        'ingredients',
    ]
    ordering_fields = [
        'votes_count',
        'comments_count',
        'votes__created_at',
        'cooking_time',
        'created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a recipe and edit or delete it if you own it.
    """
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.annotate(
        votes_count=Count('votes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
