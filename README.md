In order to run the project run the following commands: 
- Create a virtual environment (using anaconda run conda create -n plaidenv python=3.8 then activate using conda activate plaidenv) 
- Install dependencies by running pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver
- The website will we available at http://localhost:8000/users/


Following are the different steps involved in the project:
- <b>Step 1: Registering users</b><br />
Created a class in models.py called Users with fields username, password, email, is_logged_in, access_tkn and item_id all of datatype character
- <b>Step 2: Login Validation</b><br />
In this step basically the user will have to input the username and password. We check if the credentials are found in the db. If yes then we set is_logged_in of User object = True, and go to the profile page.
Else we raise a message with incorrect credentials and reload the login page.
- <b>Step 3: Get Transaction and Account Detail</b><br />
Currently 3 APIs have been integrated into the project.<br />
Transactions Data: Using the access token, we can specify the start date and end date between whose all transactions we want to get. <br />
Total Number of Transactions: To get the total number of transactions we can simply return response['total_transactions']. <br />
Account Data: Return the balance details of accounts
- <b>Step 4: Using celery for Asynchronous Task</b> <br />
We are using redis as the broker at port 6379. We create a task in task.py where we are getting the Accounts Data. An API is exposed with path getAccountsCelery. When it is called the access token is passed to the task and it gets the accountData, and returns Success.
- <b>Step 5: Logout</b> <br />
You can click on the logout button on the top right corner to logout. It will render the login page again.

The PLAID client ID, Secret Key and environment are stored as environment variables. These values are exported in bashrc script, and are loaded in the main folder settings.py file using os.getenv.

Refer to [<b>documentation.pdf</b>](https://github.com/anandxkumar/bright_money_assignment/blob/main/Bright%20Money%20Assignment%20Documentation.pdf) for detailed step by step guide.
