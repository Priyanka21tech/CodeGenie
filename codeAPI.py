from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


#  modify this******

# Load API Key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("ERROR: Missing OpenAI API key. Please check your .env file.")

# Initialize FastAPI
app = FastAPI()

# Initialize AI Model
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini")

# Request Model
class CodeReq(BaseModel):
    input_text: str
    task: str  # "explain" or "generate"


async def explain_code(input_text: str, task: str) -> str:
    if task == "generate":
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert programming tutor. Your task is to generate code step-by-step in a clear and structured way and not to explain the code."),
            ("human", "Please explain the following code step-by-step:\n\n{code}")
        ])
    elif task == "explain":
        prompt = ChatPromptTemplate.from_messages([
                        ("system","You are a helpful programming tutor. Your job is to explain code to beginners clearly and step-by-step and not to generate the code if the code is not provided . "
            "Structure your response like this:\n\n"
            "1. **Overview**: A short summary of what the code does.\n"
            "2. **Line-by-line Explanation**: Explain each part in a numbered list.\n"
            "3. **Key Concepts**: Highlight any important functions, libraries, or logic used.\n\n"
            "Use markdown formatting and make the explanation easy to understand."
                        ),
            ("human", "Generate code for the following requirement:\n\n{code}")
        ])
    else:
        raise HTTPException(status_code=400, detail="Invalid task input. Use 'explain' or 'generate'.")

    formatted_prompt = prompt.format(code=input_text)

    # Run the model (optionally using run_in_executor if it's not async)
    response = llm.invoke(formatted_prompt)

    if hasattr(response, "content"):
        response = response.content.strip()
    else:
        response = str(response).strip()

    return response


# API Route
@app.post("/code", response_class=PlainTextResponse) #ensure response is plain text
async def code_process(request: CodeReq):
    if not request.input_text.strip():# if i/p is  empty
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    result = await explain_code(request.input_text, request.task)
    
    return PlainTextResponse(content=result) # returning result in plain format
