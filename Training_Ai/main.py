from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import torch_directml
import os

# --- 1. Setup DirectML device ---
dml = torch_directml.device()
print("Using DirectML GPU:", dml)

# --- 2. Setup local cache folder for the model ---
cache_folder = os.path.join(os.getcwd(), "module")
os.makedirs(cache_folder, exist_ok=True)

# --- 3. Load tokenizer and model on GPU ---
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/DialoGPT-small", cache_dir=cache_folder
)
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/DialoGPT-small", cache_dir=cache_folder
).to(dml)

# --- 4. Initialize chat history ---
chat_history_ids = None

print("Chatbot ready! Type 'exit' to quit.")

# --- 5. Chat loop ---
while True:
    user_input = input(">> User: ")
    if user_input.lower() == "exit":
        break

    # Encode input and move to GPU
    new_user_input_ids = tokenizer.encode(
        user_input + tokenizer.eos_token,
        return_tensors="pt"
    ).to(dml)

    # Attention mask (all ones)
    attention_mask = torch.ones_like(new_user_input_ids).to(dml)

    # Append to chat history
    bot_input_ids = (
        torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        if chat_history_ids is not None else new_user_input_ids
    )
    bot_attention_mask = (
        torch.cat([torch.ones_like(chat_history_ids).to(dml), attention_mask], dim=-1)
        if chat_history_ids is not None else attention_mask
    )

    # Generate response
    chat_history_ids = model.generate(
        bot_input_ids,
        attention_mask=bot_attention_mask,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode and print response
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )
    print("DialoGPT:", response)
