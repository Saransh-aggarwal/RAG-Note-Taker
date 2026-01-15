# RAG Note Taker

A powerful Django-based application that combines RAG (Retrieval-Augmented Generation) capabilities with a robust note-taking system. This application allows users to upload documents, chat with them using Google's Gemini 2.5 Flash model, and seamlessley take notes within the same interface.

## Features

- **RAG Chatbot**: Chat with your documents (PDF, DOCX, TXT) using advanced AI.
- **Document Management**: Upload and index documents for semantic search (ChromaDB).
- **Smart Note Taking**: Create, edit, and organize notes.
- **User Authentication**: Secure login and registration system.
- **Responsive Design**: Modern UI with dark/light themes.

## Tech Stack

- **Backend**: Django, Python
- **AI/ML**: Google Gemini 2.5 Flash, Haystack, ChromaDB, Sentence Transformers
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (Dev), PostgreSQL (Prod ready)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Saransh-aggarwal/RAG-Note-Taker.git
   cd RAG-Note-Taker
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory with the following variables:
   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

## Screenshots

### Login Page
![Login Page](Screenshot/Login.png)

### Documents Management
![Document Management](Screenshot/Document.png)

### RAG Chat Interface
![Chat Interface](Screenshot/Chat.png)

### Note Taking
![Notes](Screenshot/Notes.png)
