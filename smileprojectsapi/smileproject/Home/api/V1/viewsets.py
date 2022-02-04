from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg, Max, Min
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework.authtoken.models import Token
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
from Home.models import User, DailyQuote, Smile, Goal, Activity, Favourite, Community, Smilescience
from rest_framework import status, viewsets
from Home.api.V1.serializer import SignUpSerializer, Loginserialize, DailyQuoteSerializer, SmileSerializer, \
    GoalSerializer, ActivitySerializer, FavouriteSerializer, Smile_scienceSerializer, CommunitySerializer, \
 resourceSerializer


# Token
#

class CreateUserViewMy(CreateAPIView):
    model = User
    serializer_class = SignUpSerializer


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
                         'detail of user': {'eamil': user.email, 'username': user.username}})


class DailyQuoteview(viewsets.ModelViewSet):
    serializer_class = DailyQuoteSerializer

    def get_queryset(self):
        return DailyQuote.objects.filter(DATE=datetime.now())


class Smileview(viewsets.ModelViewSet):
    serializer_class = SmileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # obj=self.get_object()
        s = Smile.objects.filter(user=self.request.user)
        return s

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        days = self.request.query_params.get("days")
        today = datetime.now().date()
        p_date = today - timedelta(days=int(days))
        bestday = Smile.objects.values('DATE').annotate(Bestday=Sum('smileSecond')).order_by('-Bestday').first()
        query = Smile.objects.filter(DATE__gte=p_date, user=self.request.user).aggregate(smilesecond=Sum("smileSecond"),
                                                                                         smilecount=Count("user"),
                                                                                         maxsmile=Max("smileSecond"),
                                                                                         minsmile=Min("smileSecond"),
                                                                                         smilepercentage=Avg(
                                                                                             "smileSecond"))

        output = {
            'query': query,
            'best_day': bestday

        }
        return Response(output)


class GoalView(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        obj = Goal.objects.filter(user=self.request.user)

        return obj

    def list(self, request, smileSecond=None, *args, **kwargs):
        latest_streak = 0
        Max_streak = 0
        streaks = []
        today = datetime.now().date()
        Next_Date = today + timedelta(days=1)

        entry_dates = Smile.objects.values("DATE").filter(user=self.request.user, DATE__lte=today).order_by(
            "-DATE")

        for date in entry_dates:
            delta = Next_Date - date["DATE"]

            if delta.days == 1:  # Keep the streak going!
                latest_streak += 1
            if delta.days > 1:
                streaks.append(latest_streak)
                latest_streak = 1
            Next_Date = date["DATE"]
        streaks.append(latest_streak)
        latest_streak = streaks[0]
        streaks.sort()
        Max_streak = streaks[-1]
        queryset = self.get_queryset()
        a = Smile.objects.aggregate(s_second=Sum("smileSecond"))
        b = Smile.objects.aggregate(s_count=Count("user"))
        ss = a['s_second']
        sc = b['s_count']
        goal_second = Goal.objects.aggregate(g_count=Sum("smile_count"))
        goal_count = Goal.objects.aggregate(g_second=Sum('smile_second'))
        gs = goal_count['g_second']
        gc = goal_second['g_count']
        total_second = ss * 100 / gc
        total_count = sc * 100 / gs
        percentage = (total_count + total_second) / 2
        remaining_second = gc - ss
        remaining_count = gs - sc
        # d = timedelta(days=1)
        # td = datetime.now().date()
        # time = (td - d)
        s = Smile.objects.aggregate(Sum('smileSecond'))
        s1 = s['smileSecond__sum']

        # s1 = 15000

        list1 = [10, 30, 120, 300, 420, 600, 900, 1200, 1500, 1800, 2400, 3000, 3600, 4200, 4800, 5400, 6000, 6600,
                 7200, 7800, 8400, 9000, 9600, 10200]

        for count, value in enumerate(list1):

            if s1 == value or s1 < list1[count + 1]:
                return Response({"level": count + 1, 'percentage': percentage, 'remaining_second': remaining_second,
                                 'remaining_count': remaining_count, "latest_streak": latest_streak,
                                 "max_streak": Max_streak})
            i = 10200
            if s1 > i:
                smile = int((s1 - i) / 600)
                level = 24 + smile

                return Response({"level": level, 'percentage': percentage, 'remaining_second': remaining_second,
                                 'remaining_count': remaining_count, "latest_streak": latest_streak,
                                 "max_streak": Max_streak})


class AcitivityViewset(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]


class resourceViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = resourceSerializer
    permission_classes = [IsAuthenticated]


class FavouriteViewset(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        already_favorite = Favourite.objects.filter(activity=request.data.get("activity"), user=self.request.user)
        if already_favorite:
            already_favorite.delete()
            return Response({"status": 0}, status=status.HTTP_200_OK)
        self.perform_create(serializer)
        return Response({"status": 1}, status=status.HTTP_201_CREATED)


class CommnityViewset(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]


class SmilescienceViewset(viewsets.ModelViewSet):
    queryset = Smilescience.objects.all()
    serializer_class = Smile_scienceSerializer
    permission_classes = [IsAuthenticated]
#
#
# class ChangePasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = (IsAuthenticated,)
#
#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj
#
#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }
#
#             return Response(response)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
