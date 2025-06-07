import pytest

from NewsApp.models import CustomUser, Article, Source
from NewsApp.utils import add_to_db, cosine_similarity, process_title, init_biases
from django.utils import timezone


@pytest.mark.django_db
def test_user_create():
    # check that if custom_user is created that user is present in database
    CustomUser.objects.create_user('username', 'email@validemail.com', 'password123!')
    assert CustomUser.objects.count() == 1

def test_process_title():
    # check lemmatizing and stop word removal, with article title in format "title - news source"
    title = "a the an and it birds and the rocks and the trees- BBC"
    assert process_title(title) == '["bird", "rock", "tree"]'

def test_matching():
    # check that cosine similarity between unrelated variables should give 0
    similarity = cosine_similarity('["unrelated", "sentence", "number", "one"]', '["non-related","phrase","two"]')
    assert similarity == 0.0

@pytest.mark.django_db
def test_add_to_db():
    # test that API results are added to database properly
    # test that API results with bad parameters are NOT added to database (e.g. no source name)
    mock_json_response = {
        "articles":
        [
            {
            "source":{"name":"BBC News"},
                "author":"Anonymous",
                "title":"Some title",
                "description":"Some description",
                "url":"https://",
                "urlToImage":"https://",
                "publishedAt":timezone.now(),
                "content":"Some content"
            }
        ]
    }
    add_to_db(mock_json_response)
    assert Article.objects.filter(title="Some title").exists()

test_sources = [
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

@pytest.mark.django_db
@pytest.mark.parametrize("name, bias", test_sources)
def test_init_db(name, bias):
    # Clear ALL sources in DB
    delete_sources = Source.objects.all()
    delete_sources.delete()

    # Populate DB
    init_biases()

    # Assert that ALL of the proper sources have been created and exist in the DB
    assert Source.objects.filter(name=name,bias=bias).exists()
