# **RecipeShare (Backend API)**

# [Table of Contents](#table-of-contents)

- [**Project Overview**](#project-overview)
  - [Objective](#objective)
  - [Links to Deployed Project](#links-to-deployed-project)
  - [Project Structure](#project-structure)
  - [User Stories](#user-stories)
- [Database Designs](#database-designs)
  - [Models](#models)
- [Features](#features)
  - [Homepage](#homepage)
  - [Profile Data](#profile-data)
  - [Recipes Data](#posts-data)
  - [Comments Data](#comments-data)
  - [Followers Data](#followers-data)
  - [Votes Data](#reviews-data)
  - [Categories Data](#contact-data)
- [Agile Development](#agile-development)
  - [GitHub Project Board](#github-project-board)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
  - [Languages](#languages)
  - [Frameworks & Libraries](#frameworks-libraries)
- [Deployment](#deployment)
- [Credits](#credits)

# **Project Overview**

## Objective

The objective of the RecipeShare Back-end API is to serve as the foundation for a community-driven interactive recipe-sharing platform. The Django Rest Framework (DRF) API is designed to facilitate seamless communication between the front-end web application and the database, enabling users to create, retrieve, update, and delete recipes, profiles, comments and votes as well as perform other essential actions within the platform.

## Links to Deployed Project

  - The backend  of this project is deployed on Heroku and can be found at: [RecipeShare API](https://ci-pp5-backendapi-sb-1f7f0e4a782e.herokuapp.com/)
  - The GitHub repository for the frontend front end of the project can be found at: [RecipeShare Front End Repository](https://github.com/stevebiczyk/pp5-recipe-share-sb)
  - The front end of this project is also deployed on Heroku and can be found at: [RecipeShare Web App]( https://recipe-share-sb-38760b27e610.herokuapp.com/)

## Project Structure

The RecipeShare DRF API was losely based on the DRF API part of the Moments walkthrough [drf-api](https://github.com/Code-Institute-Solutions/drf-api) that was completed as part of the Advanced Front End section of the Code Institute's Diploma in Fullstack Development program.
As per the requirements of the final project, two different models were created, the Recipes and the Votes models.

[Back to top](<#table-of-contents>)

# User Stories

## Developer User Stories

- As the developer, I will create a new repository on GitHub so that I can develop the API separately from the front end.
- As a developer, I will install the necessary packages and framework dependencies to ensure that the API is fully functional both during development and as the deployed project.
- As the developer, I will create a superuser account so that I can develop and test features from the backend.
- As the developer, I will create an gitignore file so that the sensitive information is kept hidden from the public.
- As the developer, I will test all the features of the API so I can be sure that the deployed project will work with the front end.
- As the developer, I will deploy the finished project to Heroku so that it's available for the public to access and use.

## Profiles User Stories

- As the developer, I will create a Profiles app so that users can create and edit their profiles and view others'.
- As the developer, I will create a Register/Login feature so that users can create an account and log into their existing account.
- As the developer/superuser, I want to be able to access all the user profiles so that i can view and edit their information.
- As the developer, I will create a Logout feature so that users can log out of their account when they finish using the site.

## Recipes User Stories

- As the developer, I will create a Recipes app so that registered/logged-in users can post, view and interact with recipes on the platform.
- As a developer/superuser, I can view a list of all recipes so that I can see all recipes currently in the backend API.
- As a developer/superuser, I can look up a specific recipe by ID so that I can view the recipe details of a singular recipe.
- As a developer/superuser, I can edit a specific recipe by ID so that information remains updated in the API pertaining to that recipe.
- As a developer/superuser, I can delete a specific recipe so that no erroneous information will appear on the site (or in the backend API) if the recipe details are incorrect or irrelevant.

## Votes User Stories

- As the developer, I will create a Votes app so that registered/logged-in users can upvote or downvote recipes and view other users' votes.
- As a developer/user, I can create a vote so that other logged-in users can see what I thought about a recipe.
- As a developer/user, I can view the total number of up and down votes for each recipe so that I can see what other users thought of that recipe.
- As a developer/superuser I can edit other users' votes so that I can change or remove votes if required.

## Comments User Stories

- As the developer, I will create a Comments app so that registered/logged-in users can add further information to recipes and view other users' comments.
- As the developer/superuser, I can access all comments so that I can edit or delete a certain comment from the backend if it's inappropriate or erroneous.
- As a logged in user, I want to be able to create a comment, edit it and delete it and view other users' comments.
- As a logged in user, I want to be able to see the number of comments for each recipe to see which is the most commented recipe.

## Categories User Stories

- As the developer, I will create a Categories feature so that registered/logged-in users can access recipes that are grouped according to their requirements.
- As the developer/user I want to be able to view the categories and select one or more of them so that I can view recipes that are relevant to my needs.
- As the developer/user I want to be able to add categories and assign them to registered users'/my recipes so that other users can access recipes that are relevant to their interested/ dietary needs.

## Followers User Stories

- As the developer, I will create a Followers app so that registered/logged-in users can follow other users whose recipes they find relevant to their interests and needs.
- As the developer/superuser I want to be able to see the followers of other users so that I can see which are the most popular profiles.
- As the developer/logged in user I want to be able to follow and unfollow other users' profiles so that I can keep track of users who have interesting recipes or comments.

## Testing User Stories

- As the developer, I will thoroughly test my application so that it's free of bugs as much as possible.
- As the developer, I will document the tests I carried out and the bugs I found so that users and other developers are aware of the issues I discovered and addressed.
- As the developer, I will document any bugs I found but haven't been able to fix so that users and other developers are aware of them.

## Documentation User Stories

- As the developer, I will thoroughly document the development of the application so that other developers can follow the development pocess and more easily contribute if required.
- As the developer, I will create a Readme file for the application so that the documentation is clear, structured and accesible for other developers.

# Database Designs

## Models

For the purposes of this project, I created a database losely based on the DRF API of the Moments walktrough project.
The database contains the following models:

 - Profiles (Shows user information for the registered users)
 - Recipes (Shows all the necessary information for the recipes for other users)
 - Votes (Users can vote on recipes and change or delete their vote)
 - Comments (Users can write comments to add relevant information to recipes)
 - Categories (Users can create categories and use them to select groups of recipes)
 - Followers (Allows users to follow and unfollow other profiles)

The Recipes and Categories models arecompletely separate from the models used in the Moments walkthrough while the Votes model is losely based on the original Likes model.

[Back to top](<#table-of-contents>)

# Features

## Homepage

When you open the Root Route, you're taken to the homepage, where you'll see a welcome message for the RecipeShare API.  

![API Homepage](images/homepage.png)

## Profile Data

All the profiles created for the RecipeShare are listed in the Profiles section.

![Profile List](images/profiles.png)

The profiles model includes the following fields:

- owner
- created_at
- updated_at
- name
- bio
- avatar

The following fields were added through the profiles serializer:

- is_owner
- following_id
- recipes_count
- followers_count
- following_count

For the admin user, full CRUD functionality is available for all profiles. Other logged in users can access, edit and delete their own profile. This is done via a form that's part of the Django Rest framework.

![Profile Edit Form](images/profile-edit.png)

## Recipes Data

On the Recipes List page, the user can view all recipes created in the application.

![Recipes List](images/recipes.png)

The fields listed below are included in the recipes model:

- owner
- created_at
- updated_at
- title
- ingredients
- instructions
- cooking_time
- image

The following fields were added through the recipes serializer:

- is_owner
- profile_id
- profile_image
- like_id
- review_id
- likes_count

A logged-in superuser can create a recipe from the backend via a Django form. This recipe will be visible for logged in users on the front end.
The supeuser can also edit or delete recipes if required.

![Create a recipe](images/create-recipe.png)

## Comments Data

The Comments section contains a list of all the comments and related content stored in the API.

![Comments List](images/comments.png)

A logged in superuser can fill out a form to create a comment. This will be saved to the API and will also be accessible from the frontend.

![Create a Comment](images/create-comment.png)

The superuser can also editor delete a comment from the API.

![Edit Comment Form](images/edit-comment.png)

## Followers Data

On the Followers page, all followers of profiles are shown.

![Follower List](images/followers.png)

After logging in, the superuser can fill out a form with the 'owner' and 'followed' fields to have a user follow another. 
![Create a Follower Post](images/create-followers.png)

The same superuser can edit the form to change the 'owner' and 'followed' fields. the owner / follower combination can only be used one time, otherwise an error message is shown alerting that the owner is already following the other user.

Clicking the delete button deletes this owner-follower combination from the database.

![Edit Followers](images/edit-followers.png)

## Votes Data

Users can see a list of all votes in the API. 

![Votes List](images/reviews.png)

Once logged in, the superuser can create a Vote for a Recipe. Only one Vote per user allowed for each Recipe. Two types of Votes are availableto the user, an upvote or a downvote, depending on their experience with the Recipe. They can also retract and change their Vote if they want to do so.

# Agile Development

## GitHub Project Board

I used a Github project board for creating User Stories and keeping track of them during the development of this API. I used Agile principles throughout the development.
<!-- - Epics, Must haves, Nice to haves, etc. -->

![GitHub Project Board](images/project-board.png)


[Back to top](<#table-of-contents>)

# Testing

- Add detailed description of the testing process

# Technologies Used

## Languages

* [Python](https://www.python.org/) - The programming language behind the DRF framework.

## Frameworks, Libraries & Software

- [Django Rest Framework](https://www.django-rest-framework.org/) - Python framework used for building Web APIs in Django, used to interact with frontend applications.
- [Git](https://www.git-scm.com/) - Version control system, used for keeping track of the changes made to the file system during the development process.
- [GitHub](https://github.com/) - Github is cloud-based service for version control using Git. It is used to host the repository and the project board for this project.
- [GitPod](https://www.gitpod.io) - Cloud based IDE, used for creating and editing the files in the repository and also for pushing the changes to GitHub.
- [Heroku](https://en.wikipedia.org/wiki/Heroku) - Hosting platform used for making this project accessible on the web.
- [Cloudinary](https://cloudinary.com/) - An image hosting service used for storing the image filesfor this project.
- [Pillow](https://pypi.org/project/Pillow/) - Pillow is the Python Imaging Library that was used for this project. It adds image processing capabilities to the Python interpreter.
- [Django Rest Auth](https://django-rest-auth.readthedocs.io/en/latest/#) - Used in this project to provide REST API endpoints for user authentication and registration. 
- [Gunicorn](https://pypi.org/project/gunicorn/) - Gunicorn ‘Green Unicorn’ is a Python WSGI Application Server used for this project.
- [Psycopg2](https://pypi.org/project/psycopg2/) - Psycopg is a popular PostgreSQL database adapter for the Python programming language.
- [PEP8 Validation](https://pypi.org/project/pep8/) - A validation tool to check Python code against various style conventions in PEP 8.

[Back to top](<#table-of-contents>)

# Deployment

The project was deployed to [Heroku](https://www.heroku.com). The deployment process is detailed below:

1. First, create a GitHub repository from the [Code Institute template](https://github.com/Code-Institute-Org/gitpod-full-template). 

2. Click 'Use this template' and fill in the details for the new repository. When that's done, click 'Create Repository From Template'.

3. Once the repository is created, click the green 'Gitpod' button to open the Gitpod workspace.

4. Install necessary libraries like Django, Gunicorn, Psychopg2 and Cloudinary using these commands in the Gitpod terminal:

* ```pip3 install 'django<4'```
* ```pip3 install 'django<4' gunicorn```
* ```pip3 install 'dj_database_url psycopg2```
* ```pip3 install 'dj3-cloudinary-storage```

5. After completing these installations, create a requirements.txt file using the command below, which will create and add required libraries to the file:

* ```pip3 freeze --local > requirements.txt```


6. Now, create the actual project using:

* ```django-admin startproject project-name ``` 

7. After the project has been created, you can create each app. The current project includes: Profiles, Recipes, Comments, Votes, Categories and Followers.

* ```python3 manage.py startapp appname```

8. Add these apps to the settings.py file in the INSTALLED_APPS list.

8. Migrate these new developments and run the server to ensure everything is working properly in the local environment. It's a good idea to start with a 'dry-run' migration to check for any typos or spelling errors. The command for this is:
* ```python3 manage.py makemigrations --dry-run``` 

  Then you can prepare the migrations
* ```python3 manage.py makemigrations```

  and migrate the changes:
* ```python3 manage.py migrate```

  Now run the server by entering the command below. Click the 'open browser' button when it pops up to see the page in your local browser.
* ```python manage.py runserver```

9. Once the above steps are completed, you can create the Heroku app and link the GitHub repository.

    Sign into your [Heroku account](https://www.heroku.com/), and click on 'New' at the top right-hand corner to create a new app.

10. Choose a unique app name, fill out the region and click on the 'Create app' button at the bottom.

11. Next, connect an external PostgreSQL database to the app, using [ElephantSQL](https://customer.elephantsql.com/login). When you've logged in and are on the ElephantSQL dashboard, click 'Create New Instance' to create a new database. Complete the following:
* Name the database
* Select 'Tiny Turtle Free Plan'
* Select data center near you then click 'Create Instance'.
* Return to the ElephantSQL Dashboard and click your newly created database instance. 
* Copy the Database URL and return to Heroku.

12. In the Heroku app settings tab, click 'Reveal Config Vars'. Create a variable called DATABASE_URL and paste the URL you just copied from ElephantSQL. This will connect the database to the app. 

13. Now, in the Gitpod environment, create an env.py file. In this file, add the following code to import the os library, set the environment variables, and keep a secret key, respectively:

* ```import os```
* ```os.environ["DATABASE_URL"]```
* ```os.environ["SECRET_KEY"]```

14. Return to the Heroku Config Vars settings and create a variable called SECRET_KEY. Copy and paste the secret key from the env.py file into this variable. 

    REMEMBER: add the env.py file to the .gitignore file so none of this information is committed and pushed to GitHub and therefore, publicly accessible.

15. Now, to connect to the environment and settings.py file, add the following code to the settings.py file:

* ```import os```
* ```import dj_database_url```
* ```if os.path.isfile("env.py"):```
* ```import env```

16. Then, in the same file, remove the unsafe secret key and replace it with:
```SECRET_KEY = os.environ.get('SECRET_KEY')```

17. Next, set up [Cloudinary](https://cloudinary.com/users/login) to be able to store static files (images, etc). Create or login to your account and copy the API variable from the Cloudinary dashboard.

18. Add the Cloudinary URL to the gitpod environment in the env.py file, making sure it's correct:

* ```os.environ["CLOUDINARY_URL"] = "cloudinary://************************"```

19. In the Heroku app, add the Cloudinary URL to the Config Vars, along with the DISABLE_COLLECTSTATIC variable (equal to 1) to be able to properly deploy.

20. In the gitpod environment, in the settings.py file, add the installed Cloudinary Libraries to the INSTALLED_APPS list. 

    REMEMBER to put them in this order: 

    * cloudinary_storage
    * django.contrib.staticfiles
    * cloudinary

21. Add the Heroku app and localhost to the ALLOWED_HOSTS list in the settings.py file.

22. Now, create the Procfile directory in the Gitpod environment. Add the following line:

* ```web: gunicorn proj_name.wsgi?```

23. Save the files, commit and push these changes to GitHub. 

24. Scroll to the top of the settings page in Heroku and click the 'Deploy' tab. For deployment method, select 'Github'. Search for the repository name you want to deploy and then click connect.

    The deployed Heroku API can be found [here](https://ci-pp5-backendapi-sb-1f7f0e4a782e.herokuapp.com/).
    The backend GitHub repository can be found [here](https://stevebiczyk-cipp5backen-u3gmtuyoysq.ws-eu102.gitpod.io/).

[Back to top](<#table-of-contents>)


# Credits

This application and website are completely fictional and for use only from a learning standpoint. The site was created for Portfolio Project 5 (Advanced Front End) - Diploma in Full Stack Software Development through [Code Institute](https://www.codeinstitute.net).

I'd like to say thank you to:

- The Code Institute Slack Community and the tutors for their help with the issues I encountered while working on the course material and my projects.

- My mentor, Dick Vlaanderen for his mentoring and guidance with my numerous project and industry related queries.

[Back to top](<#table-of-contents>)