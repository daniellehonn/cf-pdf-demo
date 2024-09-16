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
    # "Llama3.1 8B": {
    #     "input": 0 ,  # Free
    #     "output": 0 , # Free
    # },
    "Groq Llama3.1 70b": {
        "input": 0 ,  # Free
        "output": 0 , # Free
    },
    # Add other models and their prices here if needed
}

GROQ_LLAMA_MODEL_FULLNAME="llama-3.1-70b-versatile"

SYSTEM_MESSAGE = """Your task is to answer user questions based on the information given above each question. Only ever use the information given, DO NOT FIND YOUR OWN INFORMATION. Say "I don't know" if the information is missing and be as detailed as possible. End each sentence with a period. Please begin."""

USER_MESSAGE = """
    Information: {context}

    User Question: {query}
"""
