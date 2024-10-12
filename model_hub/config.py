# Define the pricing for models without Batch API
PRICING = {
    "gpt-4o-mini": {
        "input": 0.150 / 1_000_000,  # $0.150 per 1M input tokens
        "output": 0.600 / 1_000_000, # $0.600 per 1M output tokens
    },
    "gpt-4o-2024-08-06": {
        "input": 2.5 / 1_000_000,  # $2.5 per 1M input tokens
        "output": 10 / 1_000_000, # $10 per 1M output tokens
    },
    "gemini-1.5-flash": {
        "input": 0.075 / 1_000_000,  # $0.075 per 1M input tokens
        "output": 0.30 / 1_000_000, # $0.30 per 1M output tokens
    },
    "Groq Llama3.1 70b": {
        "input": 0 ,  # Free
        "output": 0 , # Free
    },
    # Add other models and their prices here if needed
}

GROQ_LLAMA_MODEL_FULLNAME="llama-3.1-70b-versatile"

USER_MESSAGE = """Your task is to answer user questions based on the context given above each question. The information is given in the following structure: 
[CONTEXT]: {context}

[QUESTION]: {query}

[OUTPUT GUIDELINES]: Use the context provided to generate your answer. You MUST quote your source with source number using this format [1], [2]... If you cannot find the answer based on the context. Simply said “N/A” instead of making it up.
"""
