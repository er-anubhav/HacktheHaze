# HackTheHaze

## Project Setup

HackTheHaze is a web application that allows users to scrape images from websites. It consists of a FastAPI backend and a React frontend.

## Features

- User authentication via Supabase
- Image scraping from multiple websites
- Scrape history tracking for authenticated users
- Responsive UI with modern design
- Image preview and download functionality

## Environment Setup

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create a `.env` file in the frontend folder with your Supabase credentials:
```
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

3. Start the development server:
```bash
npm run dev
```

### Backend

1. Create a virtual environment:
```bash
cd backend
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend folder with your Supabase credentials:
```
DATABASE_URL=your_postgresql_database_url_from_supabase
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret_key
ENV=development
```

4. Start the backend server:
```bash
uvicorn main:app --reload
```

## Database Setup

1. Create a new Supabase project
2. Create a table called `scrape_history` with the following columns:
   - `id` (int8, primary key, auto-increment)
   - `user_id` (uuid, not null, references auth.users)
   - `urls` (jsonb, not null)
   - `image_count` (int4, not null)
   - `created_at` (timestamptz, not null, default: now())

3. Set up Row Level Security (RLS) policies to ensure users can only access their own data:

```sql
-- Enable RLS
ALTER TABLE scrape_history ENABLE ROW LEVEL SECURITY;

-- Create policy for users to view their own data
CREATE POLICY "Users can view their own scrape history"
  ON scrape_history
  FOR SELECT
  USING (auth.uid() = user_id);

-- Create policy for users to insert their own data
CREATE POLICY "Users can insert their own scrape history"
  ON scrape_history
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

## Deployment

- Backend: Deploy to a service like Heroku, Render, or Railway
- Frontend: Deploy to Vercel or Netlify
- Make sure to update the CORS settings in the backend to allow requests from your frontend domain

## API Endpoints

- `POST /scrape`: Scrape images from URLs
- `GET /history`: Get authenticated user's scrape history
- `GET /health`: API health check

## Security Notes

- Authentication is handled via Supabase
- API rate limiting is recommended for production
- Implement proper error handling and logging