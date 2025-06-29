# BriefNews - AI-Powered News Summarization

A modern web application that provides AI-powered news summarization with a sleek Angular Material frontend and FastAPI backend.

## Features

- **News Articles Tab**: Browse and read summaries of the latest news articles by topic
- **URL Summarization Tab**: Paste any news article URL to get an AI-generated summary
- **Topic Filtering**: Filter articles by business, technology, science, health, or politics
- **Responsive Design**: Beautiful, modern UI that works on all devices
- **Real-time Summarization**: Instant AI-powered article summaries

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **HuggingFace**: AI summarization models
- **GNews**: News article crawling
- **Pydantic**: Data validation

### Frontend
- **Angular 19**: Latest Angular framework
- **Angular Material**: Material Design components
- **TypeScript**: Type-safe JavaScript
- **Responsive CSS**: Modern, mobile-first design

## Prerequisites

- Python 3.8+
- Node.js 18+
- HuggingFace API token

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r ../requirements.txt

# Create .env file with your HuggingFace token
echo "HF_TOKEN=your_huggingface_token_here" > .env

# Run the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `https://briefnews.onrender.com/`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:4200`

## API Endpoints

### GET /articles
Get news articles with summaries, optionally filtered by topic.

**Query Parameters:**
- `topic` (optional): Filter by topic (business, technology, science, health, politics)

**Response:**
```json
[
  {
    "title": "Article Title",
    "summary": "AI-generated summary...",
    "url": "https://example.com/article",
    "date": "2024-01-15"
  }
]
```

### POST /summarize
Summarize an article from its URL.

**Request Body:**
```json
{
  "url": "https://example.com/news-article"
}
```

**Response:**
```
AI-generated summary of the article...
```

## Environment Variables

### Backend (.env file)
- `HF_TOKEN`: Your HuggingFace API token

## Deployment

### Backend (Render/Heroku)
1. Set environment variables in your cloud platform
2. Deploy the backend code
3. Update the frontend API base URL

### Frontend (Vercel/Netlify)
1. Build the project: `npm run build`
2. Deploy the `dist` folder
3. Update the API base URL for production

## Development

### Backend Development
- API documentation: `https://briefnews.onrender.com/docs`
- ReDoc documentation: `https://briefnews.onrender.com/redoc`

### Frontend Development
- Hot reload enabled
- TypeScript compilation
- Material Design components

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Author

Rithwik Mishra - [GitHub](https://github.com/rithwik-mishra)
