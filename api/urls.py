from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (
    RegisterApi,
    SubscriberApi,
    PutevoditelApi,
    PutevoditelImageApi,
    AimApi,
    ChangeAimApi,
    DreamApi,
    ChangeDreamApi,
    DreamToAimApi,
    UserAimApi,
    PostApi,
)

urlpatterns = [
    # auth
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterApi.as_view(), name="user_register"),
    # ==========================================================================================
    # user
    path(
        "user/<str:slug>/subscribers/", SubscriberApi.as_view(), name="list_subscribers"
    ),
    path("user/<str:slug>/aims/", UserAimApi.as_view(), name="list_user_aims"),
    path("user/form/", PutevoditelApi.as_view(), name="putevoditel_form"),
    path(
        "user/form/image/", PutevoditelImageApi.as_view(), name="putevoditel_image_form"
    ),
    # ==========================================================================================
    # goals
    path("goals/aim/", AimApi.as_view(), name="list_create_aim"),
    path("goals/aim/<int:id>", ChangeAimApi.as_view(), name="update_delete_aim"),
    path("goals/dream/", DreamApi.as_view(), name="list_create_dream"),
    path("goals/dream/<int:id>", ChangeDreamApi.as_view(), name="update_delete_dream"),
    path(
        "goals/dream/<int:id>/dream_to_aim",
        DreamToAimApi.as_view(),
        name="convert_dream_to_aim",
    ),
    # ==========================================================================================
    # posts
    path("posts/", PostApi.as_view(), name="list_create_post"),
]
