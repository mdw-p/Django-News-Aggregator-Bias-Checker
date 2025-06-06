<h1>News Aggregator + Bias Checker</h1>
This repo is for a News Aggregator + Bias Checker using Python, Django, NewsAPI to get articles and Sci-kit-learn for NLP.

In order to run this program you will need to create a MySQL server, then create a database.

1. Clone repo

2. In the MySQL workbench, type the following command:
```
CREATE DATABASE dbname CHARACTER SET utf8mb4;
```
3. Then create a .env file with the following paramters in it:
```
DB_NAME=Name of MySQL database you have created
DB_USER=Username for MySQL database you have created
DB_PASSWORD=Password for MySQL database you have created
DB_HOST=localhost
DB_PORT=3306

NEWS_API_KEY= Valid API Key for NewsAPI
```
You can get a NewsAPI key for free, from: https://newsapi.org/register

5. Put this .env file in the OUTSIDE AggregatorSite Folder - folder structure should look like this:
```
AgreggatorSite/
      -> AggregatorSite/
      -> NewsApp/
      -> templates/
      -> .env
      -> manage.py
```

6. Commands to install:
```
pip install -r requirements.txt
```
7. Then, from the terminal, install dependencies for NLTK (language processing):

```
import nltk

nltk.download('stopwords')

nltk.download('punkt')

cd AggregatorSite
```
8. Set up database

Make sure you are in the following folder - the OUTER AggregatorSite folder:
```
*** AgreggatorSite/ ***
      -> AggregatorSite/
      -> NewsApp/
      -> templates/
      -> .env
      -> manage.py
```
Then, in the terminal run
```
python manage.py makemigrations
python manage.py migrate
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
9. Finally, to run the program, enter in the shell:
```
python manage.py runserver
```
Then go to /localhost/NewsApp/Headlines
