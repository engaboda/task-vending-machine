# task-vending-machine
vending machine

# Setup
The first thing to do is to clone the repository:

$ git clone https://github.com/engaboda/task-vending-machine.git
$ cd task-vending-machine

# Create a virtual environment to install dependencies in and activate it:

$ vertualenv -p python3 env
$ . env/bin/activate

# Then install the dependencies:

(env)$ pip install -r requirements.txt

# Once pip has finished downloading the dependencies:

(env)$ python manage.py migrate

And navigate to http://127.0.0.1:8000/gocardless/.


# To run the tests, cd into the directory where manage.py is:

(env)$ ./manage.py test
