# Welcome to the Chit Chat app repository.

This app allows users to talk in real time with another of the a browser. There is also a bot that is useful for a variety of features.

## M3 Questions

### Why did you choose to test the code that you did?
I chose to test the code that I did because as projects grow and become more complex they many times become delicate. If a bug occurs finding that bug with premade test cases could take hours. I built out unit test cases so that in the future finding bugs will be very easy. I can also run this test at anytime to make sure that everything is working the way its supposed to.

### Is there anything else you would like to test if you had the time (or was asked to do so)?
I tested just about everything in my project. Now that I learned unit testing I plan on using these skills to make test cases for my old projects. I may even go back to my recipe app and add unit tests, just to improve the project before I put it in my portfolio. 

# Setup
### Step 1 - Clone Repository
1. Open a terminal in your environment
2. Clone this repository using git clone https://github.com/NJIT-CS490/project2-m2-mdm56

### Step 2 - Install python dependencies
1. 'npm install'
2. 'npm install react-google-login'
2. 'npm install react-dom'
3. 'pip install flask'
4. 'pip install flask_sqlalchemy'
5. 'pip install flask_socketio'
6. 'pip install dotenv'
7. 'pip install requests'


### Step 3 - Set Up Postgres Database and Tables
1. Install PostGreSQL using `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Be sure to enter yes to all prompts.    
2. Start Your PSQL database: 
      A) `sudo service postgresql initdb` 
      B) `sudo service postgresql start`  
3. Make a yourself a user with `sudo -u postgres createuser --superuser $USER` 
4. Create a database with 'sudo -u postgres createdb $USER'
5. Create a user for yourself with 'create user [your_username_here] superuser password '[your_password_here]'
6. Create a new file called 'sql.env' and add the following text:
      export SQL_USER=[your_username_here]
      export SQL_PASSWORD=[your_password_here]
      export USER=[your_username_here]
      export DATABASE_URL='postgresql://[your_username_here]:[your_password_here]@localhost/postgres'

### Step 4 - Setting up SQLAlchemy
1. Run `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. run `sudo service postgresql restart` 

### Step 5 - Start the flask app in your environment
1. Navigate to the root directory of the project
3. In one terminal run 'npm run watch'
2. In another terminal run flask-launcher.py using the terminal command 'python app.py'
3. The app is now running locally and you should be able to see it using your local ip and port 8080
    If you are running on aws, simply click preview to see the web app

### Step 6 - Run the app on Heroku
1. Sign up for heroku at heroku.com 
2. Install heroku in your terminal by running 'npm install -g heroku'
3. Name the app 'chitchat'
4. Go through the following steps:
    heroku login -i
    heroku create
    git push heroku master
5. Add secret keys (from sql.env) by going to https://dashboard.heroku.com/apps
    and clicking into your app. Click on Settings, then scroll to "Config Vars." Click
    "Reveal Config Vars" and add the key value pairs for the five keys (use the same key names)
6. In terminal push again to start app again with the command 'git push heroku master'

## Running Tests
In the main directory simply run this command:

coverage run -m --source=. unittest tests/*.py && coverage html

Then, look at the index.html file in the /htmlcov folder to see the coverage of the tests

## Issues

There should be none

## Technical Challenges
 1. Working with sockets was very challenging
 2. Moving th db to heroku was tricky
 3. Getting react functional components to work how I want them to took some practice
