from agent_reader import summarize, retrieve, get_model, ModelType
import os
from dotenv import load_dotenv
import time
import itertools

load_dotenv()
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

def test_retrieve(urls):
  print("Testing retrieve()...")
  for url in urls:
    print(f"Retrieving the page at {url}...")
    start_time = time.time()
    result = retrieve(url)
    end_time = time.time()
    title = result["title"]
    content = result["content"]
    print(f'''Title: {title}
Content:
{content}
Time: {end_time - start_time} seconds
\n=========================================\n''')
  print("Done testing retrieve().\n")

def test_summarize(urls, llms):
  print("Testing summarize()...")
  for url, llm in itertools.product(urls, llms):
    print(f"Summarizing the page at {url} by {llm['type']}...")
    start_time = time.time()
    result = summarize(url, llm['model'])
    end_time = time.time()
    title = result["title"]
    summary = result["summary"]
    print(f'''Title: {title}
Model: {llm['type']}
Summary:
{summary}
Time: {end_time - start_time} seconds
\n=========================================\n''')
  print("Done testing summarize().\n")

if __name__ == "__main__":
  llms = [
    {'type': ModelType.OPENAI_GPT35, 'model': get_model(ModelType.OPENAI_GPT35, OPEN_AI_KEY)},
    {'type': ModelType.OPENAI_GPT4, 'model': get_model(ModelType.OPENAI_GPT4, OPEN_AI_KEY)},
    {'type': ModelType.COHERE_L, 'model': get_model(ModelType.COHERE_L, COHERE_API_KEY)},
    {'type': ModelType.COHERE_XL, 'model': get_model(ModelType.COHERE_XL, COHERE_API_KEY)}
  ]
  urls = [
    "https://www.bbc.com/news/technology-65886125", # news article
    "https://baseten.co",                           # company website
    "https://arxiv.org/abs/2305.20050",             # research paper
    "https://openaccess.thecvf.com/content/CVPR2023/html/Ci_GFPose_Learning_3D_Human_Pose_Prior_With_Gradient_Fields_CVPR_2023_paper.html", 
    "https://github.com/hwchase17/langchain"        # github repo
  ]
  
  test_retrieve(urls)
  test_summarize(urls, llms)
  print("All done!")
