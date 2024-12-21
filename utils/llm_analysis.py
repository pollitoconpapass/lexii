import os
from collections import deque
from dotenv import load_dotenv
from openai import AzureOpenAI


load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# === AZURE CONFIG ====
az_client = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_DEPLOYMENT")
)

chunks_list = []
chunks_history = deque(maxlen=3)

def azure_chunk_analysis_4_translation(text: str):
    chunks_list.append(text)
    context_chunks = ', '.join(chunks_history)

    response = az_client.chat.completions.create(
        model="gpt4-o",
        messages=[
            {"role": "assistant", "content": f"""You will analyze the given chunk of a Quechua-to-Spanish dictionary. 
                Instructions:
                1. Extract each Quechua word and its primary Spanish translation(s).
                2. Ignore symbols like `.`, `:`, `-`, or `=` that separate the words and translations.
                3. Only include the Quechua word and its primary translation into Spanish, formatted as:
                    word: translation
                    word: translation

                Return only the output in this format. Do not explain your reasoning or provide definitions in any other language. 

                The chunk is: {text}
                Consider these relevant contexts from previous chunks to resolve splits:
                {context_chunks}
                """
            }
        ]
    )

    return response.choices[0].message.content


def parse_llm_output(response_text):
    lines = response_text.strip().split('\n')
    results = []
    
    for line in lines:
        if ':' in line: 
            word, translation = map(str.strip, line.split(':', 1))
            results.append({"word": word, "translation": translation})

    return results
    