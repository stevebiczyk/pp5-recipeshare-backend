from django.db.models import Count, IntegerField, OuterRef, Subquery, Value
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from followers.models import Follower
from pp5_backend_sb.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


def profile_queryset(user):
    queryset = Profile.objects.select_related('owner').annotate(
        recipes_count=Count('owner__recipe', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    )
    if user.is_authenticated:
        following = Follower.objects.filter(
            owner=user,
            followed_id=OuterRef('owner_id'),
        )
        queryset = queryset.annotate(
            current_following_id=Subquery(following.values('id')[:1]),
        )
    else:
        queryset = queryset.annotate(
            current_following_id=Value(None, output_field=IntegerField()),
        )
    return queryset.order_by('-created_at')


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'recipes_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

    def get_queryset(self):
        return profile_queryset(self.request.user)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return profile_queryset(self.request.user)
