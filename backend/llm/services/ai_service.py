from django.shortcuts import render

from langchain_core.prompts import ChatPromptTemplate
try:
    from langchain_ollama.llms import OllamaLLM
except ImportError:
    OllamaLLM = None  # type: ignore

template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llava.1")

chain = prompt | model

chain.invoke({"question": "What is LangChain?"})