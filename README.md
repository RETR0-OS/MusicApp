# MusicApp - Crescendo
 
## Project Description
Crescendo is a web application that allows users to register, log in, and manage their music preferences. It integrates with Spotify and Google for authentication and provides a personalized music experience based on user preferences. Crescendo takes your spotify playlist and makes it completely offline to avoid adds and give a seemless listening experience.

## Features
- User registration and login
- Google OAuth login
- Spotify API integration
- User profile management
- Music preference selection
- Sptify playlist download
- Middleware for login requirement

## Installation Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/RETR0-OS/MusicApp.git
    cd MusicApp
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
4. Obtain Spotify Developer Client ID, and Client secret for Spotify link and replace the following lines in settings.py:
    ```sh
    CLIENT_ID = "Spotify client ID here"
    CLIENT_SECRET = "Spotify Client Secret here"
   ```
5. Obtain Google Developer Client ID, and Client secret for OAuth authorization and replace the following lines in settings.py:
   ```sh
     GOOGLE_CLIENT_ID = "Google client ID here"
     GOOGLE_CLIENT_SECRET = 'Google client secret here'
   ```

6. Create a secure secret key for the project and replace this line in settings.py:
   ```sh
     SECRET_KEY = "Your secret key here"
   ``` 

7. Set up the database:
    ```sh
      python manage.py migrate
    ```

8. Create a superuser:
    ```sh
      python manage.py createsuperuser
    ```

9. Run the development server:
    ```sh
    python manage.py runserver
    ```

10. Open your browser and navigate to `http://localhost:8000` to access the application.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
