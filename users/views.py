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
	# url = "https://sandbox.plaid.com/transactions/get"

	# payload = {
	# 	"client_id":"5da9e9d3470e370016651aa3",
	# 	"secret":"1026c23bcd23fccd4f9dabb1f9f172",
	# 	"access_token": access_tkn,
	# 	"start_date":"2017-10-25",
	# 	"end_date":"2019-10-25"
	# }

	# data = json.dumps(payload)

	# headers = {
    # 'Content-Type': "application/json",
    # 'cache-control': "no-cache",
    # 'Postman-Token': "bec1a651-a9e8-4771-9b6e-bf668f000232"
    # }

	# rawResponse = requests.request("POST", url, data=data, headers=headers)
	# response = json.loads(rawResponse.text)
	# prettyResponse = json.dumps(response, indent=4, sort_keys=True)
	INSTITUTION_ID = 'ins_3'
	client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET_KEY, environment=PLAID_ENV)
	# res = client.Sandbox.public_token.create(
	# 		INSTITUTION_ID,
	# 		['transactions'],
	# 		webhook='https://webhook.site/82e5cebe-b8d0-4178-ac51-bb3699d782ac'
	# 	)



	response = client.Transactions.get(access_tkn,
									start_date='2021-09-25',
									end_date='2021-10-25')

	return response

# def getAccountData(access_tkn):
# 	response = getAllData(access_tkn)
# 	accountData = response['accounts']
# 	print(accountData)
# 	return accountData

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
	transactionData=None
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

	# url = "https://sandbox.plaid.com/sandbox/public_token/create"
	# payload = {
	# 	"public_key":"91e20631f435dd6896adf30031b81c",
	# 	"institution_id":"ins_3",
	# 	"initial_products":["transactions"],
	# 	"options":{
	# 		"webhook":"https://webhook.site/82e5cebe-b8d0-4178-ac51-bb3699d782ac"
	# 	}
	# }
	# data = json.dumps(payload)
	# headers = {
	#     'Content-Type': "application/json",
	#     'cache-control': "no-cache",
	#     'Postman-Token': "02fad5e9-5a06-4d80-b35e-db22559238e9"
	#     }
	# rawResponse = requests.request("POST", url, data=data, headers=headers)
	# response = json.loads(rawResponse.text)
	# public_token = response['public_token']
	public_token = res['public_token']
	print("PUBLIC TOKENNNN MIL GYA")
	return public_token, client

def exchangeToken(public_token, client):

	# Using legacy method
	# url = "https://sandbox.plaid.com/item/public_token/exchange"

	# payload = {
	# 	"client_id":"5da9e9d3470e370016651aa3",
	# 	"secret":"1026c23bcd23fccd4f9dabb1f9f172",
	# 	"public_token":public_token
	# }

	# data = json.dumps(payload)

	# headers = {
	#     'Content-Type': "application/json",
	#     'cache-control': "no-cache",
	#     'Postman-Token': "278806c6-0301-49d7-933d-f3c7b295e6a4"
	# }

	# rawResponse = requests.request("POST", url, data=data, headers=headers)
	# response = json.loads(rawResponse.text)
	# access_tkn = response['access_token']
	# item_id = response['item_id']
	response = client.Item.public_token.exchange(public_token)
	access_tkn = response['access_token']
	item_id = response['item_id']
	print("accees_tkn: ", access_tkn, "item_id: ", item_id)
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


# Create your views here.  
  
def testCelery(request):  
    # call the test_function using delay, calling task  
    test_func.delay()  
    access_tkn = request.session['access_tkn']
    #client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET_KEY, environment=PLAID_ENV)
    accountData = getAccountsCelery.delay(access_tkn)

	
    return HttpResponse("Success")
