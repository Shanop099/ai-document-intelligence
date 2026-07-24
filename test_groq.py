from backend.groq_client import groq_client

response = groq_client.generate(
    "Say Hello in one sentence."
)

print(response)