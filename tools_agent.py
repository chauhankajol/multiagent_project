from langchain_core.tools import tool
import requests # to access the other website by api keys
from tavily import TavilyClient
from bs4 import BeautifulSoup #its a library of paython
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import os
from rich import print

load_dotenv()

tavily_client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """ search on the web  the relatable and recent topic . Return Titles ,URL """
    result = tavily_client.search(
        query=query,
        max_results=5
    )
    out=[]
    for r in result["results"]:
     out.append(
        f"title: {r['title']}\n"
        f"URL: {r['url']}\n"
        f"content: {r['content'][:300]}"
    )

    return "\n------\n".join(out)

@tool
def scaraper_content(url:str)-> str:
    """it scrape the  content from url for the deeper reading of content"""
    try:
        response= requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup=BeautifulSoup(response.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()

        text=soup.get_text(# get text will get the text  from html by beautiful soap
        separator=" ", # where need to be space its make space
        strip=True #unnecessary space ko hatata h
        )
        return text[:10000]     
    except Exception as e:
      return f"scrapping error {str(e)}"
  
# print(scaraper_content.invoke('https://www.cnbc.com/world-politics'))


  



 