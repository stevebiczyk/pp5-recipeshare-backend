from django.db.models import Count, DateTimeField, F, OuterRef, Q, Subquery, Value

from .models import Recipe
from votes.models import Vote


def recipe_queryset(user=None):
    queryset = Recipe.objects.select_related('owner__profile').annotate(
        upvotes_count=Count('votes', filter=Q(votes__vote_type='upvote') | Q(votes__vote_type__isnull=True), distinct=True),
        downvotes_count=Count('votes', filter=Q(votes__vote_type='downvote'), distinct=True),
        comments_count=Count('comment', distinct=True),
    ).annotate(votes_count=F('upvotes_count') - F('downvotes_count'))
    if user is not None and user.is_authenticated:
        vote = Vote.objects.filter(owner=user, recipe_id=OuterRef('pk'))
        queryset = queryset.annotate(
            current_vote_id=Subquery(vote.values('id')[:1]),
            current_vote_type=Subquery(vote.values('vote_type')[:1]),
            current_vote_created_at=Subquery(vote.values('created_at')[:1]),
        )
    else:
        queryset = queryset.annotate(
            current_vote_created_at=Value(None, output_field=DateTimeField()),
        )
    return queryset.order_by('-created_at')
