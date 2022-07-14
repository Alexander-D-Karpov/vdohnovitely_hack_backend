from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from goals.models import Aim, Dream, Post
from user.models import User, Subscriber, DreamAssociation


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "slug")


class PublicUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class PublicSubscriberInfoSerializer(serializers.ModelSerializer):
    user = PublicUserInfoSerializer()

    class Meta:
        model = Subscriber
        fields = ("user",)


class RetrieveUserSerializer(serializers.ModelSerializer):
    subscribers = PublicSubscriberInfoSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "email", "subscriber_count", "subscribers")


class SubscriberSerializer(serializers.ModelSerializer):
    author = PublicUserInfoSerializer()

    class Meta:
        model = Subscriber
        fields = ("author",)
        extra_kwargs = {"author": {"read_only": True, "required": False}}

    def save(self, user, slug):
        if user.is_authenticated:
            author = User.objects.get(slug=slug)
            if not author.groups.filter(name="inspirer").exists():
                raise serializers.ValidationError(
                    "You are not allowed to subscribe to this user"
                )

            Subscriber.objects.get_or_create(
                author=author,
                user=user,
            )
            return author
        raise AuthenticationFailed("User is not authenticated")


class PutevoditelSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.ImageField())

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "telephone",
            "communication",
            "idea_generation",
            "organisation",
            "creativity",
            "resource_search",
            "achievement",
            "critical_thinking",
            "leadership",
            "want_to_find_out",
            "want_to_learn",
            "want_to_get",
            "images",
            "introvert",
            "individualist",
            "optimist",
            "serious",
            "organized",
            "leader",
            "who_am_i_extra_1",
            "who_am_i_extra_2",
            "who_am_i_extra_3",
            "who_am_i_extra_4",
            "who_am_i_extra_5",
            "what_i_want_1",
            "what_i_want_2",
            "what_i_want_3",
            "what_i_want_4",
            "what_i_want_5",
            "what_i_want_6",
            "what_i_want_7",
            "what_i_want_8",
            "what_i_want_9",
            "what_i_want_10",
        )
        extra_kwargs = {
            "images": {"read_only": True},
        }


class DreamAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DreamAssociation
        fields = ("image",)


class AimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aim
        fields = ("id", "name", "description", "created_at", "deadline")
        extra_kwargs = {
            "created_at": {"read_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        aim = Aim.objects.create(user=user, **validated_data)
        return aim


class DreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dream
        fields = ("id", "name", "description", "created_at")
        extra_kwargs = {
            "created_at": {"read_only": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        dream = Dream.objects.create(user=user, **validated_data)
        return dream


class DreamToAimSerializer(serializers.Serializer):
    deadline = serializers.DateTimeField(required=True)


class PostSerializer(serializers.ModelSerializer):
    creator = PublicUserInfoSerializer()

    class Meta:
        model = Post
        fields = ("id", "name", "creator", "video", "description", "created_at")
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }
