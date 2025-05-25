# Youtube API Django DRF Project

This is a Django + Django Rest Framework (DRF) project. API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Requirements

- Python 3.9+
- pip

## Setup Venv
1. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:

   - Create a `.env` file in the project root
   - Add your YouTube API keys and query term:
     ```
     YOUTUBE_API_KEYS=<All keys comma separated>
     YOUTUBE_QUERY=<query you want to search for>
     ```

4. Run the migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the API:
   Open your browser and go to `http://127.0.0.1:8000/api/videos/` to see the list of YouTube videos.
