from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from transformers import BitsAndBytesConfig
import torch


MODEL_NAME = "IlyaGusev/saiga_llama3_8b"
DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."

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

model.save_pretrained("../saved_model")
tokenizer.save_pretrained("../saved_model")