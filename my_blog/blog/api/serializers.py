from rest_framework.serializers import (ModelSerializer,
HyperlinkedIdentityField,SerializerMethodField,CharField,EmailField,ValidationError)
from blog.models import Post
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }

    def validate(self, data):
        email = data['email']
        username=data['username']
        user_qs = User.objects.filter(email=email)
        user_q = User.objects.filter(username=username)
        if user_qs.exists():
            raise ValidationError("This email id has already registered.")
        elif user_q.exists():
            raise ValidationError("This user has already registered.")
        else:
            return data
    #done only becasue password cannot pe stored raw otherwise CreateAPIView does this work
    #set password does the hashing work
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }



class PostListSerializer(ModelSerializer):
    detail=HyperlinkedIdentityField(view_name='api_blog:detail',lookup_field='slug')
    author=SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'detail',
            'author',
            'title',
            'body',
            ]
    def get_author(self, obj):
        return obj.author.username

class PostDetailSerializer(ModelSerializer):
    #if we change author to something else it will not work
    author=UserDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'body',
            'slug',
            'publish',
        ]

class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            #'id',
            'title',
            #'slug',
            'body',

        ]
