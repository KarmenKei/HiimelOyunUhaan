from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "distilgpt2"

print("Loading DistilGPT-2 model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

device = "cpu"
model.to(device)
print("Model loaded.\n")

print("=== PRETRAINED MODEL OUTPUT ===\n")

prompt = "Artificial intelligence will change the future because"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

output_ids = model.generate(
    **inputs,
    max_length=80,
    do_sample=True,
    top_k=50,
    top_p=0.95
)

print("Prompt:", prompt)
print("Output:", tokenizer.decode(output_ids[0], skip_special_tokens=True))
print("\n")

prompts = [
    "What are the benefits of artificial intelligence?",
    "How will technology evolve in the next 10 years?"
]

print("=== PROMPT RESULTS ===\n")

for p in prompts:
    print("Prompt:", p)
    inputs = tokenizer(p, return_tensors="pt").to(device)

    output_ids = model.generate(
        **inputs,
        max_length=80,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print("Output:", output_text)
    print()

print("Lab 8 completed successfully!")