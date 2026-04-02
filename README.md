# AI-based Plagiarism Analyzer

A modern web application that uses artificial intelligence to detect plagiarism in text documents and academic papers.

![Plagiarism Analyzer](https://img.shields.io/badge/AI-Plagiarism%20Detection-blue)
![Django](https://img.shields.io/badge/Django-5.2.6-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![NLTK](https://img.shields.io/badge/NLTK-AI%20Processing-orange)

## 📋 Overview

This AI-based Plagiarism Analyzer is a sophisticated tool designed to help educators, students, and content creators detect potential plagiarism in written work. The system uses natural language processing and machine learning techniques to compare submitted text against a comprehensive database of sources, providing detailed similarity reports.

### Key Features

- **Advanced Text Analysis**: Uses TF-IDF vectorization and cosine similarity to detect plagiarism
- **Document Upload Support**: Analyze text from uploaded DOCX files
- **Sentence-Level Detection**: Identifies specific sentences that may be plagiarized
- **Risk Assessment**: Categorizes plagiarism risk as Low, Medium, or High
- **User Dashboard**: Track and review previous plagiarism reports
- **Secure User Authentication**: Complete account management system

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   extract or clone the project
   cd ai-plagiarism-analyzer
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## 🔍 How It Works

1. **User Authentication**: Users create an account or log in to access the system
2. **Text Submission**: Users can either paste text directly or upload a document
3. **AI Analysis**: The system processes the text using:
   - Natural Language Processing (NLTK)
   - Text vectorization (TF-IDF)
   - Cosine similarity measurement
4. **Report Generation**: A detailed report shows:
   - Overall similarity score
   - Flagged sentences with potential sources
   - Risk level assessment

## 🏗️ Project Structure

```
ai-plagiarism-analyzer/
├── accounts/                # User authentication and management
├── analyzer/                # Core plagiarism detection functionality
│   ├── models.py            # Data models for plagiarism reports
│   ├── utils.py             # AI and NLP utilities
│   └── views.py             # View controllers
├── media/                   # User uploaded files
├── plagiarism_analyzer/     # Project settings
├── static/                  # Static assets
├── templates/               # HTML templates
│   ├── accounts/            # Authentication templates
│   ├── analyzer/            # Main application templates
│   └── base.html            # Base template
└── manage.py                # Django management script
```

## 🔧 Technologies Used

- **Backend**: Django, Python
- **AI/ML**: NLTK, scikit-learn
- **Document Processing**: python-docx
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite (development), PostgreSQL (recommended for production)

## 🛡️ Security Features

- CSRF protection
- Secure authentication system
- Input validation and sanitization
- File type validation for uploads

## 🔮 Future Enhancements

- Integration with academic databases for more comprehensive checking
- API for third-party applications
- Batch processing for multiple documents
- Improved visualization of plagiarism results
- Support for additional file formats (PDF, TXT, etc.)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- [Your Name](https://github.com/yourusername)

## 🙏 Acknowledgements

- NLTK for natural language processing capabilities
- scikit-learn for machine learning algorithms
- Django for the web framework
