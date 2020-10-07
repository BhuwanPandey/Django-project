from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

def scrape(request):
    url = "https://www.theonion.com/"
    r=requests.get(url)
    soup = BSoup(r.content, 'html.parser')
    val=soup.find_all('article',{'class':"js_post_item"})
    for link in val:
        main=link.find('a')
        try:
            image_url=(str(main.find('img')['data-srcset']).split(" ")[0])
            new_headine=Headline()
            new_headine.image=image_url
            new_headine.url=main['href']
            new_headine.title=link.find('h4').get_text()
            new_headine.save()
        except:
            pass
    return redirect("../")

def news_list(request):
    headlines=Headline.objects.all()[::-1]
    context={
        'object_list':headlines,
    }
    return render(request,"news/home.html",context)

