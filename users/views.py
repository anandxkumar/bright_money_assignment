from django.http import HttpResponse
from .models import Users
from django.template import loader
from django.http import Http404
from plaid import Client
from .tasks import test_func, getAccountsCelery  
from mainApp.settings import PLAID_CLIENT_ID, PLAID_SECRET_KEY, PLAID_ENV


# renders on homepage
def index(request):
	# Get all users
	all_users = Users.objects.all()
	# render index.html
	template = loader.get_template('users/index.html')
	context  = {
		all_users : 'all_users',
	}
	return HttpResponse(template.render(context, request))

def login(request):
	template = loader.get_template('users/login.html')
	login_message = 'Enter your credentials to login into the system'
	context  = {
		'login_message': login_message,
	}
	return HttpResponse(template.render(context, request))

def success_loggin(request, user_id):

	return HttpResponse("<h2>User profile for user: " + str(user_id) + " </h2>" )

def logout(request):
	template = loader.get_template('users/login.html')
	login_message = 'Logged out successfully. Enter your credentials to login into the system'
	context  = {
		'login_message': login_message,
	}
	return HttpResponse(template.render(context, request))


## Get all transaction details
def getAllData(access_tkn):

	client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET_KEY, environment=PLAID_ENV)
	response = client.Transactions.get(access_tkn,
									start_date='2021-09-25',
									end_date='2021-10-25')

	return response


def validate(request):
	template = loader.get_template('users/login.html')
	username = request.POST['username']
	password = request.POST['password']
	print(username)
	print(password)
	try:
		user = Users.objects.get(username=username, password=password)
		print("is valid",user.is_logged_in)
		user.is_logged_in = True
		user.save()

		login_message = "Sucessfully logged in"

		access_tkn = user.access_tkn

		request.session['access_tkn']=access_tkn
		context = {
			'user': user,
			'login_message': login_message
		}

		template = loader.get_template('users/success_loggin.html')
	except:
		login_message = "Incorrect Credentials. Please Try Again...."		
		context = {
			'user': None,
			'login_message': login_message
		}
		return HttpResponse(template.render(context,request))

	username=None
	password=None
	access_tkn=None
	return HttpResponse(template.render(context, request))


def invalidate(request):
	request.session['access_tkn'] = None
	template = loader.get_template('users/login.html')
	user_id = request.POST['user_id']
	context = {}
	try:
		user = Users.objects.get(pk=user_id)
		user.is_logged_in =False
		user.save()
	except:
		print('')
	user_id = None
	return HttpResponse(template.render(context, request))

def signup(request):
	template = loader.get_template('users/signup.html')
	context = {}
	return HttpResponse(template.render(context, request))


# Uses sandbox environemt
def getPublicToken():

	# Using legacy library for generating Public Enviroment
	INSTITUTION_ID = 'ins_1' # The ID of the institution the Item will be associated with
	# Creating client
	client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET_KEY, environment=PLAID_ENV)
	# Creating public token
	res = client.Sandbox.public_token.create(
			INSTITUTION_ID,
			['transactions'],
			webhook='https://sample-webhook-uri.com' # Expose a webhook for handling plaid transaction updates and fetch the transactions on receival of a webhook
		)


	public_token = res['public_token']

	return public_token, client

def exchangeToken(public_token, client):

	# Using legacy method
	
	response = client.Item.public_token.exchange(public_token)
	access_tkn = response['access_token']
	item_id = response['item_id']
	# print("access_tkn: ", access_tkn, "item_id: ", item_id)
	return access_tkn, item_id


# For adding user in database
def register(request):
	all_users = Users.objects.all()
	template = loader.get_template('users/login.html')
	username = request.POST['username']
	password = request.POST['password']
	email = request.POST['email_id']

	public_token, client = getPublicToken()
	print("Successfully Generated Public Token for user ",username," ",public_token)
	access_tkn,item_id = exchangeToken(public_token, client)

	# Creating a user
	user = Users.objects.create(username=username,password=password,email=email,access_tkn=access_tkn,item_id=item_id)
	# Saving it in db
	user.save()

	context  = {
		all_users : 'all_users',
	}
	# Returning request
	return HttpResponse(template.render(context, request))

# To get Transactions details 
def getTransactions(request):
	template = loader.get_template('users/success_loggin.html')
	user_id = request.POST['user_id']
	access_tkn = request.session['access_tkn']
	context = dict()
	if access_tkn:
		try:
			user = Users.objects.get(pk=user_id)
			# Get Transactions details from all detail
			response = getAllData(access_tkn)
			transactionData = response['transactions']
			context = {	
				'user':user,
				'transactionData':transactionData,
				'response_message':'Successfully Loaded Transaction Data'
			} 
		except:
			template = loader.get_template('users/login.html')
		
	
	else:
		template = loader.get_template('users/login.html')
	
	return HttpResponse(template.render(context, request))

# To get Total number of Transactions 
def getTotalTransactions(request):
	template = loader.get_template('users/success_loggin.html')
	user_id = request.POST['user_id']
	access_tkn = request.session['access_tkn']
	context = dict()
	if access_tkn:
		try:
			user = Users.objects.get(pk=user_id)
			# Get Transactions details from all detail
			response = getAllData(access_tkn)
			totalTransactionData = response['total_transactions']
			context = {	
				'user':user,
				'totalTransactionData':totalTransactionData,
				'response_message':'Successfully Loaded Total Number of Transaction Data'
			} 
		except:
			template = loader.get_template('users/login.html')
		
	
	else:
		template = loader.get_template('users/login.html')
	
	return HttpResponse(template.render(context, request))

# get Account details
def getAccounts(request):
	template = loader.get_template('users/success_loggin.html')
	user_id = request.POST['user_id']
	access_tkn = request.session['access_tkn']
	context = dict()
	client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET_KEY, environment=PLAID_ENV)
	
	try:
		user = Users.objects.get(pk=user_id)
		response = client.Accounts.balance.get(access_tkn)
		accountData = response['accounts']
		context = {	
			'user':user,
			'accountData':accountData,
			'response_message':'Successfully Loaded Account Data'
		} 
	except:
		print("Redirecting")
		template = loader.get_template('users/login.html')
	
	return HttpResponse(template.render(context, request))


# Using celery for getting accountData  
def testCelery(request):  
    # call the test_function using delay, calling task  
    test_func.delay()  
    access_tkn = request.session['access_tkn']
    #client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET_KEY, environment=PLAID_ENV)
    accountData = getAccountsCelery.delay(access_tkn)

	
    return HttpResponse("Success")
