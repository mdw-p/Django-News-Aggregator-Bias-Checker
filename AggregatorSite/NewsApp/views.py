from datetime import timedelta
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from NewsApp.models import Article, Source
from .utils import init_biases, retrieve_more_articles, cosine_similarity
from .fetch_metadata import FetchMetadata
from .forms import CustomUserCreationForm, SubscribeForm

from django.contrib.auth import get_user_model, logout
User = get_user_model()

#NEWSAPI KEY: ####
#Bitcoin EXAMPLE: GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=####

# Make sure all functions follow my_func convention, all classes MyClass, all modules

def render_articles(request):
    # check age of FetchMetadata: (find method that allows for first use)
    sub_form = SubscribeForm()
    metadata = FetchMetadata()
    if metadata.is_first() == True:
        # if it is the first time that server is being used - clear any leftover user data
        logout(request)
        init_biases()
        metadata.set_time()
        retrieve_more_articles()
    else:
        # check age of data - if older than 5 then refresh, if new then leave
        if (metadata.last_loaded - timezone.now()) > timedelta(minutes=1):
            #if data older than 5 mins:
            metadata.set_time()
            retrieve_more_articles()
    # get most recent 100 articles 
    headlines = Article.objects.all()[:100]
    return render(request,"headlines.html",context={"articles":headlines,"title":"Today's Headlines","sub_form":sub_form})


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

@login_required(login_url='/accounts/login')
def feed(request):
    # get current user and their saved sources
    cur_user = request.user
    sources = [source.name for source in cur_user.saved_sources.all()]

    # generate feed from top 100 articles from sources
    articles = Article.objects.all()
    articles = articles.filter(
        source_name__in=sources
    )[:100]
    return render(request, "feed.html", {"articles": articles})

@login_required(login_url='/accounts/login')
def manage_feed(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            # add to current users saved sources
            cur_user = request.user
            new_source = form.cleaned_data['new_subscription']
            if Source.objects.filter(name=new_source).exists():
                # if user not already subscribed to news source
                if new_source not in [source.name for source in cur_user.saved_sources.all()]:
                    cur_user.saved_sources.add(Source.objects.get(name=new_source))
                    cur_user.save()
        return redirect("/")
    else:
        form = SubscribeForm()
        return render(request, 'manage_feed.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required(login_url='/accounts/login')
def logout_view(request):
    logout(request)
    return redirect ("/")

