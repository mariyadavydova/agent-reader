import requests
from bs4 import BeautifulSoup
from enum import Enum

from langchain.llms import OpenAI, Cohere
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

from .link_type import LinkType

def get_best_llm_openai(api_key, model_name="text-davinci-003", temperature=0.5):
  return OpenAI(model=model_name, temperature=temperature, openai_api_key=api_key)

def get_best_llm_cohere(api_key, model_name="summarize-xlarge"):
  return Cohere(model=model_name, cohere_api_key=api_key)

def get_the_page_content(url):
  headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
  }
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    raise Exception(f"Failed to load {url}, status code: {response.status_code}")
  content = response.text
  soup = BeautifulSoup(content, "html.parser")
  return soup

def read_webpage_title(url):
  soup = get_the_page_content(url)
  title = soup.find('title').text.strip()
  return title

def read_webpage_content(url):
  soup = get_the_page_content(url)
  for script in soup(["script", "style"]):
    script.decompose()
  text = soup.get_text()
  return text

def read_github_title(url):
  soup = get_the_page_content(url)
  element = soup.find(id="readme")
  text = None
  if element is not None:
    h1_tag = element.find('h1')
    if h1_tag is not None:
      text = h1_tag.get_text()
  return text

def read_github_content(url):
  soup = get_the_page_content(url)
  element = soup.find(id="readme")
  text = None
  if element is not None:
    for script in element(["script", "style"]):
      script.decompose()
    text = element.get_text()
  return text

def read_arxiv_title(url):
  soup = get_the_page_content(url)
  element = soup.find('h1', attrs={'class': 'title'})
  text = None
  if element is not None:
    text = element.get_text()
  return text

def read_arxiv_content(url):
  soup = get_the_page_content(url)
  element = soup.find('blockquote', attrs={'class': 'abstract'})
  text = None
  if element is not None:
    text = element.get_text()
  return text

def read_openaccess_title(url):
  soup = get_the_page_content(url)
  element = soup.find('div', attrs={'id': 'papertitle'})
  text = None
  if element is not None:
    text = element.get_text()
  return text

def read_openaccess_content(url):
  soup = get_the_page_content(url)
  element = soup.find('div', attrs={'id': 'abstract'})
  text = None
  if element is not None:
    text = element.get_text()
  return text

def retrieve(url):
  type = LinkType.get_type_from_link(url)

  if type == LinkType.PROJECT:
    text = read_github_content(url)
    title = read_github_title(url)
  elif type == LinkType.PAPER:
    text = read_arxiv_content(url)
    title = read_arxiv_title(url)
  elif type == LinkType.OA_PAPER:
    text = read_openaccess_content(url)
    title = read_openaccess_title(url)
  else:
    text = read_webpage_content(url)
    title = read_webpage_title(url)

  return {
    "title": title.strip(),
    "content": text.strip()
  }


def summarize(url, llm):
  text_splitter = RecursiveCharacterTextSplitter()
  prompt_template = """Write a concise summary of the following text. 
  I want you to provide me with bullet points highlighting the core ideas
  of this piece. Keep each bullet point under one or two sentences.

    {text}

  Bullet points:"""
  summarizer_prompt = PromptTemplate(template=prompt_template,
                                      input_variables=["text"])
  
  result = retrieve(url)
  text = result["content"]
  title = result["title"]

  try:
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm,
                                chain_type="map_reduce",
                                map_prompt=summarizer_prompt,
                                combine_prompt=summarizer_prompt)
    summary = chain.run(docs)
    summary = "  " + summary.strip()
    return {
      "title": title,
      "summary": summary,
      "content": text
    }
  except Exception as e:
    raise Exception(f"Error while summarizing the link {url}: {e}")
