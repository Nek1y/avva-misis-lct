from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch
import uvicorn
from transformers import BitsAndBytesConfig

# Название модели и системный запрос
MODEL_NAME = "IlyaGusev/saiga_llama3_8b"
DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."

# Проверка наличия GPU
if torch.cuda.is_available():
    quantization_config = BitsAndBytesConfig(load_in_8bit=True)
    device = torch.device("cuda")
else:
    quantization_config = None
    device = torch.device("cpu")

# Загрузка модели и токенизатора
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

# Определение структуры запроса
class GenerateRequest(BaseModel):
    text: str

app = FastAPI()

@app.post("/generate/")
async def generate(request: GenerateRequest):
    try:
        query = f'{request.text}'
        
        prompt = tokenizer.apply_chat_template([{
            "role": "system",
            "content": DEFAULT_SYSTEM_PROMPT
        }, {
            "role": "user",
            "content": query
        }], tokenize=False, add_generation_prompt=True)
        
        data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
        data = {k: v.to(model.device) for k, v in data.items()}
        
        output_ids = model.generate(**data, generation_config=generation_config)[0]
        output_ids = output_ids[len(data["input_ids"][0]):]
        output = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
        
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hugging Face Model API"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()