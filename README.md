# BriefNews - AI-Powered News Summarization

A modern web application that provides AI-powered news summarization with a sleek Angular Material frontend and FastAPI backend. Built with the latest technologies and designed for optimal user experience.

## 🌟 Features

### 📰 News Articles
- **Topic-based Filtering**: Browse news articles by categories including Business, Technology, Science, Health, and Politics
- **AI-Generated Summaries**: Each article comes with a concise, AI-generated summary highlighting key points
- **Interactive Interface**: Modern card-based layout with loading states, error handling, and empty states
- **Article Actions**: Copy article URLs and open full articles in new tabs

### 🔗 URL Summarization
- **Custom Article Summarization**: Paste any news article URL to get an instant AI-generated summary
- **Real-time Processing**: Live feedback during summarization with progress indicators
- **Error Handling**: Comprehensive error handling for invalid URLs or processing issues
- **Copy & Share**: Easy copying of summaries for sharing or note-taking

### 🎨 User Experience
- **Dark/Light Theme**: Toggle between dark and light themes with system preference detection
- **Responsive Design**: Fully responsive interface that works on desktop, tablet, and mobile
- **Material Design**: Modern UI components with smooth animations and transitions
- **Accessibility**: Built with accessibility in mind using Angular Material components

### 🚀 Technical Features
- **Angular 19**: Latest Angular framework with standalone components
- **Angular Material**: Professional UI components and theming
- **Reactive State Management**: Using Angular signals for efficient state management
- **TypeScript**: Full type safety throughout the application
- **RESTful API Integration**: Seamless integration with FastAPI backend

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic API documentation
- **HuggingFace**: AI summarization models for intelligent content processing
- **GNews**: News article crawling and aggregation
- **Pydantic**: Data validation and serialization

### Frontend
- **Angular 19**: Angular framework with standalone components
- **Angular Material 19.2**: Material Design component library
- **TypeScript 5.7.2**: Type-safe JavaScript development
- **RxJS 7.8.0**: Reactive programming for state management
- **Angular CDK 19.2.19**: Component development kit

## 🚀 Live Demo

- **Frontend**: [https://brief-news.vercel.app/](https://brief-news.vercel.app/)
- **Backend API**: [https://briefnews.onrender.com/](https://briefnews.onrender.com/)
- **API Documentation**: [https://briefnews.onrender.com/docs](https://briefnews.onrender.com/docs)

## 📋 Prerequisites

- Python 3.11+
- Node.js 20+
- HuggingFace API token

## 🛠️ Setup Instructions

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

The locally hosted backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npx ng serve --host="0.0.0.0"
```

The locally-hosted frontend will be available at `http://localhost:4200/`

## 🔌 API Endpoints

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

## 🔧 Environment Variables

### Backend (.env file)
- `HF_TOKEN`: Your HuggingFace API token for AI summarization


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Rithwik Mishra**
- GitHub: [@rithwik-mishra](https://github.com/rithwik-mishra)

## 🙏 Acknowledgments

- Built with [Angular](https://angular.io/) and [Angular Material](https://material.angular.io/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- Deployed on [Vercel](https://vercel.com/) and [Render](https://render.com/)
- AI summarization powered by [HuggingFace](https://huggingface.co/)

---

**BriefNews** - Making news consumption smarter, one summary at a time. 📰✨
