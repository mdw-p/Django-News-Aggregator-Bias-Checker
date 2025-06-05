<h1>News Aggregator + Bias Checker</h1>
This repo is for a News Aggregator + Bias Checker using Python, Django, NewsAPI to get articles and Sci-kit-learn for NLP.

In order to run this program you will need to create a MySQL server, then a .env file with the following paramters in it:
```
DB_NAME=Name of MySQL database you have created
DB_USER=Username for MySQL database you have created
DB_PASSWORD=Password for MySQL database you have created
DB_HOST=localhost
DB_PORT=3306

NEWS_API_KEY= Valid API Key for NewsAPI
```
Put this .env file in the OUTSIDE AggregatorSite Folder - folder structure should look like this:
```
AgreggatorSite/
      -> AggregatorSite/
      -> NewsApp/
      -> templates/
      -> .env
      -> manage.py
```

Commands to install:
```
pip install requirements.txt
```
Then, from the terminal:

```
import nltk

nltk.download('stopwords')

nltk.download('punkt')

cd AggregatorSite

python manage.py flush
```
Then, enter yes:

Then, enter in the terminal:
```
python manage.py shell
```
Then, in the shell:
```
from NewsApp.utils import init_biases

init_biases()

quit()
```
Finally, to run the program:
```
python manage.py runserver
```
Then go to /localhost/NewsApp/Headlines
