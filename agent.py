from tavily import TavilyClient
from mistralai.client import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
mistral = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def search(topic):
    results = tavily.search(topic, max_results=3, include_raw_content=False)
    return results["results"]

def summarize(topic, search_results):
    content = "\n\n".join([f"Source: {r['url']}\n{r['content']}" for r in search_results])
    
    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": f"You are a research assistant. Summarize what you know about '{topic}' based on these sources:\n\n{content}\n\nWrite a clear, structured summary."
        }]
    )
    return response.choices[0].message.content

def save(topic, summary, mode="w"):
    filename = topic.replace(" ", "_") + ".md"
    with open(filename, mode, encoding="utf-8") as f:
        f.write(f"# Research: {topic}\n\n")
        f.write(summary)
    print(f"Saved to {filename}")

def get_follow_up_query(summary):
    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": f"Based on this summary:\n\n{summary}\n\nWhat is one thing still unclear? Reply with only a short search query, nothing else."
        }]
    )
    return response.choices[0].message.content

# Run the agent
topic = input("What topic do you want to research? ")
print("Searching...")
results = search(topic)
print("Summarizing...")
summary = summarize(topic, results)
save(topic, summary)
print(summary)
next_query = get_follow_up_query(summary)
more_results = search(next_query)
next_summary = summarize(next_query, more_results)
save(next_query, next_summary, mode="a")