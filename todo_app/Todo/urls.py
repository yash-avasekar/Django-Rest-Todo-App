from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TodoViewsets, UserViewsets, CreateUserViewset

# url ( endpoints ) goes here

router = DefaultRouter()
router.register("todos", TodoViewsets, basename="todos")
router.register("user", UserViewsets, basename="user")

urlpatterns = router.urls
urlpatterns += [
    path("create/user/", CreateUserViewset.as_view()),
]
