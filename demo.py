from summarizer import summarize, get_best_llm_open_ai
import os
from dotenv import load_dotenv
import time

load_dotenv()
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')

if __name__ == "__main__":
  llm = get_best_llm_open_ai(OPEN_AI_KEY)
  urls = [
    "https://www.bbc.com/news/technology-65886125"
  ]
  for url in urls:
    print(f"Summarizing the page at {url}...")
    start_time = time.time()
    result = summarize(url, llm)
    end_time = time.time()
    title = result["title"]
    summary = result["summary"]
    print(f'''Title: {title}
Summary:
{summary}
Time: {end_time - start_time} seconds''')
  print("All done!")
