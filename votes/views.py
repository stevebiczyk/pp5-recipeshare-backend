from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from pp5_backend_sb.permissions import IsOwnerOrReadOnly
from votes.models import Vote
from votes.serializers import VoteSerializer


class VoteList(generics.ListCreateAPIView):
    """
    List votes or create a vote if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a vote or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def downvote_view(request):
    recipe_id = request.data.get('recipe')
    if not recipe_id:
        return Response({'detail': 'recipe id required'}, status=status.HTTP_400_BAD_REQUEST)
    vote, created = Vote.objects.get_or_create(
        owner=request.user,
        recipe_id=recipe_id,
        defaults={'vote_type': 'downvote'}
    )
    if not created:
        vote.vote_type = 'downvote'
        vote.save()
    serializer = VoteSerializer(vote, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
