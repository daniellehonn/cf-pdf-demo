import os
import requests
import tiktoken
from openai import OpenAI
import google.generativeai as genai
from groq import Groq

from model_hub.config import PRICING, SYSTEM_MESSAGE, USER_MESSAGE, GROQ_LLAMA_MODEL_FULLNAME

def calculate_price(token_counts, model):
    input_token_count = token_counts.get("input_tokens", 0)
    output_token_count = token_counts.get("output_tokens", 0)
    
    # Calculate the costs
    input_cost = input_token_count * PRICING[model]["input"]
    output_cost = output_token_count * PRICING[model]["output"]
    total_cost = input_cost + output_cost
    
    return input_token_count, output_token_count, total_cost


def trim_to_token_limit(text, model, max_tokens=120000):
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    if len(tokens) > max_tokens:
        trimmed_text = encoder.decode(tokens[:max_tokens])
        return trimmed_text
    return text


def ask_pdf(data, selected_model):
    token_counts = {}
    
    if selected_model in ["gpt-4o-mini", "gpt-4o-2024-08-06"]:
        # Use OpenAI API
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": USER_MESSAGE.format(context=data["context"], query=data["query"])},
            ],
            stream=False
        )
        return response.choices[0].message.content

    elif selected_model == "gemini-1.5-flash":
        # Use Google Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        api_key = os.getenv("GOOGLE_API_KEY")
                
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = SYSTEM_MESSAGE + "\n" + USER_MESSAGE.format(context=data["context"], query=data["query"])
        completion = model.generate_content(prompt)

        return completion.text
    
    # elif selected_model == "Llama3.1 8B":
    #     # Point to the local server
    #     payload = {
    #         "model": 'llama3.1',
    #         "messages": [
    #             {"role": "system", "content": SYSTEM_MESSAGE},
    #             {"role": "user", "content": USER_MESSAGE.format(context=data["context"], query=data["query"])}
    #         ],
    #         "temperature": 0.7
    #     }
    #     response = requests.post('http://localhost:11434/api/chat', json=payload)
    #     completion = response.json()

    #     # Extract the content from the response
    #     response_content = completion
    #     return response_content
    
    elif selected_model== "Groq Llama3.1 70b":
        api_key = os.getenv("GROQ_API_KEY")        

        # Point to the local server
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

        completion = client.chat.completions.create(
            messages=[
                {"role": "system","content": SYSTEM_MESSAGE},
                {"role": "user","content": USER_MESSAGE.format(context=data["context"], query=data["query"])}
            ],
            model=GROQ_LLAMA_MODEL_FULLNAME,
        )

        # Extract the content from the response
        response_content = completion.choices[0].message.content
        
        return response_content
    
    else:
        raise ValueError(f"Unsupported model: {selected_model}")