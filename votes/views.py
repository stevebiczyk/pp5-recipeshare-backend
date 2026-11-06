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
    serializer = VoteSerializer(
        data={'recipe': request.data.get('recipe'), 'vote_type': 'downvote'},
        context={'request': request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
