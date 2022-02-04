from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


# from djangoratings.fields importimportimportimport RatingField


class User(AbstractUser):
    type = (
        ('EMPLOYEE', 'EMPLOYEE'),
        ('CUSTOMER', 'CUSTOMER'),
    )
    phone_no = models.CharField(unique=True, max_length=11)
    type = models.CharField(max_length=30, choices=type)
    img = models.ImageField(upload_to="media", blank=True)
    REQUIRED_FIELDS = ['phone_no', 'email']


class Category(models.Model):
    category = models.CharField(max_length=30)
    img = models.ImageField(upload_to="service")

    def __str__(self):
        return self.category


class Employee(models.Model):
    gender = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, related_name='customer_user', on_delete=models.CASCADE)
    photo = models.ImageField(max_length=30, blank=True)
    gender = models.CharField(max_length=30, choices=gender, blank=True)
    description = models.TextField(max_length=40, blank=True)
    address = models.CharField(max_length=40, blank=True)
    house_no = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    zip = models.IntegerField(blank=True, null=True)
    year_of_experience = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(null=True)

    def __str__(self):
        return str(self.user)


class EmployeeCategory(models.Model):
    employee = models.ForeignKey(Employee, related_name="employee_name", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="category_name", on_delete=models.CASCADE)
    price = models.CharField(max_length=30)

    def __str__(self):
        return str(self.category)


# class EmployeeService(models.Model):
#     user = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     service = models.ForeignKey(Employee_Category, on_delete=models.CASCADE)
#     price = models.CharField(max_length=30)
#
#     def __str__(self):
#         return str(self.user)


class BookingRequest(models.Model):
    FILTER_status = (
        ('CREATE', 'CREATE'),
        ('ACCEPT', 'ACCEPT'),
        ('REJECT', 'REJECT'),
        ('PENDING', 'PENDING'),
        ('COMPLETE', 'COMPLETE')

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name='employee_user', on_delete=models.CASCADE)
    # Img = models.ImageField(blank=True,upload_to="media",null=True)
    employee_category = models.ForeignKey(EmployeeCategory, related_name="emp_category", on_delete=models.CASCADE)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=50)
    comment = models.CharField(max_length=50)
    state = models.CharField(max_length=40)
    zip = models.IntegerField()
    house_no = models.CharField(max_length=60)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=50, choices=FILTER_status)

    def __str__(self):
        return str(self.user)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name='employee_user1', on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    rating = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5)])
    createDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.createDate)

