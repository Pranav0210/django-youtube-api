# Youtube API Django DRF Project

This is a Django + Django Rest Framework (DRF) project. API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Requirements

- Python 3.9+
- pipenv

## Environment Variables
   - Create a `.env` file in the project root
   - Copy the keys from the `example.env` file into the created `.env` file

## Setup Venv
1. Install dependencies and create a virtual environment:

   ```bash
   pipenv install
   ```

2. Activate pipenv virtual environment:

   ```bash
   pipenv shell
   ```

3. Run the migrations to set up the database:

   ```bash
   python3 manage.py migrate
   ```

4. Start celery worker
   ```bash
   celery -A fam_youtube_api worker --loglevel=info
   ```

5. Start celery beat
   ```bash
   celery -A fam_youtube_api beat --loglevel=info
   ```

6. Start the development server:

   ```bash
   python3 manage.py runserver
   ```

7. Access the API:
   Open your browser and go to `http://127.0.0.1:8000/api/videos/` to see the list of YouTube videos.


## How I worked this assignment out:

### The choice of framework -
### The folder structure -
### The Problem Statement break down -
### I had fun! -