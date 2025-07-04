from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from utils.env_config import get_env_variable
gemini_llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=get_env_variable("GEMINI_API_KEY"),
    max_output_tokens=1024,)

model_name = "deepseek-r1-distill-llama-70b"
llm_groq = ChatGroq(model=model_name, api_key=get_env_variable("GROQ_API_KEY"))

llm = ChatOpenAI(
        model="gpt-4o",    
        temperature=0,
        api_key=get_env_variable("OPENAI_API_KEY"), 
    )