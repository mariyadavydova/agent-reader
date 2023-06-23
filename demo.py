from agent_summarizer import summarize, get_best_llm_openai, get_best_llm_cohere
import os
from dotenv import load_dotenv
import time
import itertools

load_dotenv()
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

if __name__ == "__main__":
  llms = [
    get_best_llm_openai(OPEN_AI_KEY),
    # get_best_llm_cohere(COHERE_API_KEY)   # so far this LLM is working poorly
  ]
  urls = [
    "https://www.bbc.com/news/technology-65886125", # news article
    "https://baseten.co",                           # company website
    "https://arxiv.org/abs/2305.20050",             # research paper
    "https://openaccess.thecvf.com/content/CVPR2023/html/Ci_GFPose_Learning_3D_Human_Pose_Prior_With_Gradient_Fields_CVPR_2023_paper.html", 
    "https://github.com/hwchase17/langchain"        # github repo
  ]
  for url, llm in itertools.product(urls, llms):
    print(f"Summarizing the page at {url} by {type(llm).__name__}...")
    start_time = time.time()
    result = summarize(url, llm)
    end_time = time.time()
    title = result["title"]
    summary = result["summary"]
    print(f'''Title: {title}
Summary:
{summary}
Time: {end_time - start_time} seconds
\n=========================================\n''')
  print("All done!")
