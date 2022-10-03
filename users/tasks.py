from celery import shared_task
from plaid import Client
from django.http import HttpResponse
from .models import Users
from django.template import loader
from website.settings import PLAID_CLIENT_ID, PLAID_SECRET_KEY, PLAID_ENV

@shared_task(bind=True)  
def test_func(self):  
    for i in range(10):  
        print(i)  
    return "Completed"  

@shared_task(bind=True)
def getAccountsCelery(self, access_tkn):
    client = Client(client_id=PLAID_CLIENT_ID, secret=PLAID_SECRET_KEY, environment=PLAID_ENV)
    response = client.Accounts.balance.get(access_tkn)
    accountData = response['accounts']
    print("Account DATA", accountData)
    return 'Successfully return Account Data'

# @shared_task
# def adding_task(x, y):
#     print(x+y)
#     return x + y
