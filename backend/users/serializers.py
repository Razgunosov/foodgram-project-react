from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField

from users.models import CustomUser, Subscribe


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            CustomUser.USERNAME_FIELD,
            'password',
        )


class UserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        query = Subscribe.objects.filter(author=author, user=user).exists()
        return query