"""Serendib Bank FAQ assistant — a minimal chat app on Microsoft Foundry.

Microsoft Foundry Fundamentals · Day 1 · Dialog Enterprise
Serendib Bank is fictional.

Setup:
    pip install azure-ai-projects azure-identity
    az login
    set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL (see the try-it kit)
Run:
    python chat_app.py
"""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]  # https://<resource>.services.ai.azure.com/api/projects/<project>
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5.4-mini")  # your deployment name

SYSTEM_MESSAGE = """You are the customer assistant for Serendib Bank, a Sri Lankan bank.

Rules:
1. Answer only questions about Serendib Bank products and services:
   accounts, cards, online banking, branches and opening hours.
2. Reply in the customer's language: Sinhala, Tamil or English.
3. Be short and friendly: at most 4 sentences.
4. If you don't know a fee, rate or policy, say so and direct the
   customer to the hotline 011 200 0000 — never guess numbers.
5. Never ask for or repeat passwords, PINs, OTPs or full card numbers."""


def main() -> None:
    project = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    client = project.get_openai_client()

    print("Serendib Bank assistant — type your question (empty line to quit)\n")
    previous_id = None
    while question := input("You: ").strip():
        extra = {"previous_response_id": previous_id} if previous_id else {}  # keeps the conversation going
        response = client.responses.create(model=MODEL, instructions=SYSTEM_MESSAGE, input=question, **extra)
        previous_id = response.id
        print(f"Assistant: {response.output_text}")
        print(f"   [{response.usage.input_tokens} in / {response.usage.output_tokens} out tokens]\n")


if __name__ == "__main__":
    main()
