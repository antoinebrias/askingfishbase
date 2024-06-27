from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import wikipediaapi

app = Flask(__name__)

# Function to get fish info from FishBase
def get_fish_info(species):
    url = f'https://www.fishbase.se/summary/{species}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Species not found or failed to fetch data"}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    info_fishbase = soup.getText()
    #print(info_fishbase)
  
    # Fetch content from Wikipedia
    #info_wikipedia = get_wikipedia_summary(species.replace('-', '_'))
    #print(info_wikipedia)
    return {
         "info": info_fishbase, #"info": info_fishbase+info_wikipedia,
    }

def get_wikipedia_summary(species):

    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=&explaintext&titles={species}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
    for page_id, page_info in pages.items():
        summary = page_info.get("extract")
        if summary:
            return summary
        intro = page_info.get("intro")
        if intro:
            return intro
    return "Wikipedia page not found for {}".format(species)



# Function to generate a summary using OpenAI GPT-3.5
def generate_summary(info):
    api_key = 'aaaaaaaaaaaa'  # Replace with your actual OpenAI API key
    client = OpenAI(
    api_key = api_key #os.getenv("OPENAI_API_KEY"),
)
    prompt = f"Generate a concise summary for the following fish information:\n\n{info}. The summary must contain all the important features and data about the species, based on the information given."

    completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )
    return completion.choices[0].text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.json
    species = data['species'].replace(' ', '-')
    
    fish_info = get_fish_info(species)
    if 'error' in fish_info:
        return jsonify(fish_info), 404

    summary = generate_summary(fish_info)
    
    fish_info['summary'] = summary

    return jsonify(fish_info)

if __name__ == '__main__':
    app.run(debug=True)

