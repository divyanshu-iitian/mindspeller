# Chatbot Application

A modern full-stack chatbot application with a Next.js frontend and Python Flask backend. Uses the Groq API with the powerful `llama-3.3-70b-versatile` model for intelligent responses.

## 🏗️ Project Structure

```
mindspeller/
├── backend/                    # Python Flask API
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── .env                   # Environment variables (API key)
│   ├── .gitignore
│   └── venv/                  # Virtual environment (created during setup)
│
└── frontend/                   # Next.js TypeScript application
    ├── pages/                 # Next.js pages
    │   ├── _app.tsx
    │   └── index.tsx          # Main chat page
    ├── styles/
    │   └── globals.css        # Tailwind CSS styles
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── next.config.js
    ├── .gitignore
    └── node_modules/          # (created during setup)
```

## ✨ Features

- ✅ Real-time chat interface with message history
- ✅ User messages on the right, bot responses on the left
- ✅ Loading indicator while waiting for responses
- ✅ Error handling for network and API failures
- ✅ Clean, responsive UI built with Tailwind CSS
- ✅ Python 3.7/3.8 compatible backend
- ✅ Uses `requests` library for Groq API (no official groq package)
- ✅ CORS properly configured
- ✅ Secure API key storage with `.env` file

## 🚀 Getting Started

### Prerequisites

- **Python 3.7 or 3.8** (required for compatibility)
- **Node.js 16+** (for Next.js frontend)
- **npm or yarn**
- **Groq API Key** (get it from [https://console.groq.com](https://console.groq.com))

### Backend Setup

#### 1. Create Python Virtual Environment

Using Python 3.8 (recommended):
```bash
py -3.8 -m venv venv
```

Or if you want to use Python 3.7:
```bash
py -3.7 -m venv venv
```

Or on macOS/Linux:
```bash
python3.8 -m venv venv
# or
python3 -m venv venv
```

#### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 4. Configure API Key

Open `backend/.env` and replace `your_groq_api_key_here` with your actual Groq API key:

```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**⚠️ Important:** Never commit the `.env` file to version control. The `.gitignore` is already configured to exclude it.

#### 5. Run the Backend

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

#### 1. Install Dependencies

In a new terminal (keep the backend running):
```bash
cd frontend
npm install
```

#### 2. Run the Frontend

```bash
npm run dev
```

You should see:
```
- ready started server on 0.0.0.0:3000
```

Open your browser and navigate to `http://localhost:3000`

## 🔌 API Documentation

### POST /api/chat

Send a message to the chatbot and get a response.

**Request:**
```json
{
  "message": "Hello, how are you?",
  "history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! I'm doing well, thanks for asking!"}
  ]
}
```

**Response (Success):**
```json
{
  "reply": "I'm doing great, thank you for asking! How can I help you today?",
  "history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! I'm doing well, thanks for asking!"},
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm doing great, thank you for asking! How can I help you today?"}
  ]
}
```

**Response (Error):**
```json
{
  "error": "Groq API error",
  "details": "Invalid API key",
  "status_code": 401
}
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## 🛠️ Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'flask'"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**"GROQ_API_KEY not found"**
- Check that `.env` file exists in the `backend/` directory
- Verify the API key is set correctly in `.env`

**"Connection refused" on frontend**
- Ensure backend is running on `http://localhost:5000`
- Check firewall settings
- Run `python app.py` in the backend directory

**API returns "Invalid API key"**
- Verify your Groq API key is correct
- Get a new key from [https://console.groq.com](https://console.groq.com)

### Frontend Issues

**"Cannot connect to backend"**
- Ensure backend is running: `python app.py`
- Check that backend is on `http://localhost:5000`
- Clear browser cache (Ctrl+Shift+Delete)

**Styling not loading**
- Run `npm install` in frontend directory
- Restart dev server: `npm run dev`

**Port 3000 already in use**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

## 📦 Dependencies

### Backend
- **Flask 2.2.2** - Web framework
- **Flask-CORS 3.0.10** - CORS support
- **requests 2.28.1** - HTTP library for Groq API
- **python-dotenv 0.20.0** - Environment variable management

All dependencies are compatible with Python 3.7 and 3.8.

### Frontend
- **Next.js 14** - React framework
- **React 18** - UI library
- **TypeScript 5** - Type safety
- **Tailwind CSS 3.3** - Styling
- **Axios 1.6** - HTTP client
- **PostCSS** - CSS processing

## 🔐 Security Notes

1. **Never commit `.env` file** - It contains your API key
2. **Use environment variables** in production
3. **API key in `.env` is for development only**
4. **CORS is configured** to allow requests from `http://localhost:3000`

## 🚢 Production Deployment

### Backend (Render, pinned to Python 3.8)

This project includes `backend/Dockerfile` with `python:3.8-slim` so your backend runs on Python 3.8 in production.

1. Push code to GitHub
2. Create a new **Web Service** on Render
3. Connect this repository
4. Set **Root Directory** to `backend`
5. Render will detect Docker automatically
6. Add environment variables:
  - `GROQ_API_KEY=your_real_key`
  - `FRONTEND_URL=https://your-frontend-domain.vercel.app`
7. Deploy

After deploy, test:

```bash
https://your-backend-service.onrender.com/api/health
```

### Frontend (Vercel)

1. Create a new project on Vercel and import this repo
2. Set **Root Directory** to `frontend`
3. Add env variable:

```bash
NEXT_PUBLIC_BACKEND_URL=https://your-backend-service.onrender.com
```

4. Deploy

The frontend reads backend URL from `NEXT_PUBLIC_BACKEND_URL` and falls back to `http://localhost:5000` for local development.

## 📝 Example Usage

### Starting Both Services

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # or source venv/bin/activate on macOS/Linux
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:3000` in your browser.

## ✅ Python 3.8 Compatibility Proof

This repository includes a GitHub Actions workflow at `.github/workflows/python-compatibility.yml`.

It validates backend compatibility on:
- Python 3.8
- Python 3.11

Use the GitHub **Actions** tab as cloud proof that your code works on Python 3.8 even if Python 3.8 is not installed on your local system.

## 🤖 Model Information

- **Model:** `llama-3.3-70b-versatile`
- **Provider:** Groq
- **Context Window:** Supports conversation history
- **Temperature:** 0.7 (balanced creativity and consistency)
- **Max Tokens:** 1024 per response

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Groq API Documentation](https://console.groq.com/docs)
- [Tailwind CSS](https://tailwindcss.com)

## 🐛 Reporting Issues

If you encounter issues:

1. Check the error message in the browser console (F12)
2. Check the backend terminal for error logs
3. Verify all services are running
4. Ensure API key is correct
5. Check that ports 3000 and 5000 are available

## 📄 License

This project is open source and available under the MIT License.

---

**Happy coding!** 🚀