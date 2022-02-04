from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from allauth.utils import email_address_exists, generate_unique_username
from django.http import request
from rest_framework.response import Response
from app.models import User, Category, BookingRequest, EmployeeCategory, Employee, Rating
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db.models import Avg


class SignSiializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_no', 'img', 'type', 'password')
        extra_kwargs = {'password': {'write_only': True}
                        }

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            phone_no=validated_data.get('phone_no'),
            type=validated_data.get('type'),
            img=validated_data.get('img'),
            # name=validated_data.get('name'),
            username=generate_unique_username([
                # validated_data.get('name'),
                validated_data.get('email'),

                'user'

            ])
        )

        user.set_password(validated_data.get('password'))
        user.save()
        if user.type == "EMPLOYEE":
            d = Employee(name=user.username, user=user, photo=user.img)
            d.save()
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
            obj = User.objects.filter(phone_no=username).first()
            if obj:
                user = authenticate(request=self.context.get('request'),
                                    username=obj.username, password=password)
            else:
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)
        if username and password:
            obj1 = User.objects.filter(email=username).first()
            if obj1:
                user = authenticate(request=self.context.get('request'),
                                    username=obj1.username, password=password)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = {'Unable to log in with provided credentials.'}
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EmployeeCtSerializer(serializers.ModelSerializer):
    # s = serializers.CharField(source="service.service", read_only=True)

    class Meta:
        model = EmployeeCategory
        fields = ('id', 'employee', 'category', 'price')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category', 'img')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequest
        fields = ('user', 'employee', 'employee_category', 'address', 'city', 'comment', 'state', 'zip', 'house_no',
                  'booking_date', 'booking_time', 'status')


class EmployeeSerializer(serializers.ModelSerializer):
    # average=serializers.IntegerField(source="",read_only=True)'

    Average = serializers.SerializerMethodField('get_average')

    class Meta:
        model = Employee

        fields = (
            'user', 'name', 'photo', 'gender', 'Average', 'description', 'address', 'state', 'zip', 'house_no', 'city',
            'year_of_experience', 'is_active')

    def get_average(self, obj):
        a = Rating.objects.filter(employee=obj).aggregate(Avg('rating'))
        return round(a["rating__avg"], 2)


class UserBookingSerializer(serializers.ModelSerializer):
    employee_category = serializers.StringRelatedField()
    customer_image = serializers.ImageField(source="user.img", read_only=True)
    employee_image = serializers.ImageField(source="employee.photo", read_only=True)

    # client_owner = serializers.StringRelatedField()
    class Meta:
        model = BookingRequest
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating

        fields = "__all__"
