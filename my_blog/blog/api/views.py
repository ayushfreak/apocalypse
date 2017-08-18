from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from .serializers import (PostListSerializer,
    PostDetailSerializer,PostCreateSerializer,
    UserCreateSerializer,UserLoginSerializer,)
from blog.models import Post

from .permissions import IsOwnerOrReadOnly
from django.db.models import Q

from django.contrib.auth import get_user_model

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

User = get_user_model()



class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]



class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PostCreateAPIView(CreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostCreateSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(RetrieveAPIView,DestroyModelMixin, UpdateModelMixin):
    queryset=Post.objects.all()
    serializer_class=PostDetailSerializer
    lookup_field="slug"

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostListAPIView(ListAPIView):
    serializer_class=PostListSerializer
    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all() #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(Q(title__icontains=query)|
             Q(body__icontains=query)|Q(author__username__icontains=query)|
             Q(author__first_name__icontains=query)|
             Q(tags__name__icontains=query)).distinct()
        return queryset_list

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostListSerializer
    lookup_field="slug"
    permission_classes = [IsOwnerOrReadOnly,]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostListSerializer
    lookup_field="slug"
    permission_classes = [IsOwnerOrReadOnly,]
