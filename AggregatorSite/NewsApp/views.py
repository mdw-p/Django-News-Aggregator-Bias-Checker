from datetime import timedelta
from django.shortcuts import redirect, render
from django.utils import timezone
from NewsApp.models import Article
from .fetch_metadata import FetchMetadata
from .utils import check_data_age, retrieve_more_articles, add_to_db, cosine_similarity
import requests

#NEWSAPI KEY: 4de368a777034a8185905d81529e4d4c
#Bitcoin EXAMPLE: GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=4de368a777034a8185905d81529e4d4c

# Make sure all functions follow my_func convention, all classes MyClass, all modules

def index(request):
    return redirect("render_articles",request=request)

def render_articles(request):
    # check age of FetchMetadata: (find method that allows for first use)
    retrieve_more_articles()
    
    headlines = Article.objects.all()
    return render(request,"draft.html",context={"articles":headlines,"title":"Today's Headlines"})


def generate_bias_view(request, id):
    # generate articles dictionary with all relevant biases
    articles = {"unknown":[],
                "far_left":[],
                "left":[],
                "centre_left":[],
                "centre":[],
                "centre_right":[],
                "right":[],
                "far_right":[]}
    # pull in all articles
    original_article = Article.objects.get(id=id)
    all_articles = Article.objects.all()

    # compare against our main article using cosine matching (0.2 is temporary testing variable)
    for article in all_articles:
        if cosine_similarity(article.processed_title, original_article.processed_title) > 0.2:
            if article.source.bias == 0:
                articles["unknown"].append(article)
            if article.source.bias == 1:
                articles["far_left"].append(article)
            if article.source.bias == 2:
                articles["left"].append(article)
            if article.source.bias == 3:
                articles["centre_left"].append(article)
            if article.source.bias == 4:
                articles["centre"].append(article) 
            if article.source.bias == 5:
                articles["centre_right"].append(article)
            if article.source.bias == 6:
                articles["right"].append(article)
            if article.source.bias == 7:
                articles["far_right"].append(article)

    bias_dict = {0:"unknown",
                1:"far_left",
                2:"left",
                3:"centre_left",
                4:"centre",
                5:"centre_right",
                6:"right",
                7:"far_right"}
    
    original_bias = bias_dict[original_article.source.bias]
    # if above a certain threshold (currently 0.2) assume same topic: 
    return render(request,"bias.html",context={"articles":articles,
                                               "title":f"Bias Check for '{original_article.title[0:10]}...'",
                                               "original_article":original_article,
                                               "original_bias": original_bias})

