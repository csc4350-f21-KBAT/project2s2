This is project group (Sprint2) of Software Engineering.

# Entertainment Finder
Have you ever had trouble finding a TV show or movie to watch or just don't have the time to go through the reviews for everything? Here lies our repository dedicated to helping you find something right now :)

# Technologies
- Python
- PostgreSQL
- ReactJS
- HTML
- CSS

# Libraries
- os
- json
- sys
- flask
- requests
- flask_login
- werkzeug.security
- flask_sqlalchemy
- dotenv

# APIs
- TheMovieDB popular movie API
- TheMovieDB top rated movie API
- TheMovieDB search movie API
- TheMovieDB detail movie API
- TheMovieDB discover movie API

# Heroku
http://mighty-shelf-43642.herokuapp.com/login

# Clones the repository
- In Visual Studio Code, creating a new directory where clone the code
- Go to the current directory
- In the terminal, type:
    - git clone git@github.com:csc4350-f21-KBAT/project2.git
    - git install Flask
    - git install requests
    - git install python-dotenv
    - sudo apt update
    - sudo apt install postgresql
    - pip install flask-login
    - pip install psycopg2-binary
    - pip install Flask-SQLAlchemy==2.1
    - npm install
    - pip install -r requirements.txt
    - npm install react-rating-stars-component
    - npm i emailjs-com
- Create and set up enviroment .env file:
    - In TheMovieDB:
        - Go to https://www.themoviedb.org/
        - Log In/Sign up your account
        - Go to "Profile and Settings" on toolbar, click "Settings"
        - Click "API" on navigation menu
        - Click "Create" tab
        - Choose "Developer"
        - Fill in the information then "Submit"
        - Copy API_KEY and API_TOKEN and paste to .env file
    - In the terminal of VSCode (set up environment variable DATABASE_URL):
        - heroku login -i
        - heroku create
        - heroku addons:create heroku-postgresql:hobby-dev -a {your-app-name}
        - heroku config
        - Look at DATABASE_URL='value-in-here'
        - Copy value-in-here and paste to .env file
    - In EmailJS:
        - Go to https://www.emailjs.com/
        - Log In/Sign up your account
        - Click "Email Services", choose "Gmail"
        - Copy Service ID
        - Click "Email Templates", choose "edit", edit variables to match variables in ReactJS
        - Copy Template ID
        - Click "Integration", look at User ID
        - Paste Service ID, Template ID and User ID to .env file

# Run Application
1. Run command in terminal (in your project directory): `npm run build`. This will update anything related to your `App.js` file (so `public/index.html`, any CSS you're pulling in, etc).
2. Run command in terminal (in your project directory): `python3 app.py`
3. Preview web page in browser 'localhost:8080/' (or whichever port you're using)

# Deploy to Heroku
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`
4. Setup variables environment: go to Settings tab at Heroku > Reveal Config Vars

# a. What are at least 3 technical issues you encountered with your project? How did you fix them?
- When doing contact function, we don't know how to connect with Gmail. When we research, we already know how to use EmailJS to connect between our app and Gmail.
- When doing setting function, we change the user's name, it doesn't automatically update immediately. Then, we have to get username from database and pass through userEffect of Setting Page.
- When doing favorite function, we don't know how to save it as an array in a new page. Finally, we saved that array to the database, and when we went to the Favorite Movie page, we loaded all our favorite movies from the database.

# b. What are known problems (still existing), if any, with your project?
- We really have trouble with mock and unmock test.
- I have solved all current problems in Sprint2 based on Proposal. Our team has completed all the functions stated in the proposal.

# Images
![Login Page](https://github.com/csc4350-f21-KBAT/project2/blob/Kash/imgs/Sign%20Up.png)
![Home Page - Popular Movie Page](https://github.com/csc4350-f21-KBAT/project2/blob/Kash/imgs/mainpage.jpg)
![Top Rated Movie Page](https://github.com/csc4350-f21-KBAT/project2/blob/Kash/imgs/Top%20Rated%20Movies.png)
![Search Page - result](https://github.com/csc4350-f21-KBAT/project2/blob/Kash/imgs/search_movies.png)
![Search Page - no result](https://github.com/csc4350-f21-KBAT/project2/blob/Kash/imgs/query_mismatch.png)
![Detail Page](https://github.com/csc4350-f21-KBAT/project2/blob/Kash/imgs/movie_overview.png)
