from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from NewsApp.models import Article
from .utils import retrieve_more_articles, cosine_similarity
from .fetch_metadata import FetchMetadata

#NEWSAPI KEY: ####
#Bitcoin EXAMPLE: GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=####

# Make sure all functions follow my_func convention, all classes MyClass, all modules

def render_articles(request):
    # check age of FetchMetadata: (find method that allows for first use)
    metadata = FetchMetadata()
    if metadata.is_first() == True:
        # if it is the first time that server is being used
        metadata.set_time()
        retrieve_more_articles()
    else:
        # check age of data - if older than 5 then refresh, if new then leave
        if (metadata.last_loaded - timezone.now()) > timedelta(minutes=1):
            #if data older than 5 mins:
            metadata.set_time()
            retrieve_more_articles()
    headlines = Article.objects.all()
    return render(request,"headlines.html",context={"articles":headlines,"title":"Today's Headlines"})


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

