import re
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from docx import Document
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import string

# Handle SSL certificate issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data with SSL handling
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt')
    except:
        pass

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('stopwords')
    except:
        pass

# Initialize NLTK components with fallback
try:
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    NLTK_AVAILABLE = True
except:
    # Fallback if NLTK data is not available
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'])
    stemmer = None
    NLTK_AVAILABLE = False

# Comprehensive database of reference sources for plagiarism detection
REFERENCE_SOURCES = [
    {
        "text": "Artificial intelligence is transforming the way we work and live. Machine learning algorithms can process vast amounts of data to identify patterns and make predictions. Deep learning networks are particularly effective at recognizing complex patterns in images, speech, and text.",
        "url": "https://example-tech-blog.com/ai-transformation",
        "domain": "technology"
    },
    {
        "text": "Climate change is one of the most pressing issues of our time. Rising global temperatures are causing ice caps to melt and sea levels to rise. The greenhouse effect, primarily caused by carbon dioxide emissions, is accelerating these changes.",
        "url": "https://example-science-journal.com/climate-change",
        "domain": "environment"
    },
    {
        "text": "The importance of education cannot be overstated. Quality education provides individuals with the knowledge and skills necessary to succeed in life. Educational institutions play a crucial role in developing critical thinking and problem-solving abilities.",
        "url": "https://example-education-site.com/importance-education",
        "domain": "education"
    },
    {
        "text": "Social media has revolutionized communication and information sharing. Platforms like Facebook, Twitter, and Instagram connect billions of people worldwide. However, these platforms also raise concerns about privacy, misinformation, and mental health impacts.",
        "url": "https://example-social-media-research.com/revolution",
        "domain": "social_media"
    },
    {
        "text": "Renewable energy sources such as solar and wind power are becoming increasingly important as we seek to reduce our dependence on fossil fuels. Solar panels convert sunlight into electricity, while wind turbines harness wind energy to generate power.",
        "url": "https://example-energy-news.com/renewable-sources",
        "domain": "energy"
    },
    {
        "text": "The human brain is one of the most complex organs in the body. It contains billions of neurons that work together to process information and control behavior. Neuroscience research continues to uncover the mysteries of brain function and consciousness.",
        "url": "https://example-neuroscience-journal.com/brain-complexity",
        "domain": "neuroscience"
    },
    {
        "text": "Economic inequality has been rising in many countries around the world. This trend has significant implications for social stability and economic growth. Factors contributing to inequality include technological change, globalization, and policy decisions.",
        "url": "https://example-economics-review.com/inequality",
        "domain": "economics"
    },
    {
        "text": "Technology has transformed the healthcare industry. Electronic health records, telemedicine, and AI-powered diagnostics are improving patient care. Wearable devices can monitor vital signs and detect health issues early.",
        "url": "https://example-health-tech.com/transformation",
        "domain": "healthcare"
    },
    {
        "text": "Data science is a multidisciplinary field that combines statistics, computer science, and domain expertise to extract insights from data. Data scientists use various tools and techniques including machine learning, data visualization, and statistical analysis.",
        "url": "https://example-data-science.com/overview",
        "domain": "data_science"
    },
    {
        "text": "Cybersecurity is becoming increasingly important as our reliance on digital systems grows. Cyber attacks can target individuals, businesses, and governments, potentially causing significant financial and operational damage. Strong security measures are essential.",
        "url": "https://example-cybersecurity.com/importance",
        "domain": "cybersecurity"
    },
    {
        "text": "Quantum computing represents a revolutionary approach to computation that could solve problems currently intractable for classical computers. Quantum bits or qubits can exist in multiple states simultaneously, enabling parallel processing capabilities.",
        "url": "https://example-quantum.com/computing",
        "domain": "quantum_computing"
    },
    {
        "text": "Blockchain technology provides a decentralized and secure way to record transactions. Originally developed for cryptocurrencies, blockchain has applications in supply chain management, voting systems, and digital identity verification.",
        "url": "https://example-blockchain.com/technology",
        "domain": "blockchain"
    },
    {
        "text": "Space exploration continues to push the boundaries of human knowledge and capability. Recent missions to Mars, the development of reusable rockets, and plans for lunar bases represent significant advances in space technology.",
        "url": "https://example-space.com/exploration",
        "domain": "space"
    },
    {
        "text": "Biotechnology is revolutionizing medicine and agriculture. Gene editing technologies like CRISPR allow precise modifications to DNA, potentially curing genetic diseases and improving crop yields. However, ethical considerations must be carefully addressed.",
        "url": "https://example-biotech.com/revolution",
        "domain": "biotechnology"
    },
    {
        "text": "The Internet of Things (IoT) connects everyday objects to the internet, enabling smart homes, cities, and industries. IoT devices can collect and share data, automate processes, and improve efficiency across various sectors.",
        "url": "https://example-iot.com/overview",
        "domain": "iot"
    },
    {
        "text": "Project management is essential for successful completion of any initiative. It involves planning, organizing, and managing resources to achieve specific goals. Effective project management includes defining scope, setting timelines, allocating resources, and monitoring progress.",
        "url": "https://example-project-management.com/basics",
        "domain": "project_management"
    },
    {
        "text": "Research methodology is the systematic approach to conducting research. It includes defining research questions, selecting appropriate methods, collecting and analyzing data, and drawing conclusions. Both qualitative and quantitative methods have their place in research.",
        "url": "https://example-research.com/methodology",
        "domain": "research"
    },
    {
        "text": "Software development lifecycle involves several phases including requirements gathering, design, implementation, testing, and maintenance. Agile methodologies have become popular for their iterative approach and flexibility in adapting to changing requirements.",
        "url": "https://example-software.com/development",
        "domain": "software_development"
    },
    {
        "text": "Database management systems are crucial for storing and retrieving data efficiently. Relational databases use structured query language (SQL) for data manipulation. NoSQL databases offer flexibility for handling unstructured data and scaling horizontally.",
        "url": "https://example-database.com/management",
        "domain": "database"
    },
    {
        "text": "Machine learning algorithms can be categorized into supervised, unsupervised, and reinforcement learning. Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data. Common algorithms include linear regression, decision trees, and neural networks.",
        "url": "https://example-ml.com/algorithms",
        "domain": "machine_learning"
    }
]


