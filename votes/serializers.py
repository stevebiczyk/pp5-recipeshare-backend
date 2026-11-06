from rest_framework import serializers
from votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vote model
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    vote_type = serializers.ChoiceField(choices=Vote.CHOICES, default='upvote')

    class Meta:
        model = Vote
        fields = ['id', 'recipe', 'created_at', 'owner', 'vote_type']

    def validate(self, attrs):
        recipe = attrs.get('recipe', self.instance.recipe if self.instance else None)
        if self.instance and recipe != self.instance.recipe:
            raise serializers.ValidationError({'recipe': 'A vote cannot be moved to another recipe.'})
        if recipe and recipe.owner_id == self.context['request'].user.pk:
            raise serializers.ValidationError({'recipe': 'You cannot vote on your own recipe.'})
        return attrs

    def create(self, validated_data):
        vote, _ = Vote.objects.update_or_create(
            owner=validated_data['owner'], recipe=validated_data['recipe'],
            defaults={'vote_type': validated_data.get('vote_type', 'upvote')},
        )
        return vote
