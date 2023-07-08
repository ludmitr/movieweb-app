**Movie Library Web Application**
Overview
The Movie Tracker is a Flask-based web application that allows users to add, edit, and manage movies in their personal list. It uses the Open Movie Database (OMDb) API to fetch movie details and provides functionality for user authentication.

**Features**
Add Movie: Users can add movies to their list. The movie details are fetched from the OMDb API based on the search name given by the user.

Update Movie: Users can edit the details of movies in their list.

User Authentication: The application supports user login and logout functionalities. Passwords are validated, and on successful login, user data is stored in the session.

**Routes**
/add_movie: A POST route that accepts a movie name to search and a user id to add the movie to the user's list.

/users/<int:user_id>/edit_movie/<movie_id>: A dual-purpose route that supports GET for retrieving movie data for editing and POST for updating the movie data in the user's list.

/login: A POST route for user login. It accepts a username and password, validates them, and on successful validation, stores the user data in the session.

/logout: A route for user logout. It removes user data from the session.
.
.
.

Setup and Installation
To be updated with the steps for setting up and installing the application.

Usage
To be updated with the steps for using the application.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

License
To be updated with the license details.

This readme is a basic template and may need further updates based on additional functionalities of your application.
