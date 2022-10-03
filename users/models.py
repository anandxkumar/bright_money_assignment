
from django.db import models
from django.urls import reverse

# Creating Users for account creation and validation
class Users(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	is_logged_in = models.BooleanField(default=False)
	access_tkn = models.CharField(max_length=200, default=None)
	item_id=models.CharField(max_length=200, default=None)


	def __str__(self):
		return str(self.username)

	def get_absolute_url(self):
		return reverse('users:login')

# Creating database for storing account details
class Accounts(models.Model):
	user = models.ForeignKey(Users, on_delete = models.CASCADE)
	account_no = models.IntegerField()
	bank_name = models.CharField(max_length=200)