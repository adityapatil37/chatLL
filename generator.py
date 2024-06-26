import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Check if GPU is available, otherwise use CPU
device_map = "cuda" if torch.cuda.is_available() else "cpu"

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('my-modle-train-3', device=device_map)
tokenizer = GPT2Tokenizer.from_pretrained('my-modle-train-3')

# Function to generate reply
def generate_reply(prompt, max_length=1000, temperature=7.5):
    prompt = prompt.replace("<s>", "").replace("<\s>", "").replace("[INST]", "User:").replace("[\INST]", "\nStranger:")
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device_map)

    output = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        num_beams=4,
        no_repeat_ngram_size=1,
        early_stopping=True,
        temperature=temperature,
    )

    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    print("System Reply:", reply)

    reply = reply.split("\n")[-1][9:]
    return reply












# import torch
# from transformers import AutoModelForCausalLM, GPT2Tokenizer, GPT2LMHeadModel

# device_map ="cpu"

# model = GPT2LMHeadModel.from_pretrained('my-modle-train-3', device_map=device_map)
# tokenizer = GPT2Tokenizer.from_pretrained('my-modle-train-3')

# def generate_reply(prompt, max_length=1000, temperature=7.5):
#   prompt=prompt.replace("<s>", "")
#   prompt=prompt.replace("<\s>", "")
#   prompt=prompt.replace("[INST]", "User:")
#   prompt=prompt.replace("[\INST]", "\nStranger:")

#   input_ids = tokenizer.encode(prompt, return_tensors="pt")

#   # Generate text using beam search for better coherence (optional, adjust parameters as needed)
#   output = model.generate(
#       input_ids=input_ids,
#       max_length=max_length,
#       num_beams=4,  # Adjust beam size for more or less coherence
#       no_repeat_ngram_size=1,  # Prevent repetition of short sequences
#       early_stopping=True,
#       temperature=temperature,
#   )

#   # Decode the generated IDs into text
#   reply = tokenizer.decode(output[0], skip_special_tokens=True)
#   print("system_reply ", reply)

#   reply=reply.split("\n")[-1]
#   reply=reply[9:]

#   return reply


"""
prompt = "User: How would you like to get fucked by me ? explain \nStranger:"


reply = generate_reply(prompt, max_length=len(prompt))
reply=reply.replace("I don't know what you're talking about, but", "")


print(reply)"""