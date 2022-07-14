from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import generics, mixins, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goals.models import Aim, Dream, Post
from user.models import User, Subscriber, DreamAssociation
from .serializer import (
    RegisterSerializer,
    UserSerializer,
    RetrieveUserSerializer,
    SubscriberSerializer,
    PutevoditelSerializer,
    DreamAssociationSerializer,
    AimSerializer,
    DreamSerializer,
    DreamToAimSerializer,
    PostSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class RegisterApi(generics.GenericAPIView, mixins.CreateModelMixin):
    """Creates a new user with login and password."""

    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        return serializer.save()

    @swagger_auto_schema(responses={201: UserSerializer()})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(UserSerializer(instance).data, status=status.HTTP_201_CREATED)


class SubscriberApi(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    """Returns list of all subscribed users and subscribes to the user with slug."""

    lookup_field = "slug"
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in ["GET", "DELETE"]:
            return RetrieveUserSerializer
        return SubscriberSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user, slug=self.kwargs["slug"])

    @permission_classes([IsAuthenticated])
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @swagger_auto_schema(
        request_body=no_body, responses={201: RetrieveUserSerializer()}
    )
    def post(self, request, *args, **kwargs):
        instance = self.perform_create(SubscriberSerializer())
        return Response(RetrieveUserSerializer(instance).data, status.HTTP_201_CREATED)

    def perform_destroy(self):
        Subscriber.objects.filter(
            user=self.request.user, author__slug=self.kwargs["slug"]
        ).delete()

    @permission_classes([IsAuthenticated])
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @swagger_auto_schema(request_body=no_body)
    def delete(self, request, *args, **kwargs):
        self.perform_destroy()
        return Response(status=status.HTTP_200_OK)


class PutevoditelApi(
    generics.GenericAPIView, mixins.UpdateModelMixin, mixins.RetrieveModelMixin
):
    """Updates user info provided from form"""

    serializer_class = PutevoditelSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated")
        return self.request.user

    @permission_classes([IsAuthenticated])
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return Response(
            PutevoditelSerializer(self.request.user).data, status=status.HTTP_200_OK
        )

    @permission_classes([IsAuthenticated])
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(
            PutevoditelSerializer(self.request.user).data, status=status.HTTP_200_OK
        )


class PutevoditelImageApi(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = DreamAssociationSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        DreamAssociation.objects.create(
            user=self.request.user, image=request.data["image"]
        )
        return Response(status=status.HTTP_201_CREATED)


class AimApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Lists user's aims and creates new"""

    serializer_class = AimSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Aim.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ChangeAimApi(
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):
    """Updates and deletes user's aim by id"""

    serializer_class = AimSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "id"

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated")
        aim = get_object_or_404(Aim, id=self.kwargs["id"])
        if aim.user != self.request.user:
            raise PermissionDenied("You can't change aim of other user")
        return aim

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return Response(
            AimSerializer(self.request.user).data, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(
            AimSerializer(self.get_object()).data, status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DreamApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Lists user's dreams and creates new"""

    pagination_class = StandardResultsSetPagination
    serializer_class = DreamSerializer

    def get_queryset(self):
        return Dream.objects.filter(user=self.request.user)

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ChangeDreamApi(
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):
    """Updates and deletes user's dreams by id"""

    serializer_class = DreamSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "id"

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated")
        dream = get_object_or_404(Dream, id=self.kwargs["id"])
        if dream.user != self.request.user:
            raise PermissionDenied("You can't change aim of other user")
        return dream

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return Response(
            DreamSerializer(self.request.user).data, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(
            DreamSerializer(self.get_object()).data, status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DreamToAimApi(APIView):
    @swagger_auto_schema(
        request_body=DreamToAimSerializer(), responses={201: AimSerializer()}
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated")
        dream = get_object_or_404(Dream, id=self.kwargs["id"])
        if dream.user != request.user:
            raise PermissionDenied("You can't change aim of other user")
        serializer = DreamToAimSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aim = dream.dream_to_aim(serializer.data["deadline"])
        return Response(AimSerializer(aim).data, status=status.HTTP_201_CREATED)


class UserAimApi(generics.GenericAPIView, mixins.ListModelMixin):
    """Lists user's aims"""

    serializer_class = AimSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Aim.objects.filter(user__slug=self.kwargs["slug"])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Lists inspirer's posts and creates new"""

    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Post.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.groups.filter(name="inspirer").exists()
        ):
            return self.create(request, *args, **kwargs)
        raise PermissionDenied("You can't create post")
