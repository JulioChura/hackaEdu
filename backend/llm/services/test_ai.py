from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

prompt = ChatPromptTemplate.from_template(
    "Explica brevemente qué es LangChain."
)

model = OllamaLLM(model="llama3.2:1b")

chain = prompt | model

response = chain.invoke({})

print(response)