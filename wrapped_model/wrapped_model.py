from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch
import uvicorn
from transformers import BitsAndBytesConfig
from bs4 import BeautifulSoup
import requests
import json

# Имя новой модели
MODEL_NAME = "IlyaGusev/saiga_llama3_8b"

if torch.cuda.is_available():
    print('GPU is working')
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)
    device = torch.device("cuda")
else:
    print('GPU isn`t working')
    quantization_config = None
    device = torch.device("cpu")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quantization_config,
    torch_dtype=torch.bfloat16 if device.type == 'cuda' else torch.float32,
    device_map="auto" if device.type == 'cuda' else None
)
model.eval()
model.to(device)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
generation_config = GenerationConfig.from_pretrained(MODEL_NAME)

class GenerateRequest(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hugging Face Model API"}

def search_query(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for g in soup.find_all('div', class_='g'):
        a_tag = g.find('a')
        if a_tag and a_tag['href']:
            links.append(a_tag['href'])
    return links[:5]

def parse_website(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

@app.post("/generate/")
async def generate(request: GenerateRequest):
    try:
        # Step 1: Generate search query
        search_prompt = f"Сформулируй релевантный запрос в поисковик по этой теме: {request.text}"
        data = tokenizer(search_prompt, return_tensors="pt", add_special_tokens=True)
        data = {k: v.to(model.device) for k, v in data.items()}
        output_ids = model.generate(**data, generation_config=generation_config)[0]
        search_query_text = tokenizer.decode(output_ids, skip_special_tokens=True).strip()

        # Step 2: Perform search and get links
        links = search_query(search_query_text)
        
        # Step 3: Parse websites
        parsed_texts = [parse_website(url) for url in links]
        
        # Step 4: Generate JSON and summary
        json_and_summary_prompts = []
        for text in parsed_texts:
            json_and_summary_prompt = f"Создай json для графика анализа информации по этому тексту: {text} Суммаризируй этот текст: {text}"
            data = tokenizer(json_and_summary_prompt, return_tensors="pt", add_special_tokens=True)
            data = {k: v.to(model.device) for k, v in data.items()}
            output_ids = model.generate(**data, generation_config=generation_config)[0]
            json_and_summary = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
            json_and_summary_prompts.append(json_and_summary)
        
        return {"output": json_and_summary_prompts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
