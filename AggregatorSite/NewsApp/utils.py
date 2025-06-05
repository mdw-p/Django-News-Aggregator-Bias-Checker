from datetime import timedelta
from pathlib import Path
from django.utils import timezone
import json
import os
from NewsApp.models import Article, Source
from .fetch_metadata import FetchMetadata
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import requests
import regex

BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, '.env'))

# CHANGE TO CJSON for FASTER IMPLEMENTATION

def add_to_db(data):
    for article in data["articles"]:
        # query for article.source.name in Source objects in db.
        try:
            # if in DB
            source = Source.objects.get(name=article["source"]["name"])
        except:
            # code to create source
            source = Source(
                name=article["source"]["name"],
                website="", # Unknown Website
                bias=0 # 0 = Unknown Bias
            )
            source.save()
        new_article = Article(
            source=source,
            source_name=article["source"]["name"],
            author=article["author"],
            title=article["title"],
            description=article["description"],
            url=article["url"],
            urlToImage=article["urlToImage"],
            publishedAt=article["publishedAt"],
            content=article["content"],
            processed_title=process_title(article["title"]),
            )
        try:
            new_article.save()
            
        # refine exception statement with type of error thrown when duplicate found
        except Exception as ex:
            #if article already in database
            print(f"{article["title"]} failed to save to DB")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

def check_data_age():
    singleton_metadata = FetchMetadata()
    return singleton_metadata.last_loaded

def retrieve_more_articles():
    URL = "https://newsapi.org/v2/everything?q='the'&apiKey=" + os.environ['NEWS_API_KEY']
    r = requests.get(url = URL)

    # extracting data in json format
    data = r.json()

    print(data)
    add_to_db(data)

def process_title(title):
    # Regular expression to delete punctuation 
    title = regex.sub(r'[^\w\s]','',title)
    # Tokenize data (split into words)
    tokenized_title = word_tokenize(title)


    # Remove stop words (e.g. a, at, the) from headlines - pre-processing step for later NLP proccessing
    # Cache stop words by making it a variable
    # Lemmatize headlines - shorten words to improve similarity.
    # e.g. Improving, improvements -> improve => Now easily compared
   
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    # check if words in stop_words
    filtered_title = [lemmatizer.lemmatize(w) for w in tokenized_title if not w.lower() in stop_words]

    #return filtered title MINUS last word, which is ALWAYS the source name in this format
    return json.dumps(filtered_title[0:-1])

def cosine_similarity(tokens_a, tokens_b):
    tokens_a = json.loads(tokens_a)
    tokens_b = json.loads(tokens_b)
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # # Your two tokenized lists
    # tokens_a = ['Middle', 'East', 'Entered', 'AI', 'Group']
    # tokens_b = ['History', 'Omega', 'Beginning', 'End', 'Time']

    # Join tokens into strings for vectorization
    doc_a = ' '.join(tokens_a)
    doc_b = ' '.join(tokens_b)

    # Use CountVectorizer to create aligned vectors
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([doc_a, doc_b])

    # Compute cosine similarity (returns a 2x2 matrix)
    similarity_matrix = cosine_similarity(X)

    # Extract similarity between doc_a and doc_b
    similarity_score = similarity_matrix[0, 1]
    return similarity_score

def copy_test():
    #just to copy and paste into terminal for testing
    # python manage.py shell
    from NewsApp.utils import retrieve_more_articles
    retrieve_more_articles()

    from NewsApp.utils import cosine_similarity
    cosine_similarity(Article.objects.get(id=1).processed_title,Article.objects.get(id=2).processed_title)
    print("Overlap:", set(Article.objects.get(id=1).processed_title) & set(Article.objects.get(id=2).processed_title))

def init_biases():
    Sources = [
    ("BBC News", 4),
    ("CNN", 2),
    ("Fox News", 6),
    ("The New York Times", 3),
    ("The Guardian", 3),
    ("Reuters", 4),
    ("Associated Press (AP)", 4),
    ("Daily Mail", 5),
    ("The Washington Post", 3),
    ("NBC News", 3),
    ("CBS News", 3),
    ("Bloomberg", 4),
    ("USA Today", 4),
    ("The Wall Street Journal", 5),
    ("Al Jazeera English", 3),
    ("HuffPost", 2),
    ("Newsweek", 4),
    ("Politico", 4),
    ("NPR", 3),
    ("The Independent", 3),
    ("Sky News", 5),
    ("The Times (UK)", 5),
    ("The Telegraph (UK)", 5),
    ("Financial Times", 4),
    ("The Economist", 4),
    ("Time", 4),
    ("The Atlantic", 3),
    ("Vox", 2),
    ("BuzzFeed News", 2),
    ("Vice News", 2),
    ("The Hill", 4),
    ("Business Insider", 4),
    ("Forbes", 4),
    ("Axios", 4),
    ("The New Yorker", 3),
    ("Slate", 2),
    ("The Intercept", 2),
    ("ProPublica", 3),
    ("The Daily Beast", 2),
    ("The Spectator", 5),
    ("The New Republic", 2),
    ("The Nation", 2),
    ("Reason", 5),
    ("The American Conservative", 6),
    ("National Review", 6),
    ("The Federalist", 6),
    ("Breitbart News", 6),
    ("Infowars", 7),
    ("One America News Network", 7),
    ("RT (Russia Today)", 1),
    ("Wired", 3),
    ("The Verge", 3),
] 
    for name, bias in Sources:
        Source.objects.create(name=name, bias=bias)