from django.db import IntegrityError
from rest_framework import serializers
from votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Vote
        fields = ['id', 'recipe', 'created_at', 'owner', 'vote_type']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            owner = request.user
            recipe = validated_data.get('recipe')
            vote_type = validated_data.get('vote_type') or 'upvote'

            vote, created = Vote.objects.get_or_create(
                owner=owner,
                recipe=recipe,
                defaults={'vote_type': vote_type}
            )
            if not created:
                if vote.vote_type != vote_type:
                    vote.vote_type = vote_type
                    vote.save()
                    return vote
                raise serializers.ValidationError({'detail': 'possible duplicate'})
            return vote

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})