def extract_text_from_file(file):
    """
    Extract text from uploaded file (.txt or .docx)
    """
    try:
        if file.name.endswith('.txt'):
            return file.read().decode('utf-8')
        elif file.name.endswith('.docx'):
            doc = Document(file)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")


def advanced_text_preprocessing(text):
    """
    Balanced text preprocessing that preserves meaningful content
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove only excessive punctuation, keep some for context
    text = re.sub(r'[^\w\s\.\,\!\?]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # For TF-IDF, we want to preserve more content, so less aggressive filtering
    # Only remove very common stop words, keep meaningful words
    if NLTK_AVAILABLE:
        tokens = word_tokenize(text)
    else:
        tokens = text.split()
    
    # Less aggressive filtering - only remove very short words and most common stop words
    common_stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    processed_tokens = []
    
    for token in tokens:
        # Keep words that are longer than 2 characters and not in common stop words
        if len(token) > 2 and token not in common_stop_words:
            if stemmer and NLTK_AVAILABLE:
                stemmed_token = stemmer.stem(token)
                processed_tokens.append(stemmed_token)
            else:
                processed_tokens.append(token)
        elif len(token) > 4:  # Keep longer words even if they're stop words
            processed_tokens.append(token)
    
    return ' '.join(processed_tokens)


def create_text_fingerprint(text):
    """
    Create a consistent fingerprint for text to ensure reproducible results
    """
    # Normalize text for fingerprinting
    normalized = advanced_text_preprocessing(text)
    # Create hash for consistent identification
    return hashlib.md5(normalized.encode()).hexdigest()


def calculate_semantic_similarity(text1, text2):
    """
    Calculate semantic similarity using TF-IDF with robust error handling
    """
    try:
        if not text1 or not text2:
            return 0.0
            
        # Clean and preprocess texts
        processed_text1 = advanced_text_preprocessing(text1)
        processed_text2 = advanced_text_preprocessing(text2)
        
        if not processed_text1 or not processed_text2:
            return 0.0
        
        # If texts are too similar after preprocessing, check original similarity
        if processed_text1 == processed_text2:
            return 100.0
        
        # Use simpler TF-IDF configuration for better results
        vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),  # Include unigrams and bigrams
            max_features=1000,   # Reduced for better performance
            min_df=1,           # Keep all terms that appear at least once
            max_df=1.0,         # Keep all terms
            token_pattern=r'\b\w+\b'  # Simple word tokenization
        )
        
        # Create document corpus
        documents = [processed_text1, processed_text2]
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Check if matrix is valid
        if tfidf_matrix.shape[0] < 2:
            return 0.0
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to percentage and ensure it's a valid number
        result = float(similarity * 100)
        
        # Ensure result is within valid range
        return max(0.0, min(100.0, result))
        
    except Exception as e:
        # Fallback: simple word overlap similarity
        try:
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            if not words1 or not words2:
                return 0.0
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            return (intersection / union) * 100 if union > 0 else 0.0
        except:
            return 0.0


def detect_sentence_level_plagiarism(sentences, reference_sources, threshold=65.0):
    """
    Detect plagiarism at sentence level with improved accuracy
    """
    flagged_sentences = []
    
    for sentence in sentences:
        if len(sentence.strip()) < 20:  # Skip very short sentences
            continue
            
        max_similarity = 0
        best_match_source = None
        
        for source in reference_sources:
            # Check similarity with entire source
            similarity = calculate_semantic_similarity(sentence, source["text"])
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_source = source
            
            # Also check against individual sentences in the source
            source_sentences = sent_tokenize(source["text"])
            for source_sentence in source_sentences:
                if len(source_sentence.strip()) < 15:
                    continue
                    
                sent_similarity = calculate_semantic_similarity(sentence, source_sentence)
                if sent_similarity > max_similarity:
                    max_similarity = sent_similarity
                    best_match_source = source
        
        # Flag sentences above threshold
        if max_similarity >= threshold:
            flagged_sentences.append({
                "sentence": sentence.strip(),
                "source_url": best_match_source["url"],
                "domain": best_match_source["domain"],
                "similarity": round(max_similarity, 2)
            })
    
    return flagged_sentences


def calculate_overall_plagiarism_score(text, reference_sources):
    """
    Calculate overall plagiarism score using multiple methods
    """
    processed_text = advanced_text_preprocessing(text)
    
    if not processed_text:
        return 0.0
    
    similarities = []
    
    # Method 1: Direct comparison with each source
    for source in reference_sources:
        similarity = calculate_semantic_similarity(text, source["text"])
        similarities.append(similarity)
    
    # Method 2: Sliding window approach for longer texts
    if len(text.split()) > 50:  # For longer texts
        words = text.split()
        window_size = min(50, len(words) // 3)  # Adaptive window size
        
        for i in range(0, len(words) - window_size + 1, window_size // 2):
            window_text = ' '.join(words[i:i + window_size])
            for source in reference_sources:
                similarity = calculate_semantic_similarity(window_text, source["text"])
                similarities.append(similarity)
    
    if not similarities:
        return 0.0
    
    # Use weighted scoring: higher weight for maximum similarity
    max_similarity = max(similarities)
    avg_similarity = np.mean(similarities)
    
    # Weighted score: 70% max similarity + 30% average similarity
    overall_score = (0.7 * max_similarity) + (0.3 * avg_similarity)
    
    return min(100.0, overall_score)  # Cap at 100%


def split_into_sentences(text):
    """
    Split text into sentences with NLTK fallback
    """
    if not text:
        return []
    
    if NLTK_AVAILABLE:
        sentences = sent_tokenize(text)
    else:
        # Fallback sentence splitting
        sentences = re.split(r'[.!?]+', text)
    
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def analyze_plagiarism(text):
    """
    Main function to analyze text for plagiarism with consistent and accurate results
    """
    if not text or len(text.strip()) < 10:
        return {
            "similarity_score": 0.0,
            "flagged_sentences": [],
            "total_sentences": 0,
            "flagged_count": 0,
            "text_fingerprint": "",
            "analysis_method": "insufficient_text"
        }
    
    # Create text fingerprint for consistency
    text_fingerprint = create_text_fingerprint(text)
    
    # Split into sentences
    sentences = split_into_sentences(text)
    
    # Calculate overall plagiarism score
    overall_score = calculate_overall_plagiarism_score(text, REFERENCE_SOURCES)
    
    # Detect sentence-level plagiarism
    # Adaptive threshold based on text length and overall score
    if overall_score > 80:
        threshold = 60.0  # Lower threshold for high-risk texts
    elif overall_score > 50:
        threshold = 65.0  # Medium threshold
    else:
        threshold = 70.0  # Higher threshold for low-risk texts
    
    flagged_sentences = detect_sentence_level_plagiarism(sentences, REFERENCE_SOURCES, threshold)
    
    # Sort flagged sentences by similarity score
    flagged_sentences = sorted(flagged_sentences, key=lambda x: x["similarity"], reverse=True)
    
    # Limit to top 5 flagged sentences for clarity
    flagged_sentences = flagged_sentences[:5]
    
    # Adjust overall score based on flagged sentences
    if flagged_sentences:
        max_flagged_similarity = max(fs["similarity"] for fs in flagged_sentences)
        # If we have high-similarity flagged sentences, ensure overall score reflects this
        overall_score = max(overall_score, max_flagged_similarity * 0.9)
    
    return {
        "similarity_score": round(overall_score, 2),
        "flagged_sentences": flagged_sentences,
        "total_sentences": len(sentences),
        "flagged_count": len(flagged_sentences),
        "text_fingerprint": text_fingerprint,
        "analysis_method": "advanced_ml_tfidf"
    }


def validate_file(file):
    """
    Validate uploaded file (format and size)
    """
    # Check file extension
    allowed_extensions = ['.txt', '.docx']
    if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
        raise ValueError("Only .txt and .docx files are allowed")
    
    # Check file size (max 5MB for better analysis)
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if file.size > max_size:
        raise ValueError("File size must be less than 5MB")
    
    return True


def get_plagiarism_risk_level(score):
    """
    Categorize plagiarism risk based on similarity score
    """
    if score >= 80:
        return "Very High"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    elif score >= 20:
        return "Low"
    else:
        return "Very Low"


def generate_detailed_report(analysis_result):
    """
    Generate a detailed plagiarism analysis report
    """
    score = analysis_result["similarity_score"]
    risk_level = get_plagiarism_risk_level(score)
    
    report = {
        "overall_assessment": {
            "similarity_score": score,
            "risk_level": risk_level,
            "total_sentences": analysis_result["total_sentences"],
            "flagged_sentences": analysis_result["flagged_count"]
        },
        "detailed_findings": analysis_result["flagged_sentences"],
        "recommendations": []
    }
    
    # Add recommendations based on risk level
    if score >= 80:
        report["recommendations"] = [
            "Immediate review required - very high similarity detected",
            "Check all flagged sentences for proper citation",
            "Consider rewriting flagged content in your own words",
            "Ensure all sources are properly attributed"
        ]
    elif score >= 60:
        report["recommendations"] = [
            "Review flagged sentences for proper citation",
            "Consider paraphrasing similar content",
            "Add proper references where needed"
        ]
    elif score >= 40:
        report["recommendations"] = [
            "Review flagged content for originality",
            "Ensure proper citation practices",
            "Consider adding more original analysis"
        ]
    else:
        report["recommendations"] = [
            "Content appears to be largely original",
            "Continue following good citation practices",
            "Maintain originality in your work"
        ]
    
    return report