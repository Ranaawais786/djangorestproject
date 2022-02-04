from abc import ABC

from django.contrib.auth import authenticate

from Home.models import User, DailyQuote, Smile, Goal, Activity, Favourite, Community, Smilescience, Resource
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db.models import Sum
from allauth.utils import email_address_exists, generate_unique_username


#
# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password', 'GENDER', 'AGE', 'RELATIONSHIP', 'CHILDREN', 'GOAL')
#         extra_kwargs = {'password': {'write_only': True}
#                         }
#
#     def create(self, validated_data):
#         user = User(
#
#             email=validated_data.get('email'),
#             username=generate_unique_username([
#                 validated_data.get('email'),
#                 'user'
#
#             ]))
#         user.set_password(validated_data.get('password'))
#         user.save()
#         return user
#
#
# class Loginserialize(serializers.Serializer):
#     username = serializers.CharField(
#         label=("Username"),
#         write_only=True
#     )
#     password = serializers.CharField(
#         label=("Password"),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )
#
#     # token = serializers.CharField(
#     #     label=_("Token"),
#     #     read_only=True
#     # )
#
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#
#         if username and password:
#             obj = User.objects.filter(email=username).first()
#             if obj:
#                 user = authenticate(request=self.context.get('request'),
#                                     username=obj.username, password=password)
#             else:
#                 user = authenticate(request=self.context.get('request'),
#                                     username=username, password=password)
#
#             if not user:
#                 msg = 'EMAIL AND PASSWORD IS INVALID.'
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = 'Must include "username" and "password".'
#             raise serializers.ValidationError(msg, code='authorization')
#
#         attrs['user'] = user
#         return attrs
#
#
# class DailyQuoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DailyQuote
#         fields = "__all__"
#
#
# class SmileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Smile
#         fields = ""
#
#
# class GoalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Goal
#         fields = ""
#
#
# class ActivitySerializer(serializers.ModelSerializer):
#     is_favorite = serializers.BooleanField(source="", read_only=True)
#
#     class Meta:
#         model = Activity
#         fields = "__all__"
#
#
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from Home.models import User, DailyQuote, Smile, Goal, Activity, Favourite
# from django.utils.translation import gettext_lazy as _
# from rest_framework import serializers
# from django.db.models import Sum
# from allauth.utils import email_address_exists, generate_unique_username


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'GENDER', 'AGE', 'RELATIONSHIP', 'CHILDREN', 'GOAL')
        extra_kwargs = {'password': {'write_only': True}
                        }

    def create(self, validated_data):
        user = User(

            email=validated_data.get('email'),
            username=generate_unique_username([
                validated_data.get('email'),
                'user'

            ]))
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class Loginserialize(serializers.Serializer):
    username = serializers.CharField(
        label=("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    # token = serializers.CharField(
    #     label=_("Token"),
    #     read_only=True
    # )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            obj = User.objects.filter(email=username).first()
            if obj:
                user = authenticate(request=self.context.get('request'),
                                    username=obj.username, password=password)
            else:
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)

            if not user:
                msg = 'EMAIL AND PASSWORD IS INVALID.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class DailyQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyQuote
        fields = "__all__"


class SmileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smile
        fields = ""


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ""


class ActivitySerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField('get_favourite')

    class Meta:
        model = Activity
        fields = "__all__"

    def get_favourite(self, obj):
        f = Favourite.objects.filter(user=self.context["request"].user, activity=obj)
        if f:
            return True
        else:
            return False
        # return Favourite.objects.filter(user=self.context["request"].user, activity=obj)


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"


class Smile_scienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smilescience
        fields = "__all__"


class resourceSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField('get_level')

    class Meta:
        model = Resource
        fields = "__all__"

