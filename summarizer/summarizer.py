import requests
from bs4 import BeautifulSoup
from enum import Enum

from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

def get_best_llm_open_ai(api_key, model_name="text-davinci-003", temperature=0.5):
  return OpenAI(model_name=model_name, temperature=temperature, openai_api_key=api_key)


def read_webpage_title(url):
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text.strip()
    return title
  except:
    raise Exception(f"Failed to load {url}, status code: {response.status_code}")


def read_webpage_context(url):
  headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
  }
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    raise Exception(f"Failed to load {url}, status code: {response.status_code}")
  content = response.text
  soup = BeautifulSoup(content, "html.parser")
  for script in soup(["script", "style"]):
    script.decompose()
  text = soup.get_text()
  return text


def summarize(url, llm):
  text_splitter = RecursiveCharacterTextSplitter()
  prompt_template = """Write a concise summary of the following text. 
  I want you to provide me with bullet points highlighting the core ideas
  of this piece. Keep each bullet point under one or two sentences.

    {text}

  Bullet points:"""
  summarizer_prompt = PromptTemplate(template=prompt_template,
                                      input_variables=["text"])

  text = read_webpage_context(url)
  title = read_webpage_title(url)

  try:
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm,
                                chain_type="map_reduce",
                                map_prompt=summarizer_prompt,
                                combine_prompt=summarizer_prompt)
    summary = chain.run(docs)
    return {
      "title": title,
      "summary": summary,
    }
  except Exception as e:
    raise Exception(f"Error while summarizing the link {url}: {e}")
