import requests

prompt = "Explícame brevemente qué es la fotosíntesis."

r = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.2:1b", "prompt": prompt}
)

respuesta = ""
for chunk in r.iter_lines():
    if chunk:
        respuesta += chunk.decode("utf-8")

print("Respuesta de LLaMA:", respuesta)
