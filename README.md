<h1>News Aggregator + Bias Checker</h1>
This repo is for a News Aggregator + Bias Checker using Python, Django, NewsAPI to get articles and Sci-kit-learn for NLP.

Commands to install:

pip install requirements.txt

Then, from the terminal:


import nltk

nltk.download('stopwords')

nltk.download('punkt')

cd AggregatorSite

python manage.py flush -> then enter yes

Then, enter in the terminal:

python manage.py shell

Then, in the shell:

from NewsApp.utils import init_biases

init_biases()

Finally, to run the program:

python manage.py runserver

Then go to /localhost/NewsApp/Headlines
