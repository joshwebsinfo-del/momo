# Love Journey

Love Journey is a private, elegant relationship platform for two people to preserve memories, share notes, track goals, and celebrate milestones. The experience is designed to feel premium, warm, and mobile-friendly.

## Features
- Private couple access with approved-account registration
- Memory gallery with uploads and comments
- Love story timeline
- Private love notes with future delivery support
- Goal tracking and countdowns
- Voice-message support
- Relationship playlists and statistics
- REST API endpoints for core modules

## Getting started
1. Create and activate a virtual environment.
2. Install requirements: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in the values.
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Start the dev server: `python manage.py runserver`

## Supabase notes
Set the Supabase PostgreSQL connection variables and optional Supabase Storage credentials for production media uploads.
