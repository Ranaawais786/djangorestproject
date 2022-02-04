from rest_framework import permissions, status
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework import filters

from rest_framework.decorators import action
from rest_framework import status, viewsets
from django.contrib.auth import login
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from app.models import User, Category, BookingRequest, Employee, EmployeeCategory, Rating
from app.api.serializer import SignSiializer, Loginserialize, EmployeeSerializer, CategorySerializer, \
    EmployeeCtSerializer, BookingSerializer, UserBookingSerializer, RatingSerializer


# Token
#

class CreateUserViewMy(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = SignSiializer


class Login(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]
    serializer_class = Loginserialize
    throttle_classes = ()

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'detail of user': {'eamil': user.email, 'phone': user.phone_no, 'username': user.username}})


class EmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    #

    #     # obj=Token.objects.all()
    #     # return Employee.objects.filter(user_id__in=[token.user.id for token in obj])

    @action(methods=['get'], detail=True, url_path='review', url_name='review')
    def get_review(self, request, pk):
        name = Employee.objects.get(pk=pk)
        a = Rating.objects.filter(employee=name)
        serializer = RatingSerializer(a, many=True)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['service']


class BookingView(viewsets.ModelViewSet):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingSerializer
    filterset_fields = ['status']

    # def get_queryset(self):
    # if authenticate(user,)
    # if Booking_request.customer_user is not None:
    #     e = Booking_request.objects.filter(customer_user=self.request.user)
    # if Booking_request.employee_user is not None:
    #     e = Booking_request.objects.filter(employee_user=self.request.user)
    # return e


class EmployeeCtView(viewsets.ModelViewSet):
    queryset = EmployeeCategory.objects.all()
    serializer_class = EmployeeCtSerializer


class UserBookingView(viewsets.ModelViewSet):
    serializer_class = UserBookingSerializer
    filterset_fields = ['status']

    def get_queryset(self):
        if self.request.user.type == "EMPLOYEE":
            return BookingRequest.objects.filter(employee__user=self.request.user)
        if self.request.user.type == "CUSTOMER":
            return BookingRequest.objects.filter(user=self.request.user)


class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
