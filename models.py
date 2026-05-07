from django.db import models

# Create your models here.
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'


# Create your models here.
class EmployeeEmotionsModel(models.Model):
    user_name = models.CharField(max_length=100)
    login_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    emotion = models.CharField(max_length=100)
    count = models.IntegerField()
    c_date = models.DateTimeField()

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'EmployeeEmotions'

