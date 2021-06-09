# install virtual environment using command

pip install virtualenv

# then create a virtual environment in downloaded repository using command

virtualenv venv  (here venv is the name of virtual environment you can name it whatever you want)

# then activate the virtual environment using command 

venv\Scripts\activate

# now use the command given below to install all requirements for this project

pip install -r requirements.txt

# now use command to runsever

python manage.py runserver


admin login..........

username- admin
password- admin

first create a user by registering and then add it to admin group in user model of admin panel
then create a payment method in payment model of admin panel and add a QR code image 

now you are good to go
