"""Serendib Bank FAQ assistant — a minimal chat app on Microsoft Foundry.

Microsoft Foundry Fundamentals · Day 1 · Dialog Enterprise
Serendib Bank is fictional.

1. pip install -r requirements.txt
2. Copy .env.example to .env and fill it in (works the same on Windows, macOS and Linux)
3. Sign in:  az login      (skip if you use the API-key option in .env)
4. python chat_app.py
"""

import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()
logging.getLogger("azure").setLevel(logging.CRITICAL)  # hide SDK log noise; we print friendly errors instead

MODEL = os.getenv("FOUNDRY_MODEL", "gpt-5.4-mini")  # your deployment name

SYSTEM_MESSAGE = """You are the customer assistant for Serendib Bank, a Sri Lankan bank.

Rules:
1. Answer only questions about Serendib Bank products and services:
   accounts, cards, online banking, branches and opening hours.
2. Reply in the customer's language: Sinhala, Tamil or English.
3. Be short and friendly: at most 4 sentences.
4. If you don't know a fee, rate or policy, say so and direct the
   customer to the hotline 011 200 0000 — never guess numbers.
5. Never ask for or repeat passwords, PINs, OTPs or full card numbers."""


def make_client():
    """Option A (recommended): project endpoint + your Azure sign-in (Entra ID, no keys).
    Option B (quick demo fallback): resource endpoint + API key."""
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    if api_key:
        from openai import OpenAI

        resource = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip().rstrip("/")
        if not resource:
            sys.exit("Set AZURE_OPENAI_ENDPOINT (e.g. https://<resource>.openai.azure.com) in .env")
        print("Using API key (demo mode). For real apps use Entra ID.\n")
        return OpenAI(base_url=f"{resource}/openai/v1/", api_key=api_key)

    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "").strip()
    if not endpoint:
        sys.exit("Set FOUNDRY_PROJECT_ENDPOINT in .env (copy it from your project's Overview page in ai.azure.com).")
    if "/api/projects/" not in endpoint:
        sys.exit("FOUNDRY_PROJECT_ENDPOINT should look like https://<resource>.services.ai.azure.com/api/projects/<project>"
                 " — use the PROJECT endpoint from the project's Overview page.")
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    return project.get_openai_client()


def explain(error: Exception) -> str:
    text = str(error)
    name = type(error).__name__
    if "CredentialUnavailable" in name or "DefaultAzureCredential failed" in text or "az login" in text:
        return "Not signed in. Run `az login` (use the account that owns the Foundry project) and try again."
    if "401" in text or "403" in text or "PermissionDenied" in text or "AuthenticationError" in name:
        return ("Signed in, but not allowed. Give your account the 'Azure AI User' (Foundry User) role on the project "
                "(Azure portal → your Foundry resource → Access control (IAM)), wait 5 minutes and retry. "
                "Or use the API-key option in .env for the demo.")
    if "404" in text or "DeploymentNotFound" in text or "model" in text.lower() and "not found" in text.lower():
        return f"Model deployment '{MODEL}' not found. Set FOUNDRY_MODEL to the deployment NAME shown under Models."
    if "getaddrinfo" in text or "ConnectError" in name or "Connection" in name:
        return "Can't reach the endpoint. Check the URL in .env and your network/VPN."
    return f"{name}: {text[:300]}"


def main() -> None:
    client = make_client()
    print("Serendib Bank assistant — type your question (empty line to quit)\n")
    previous_id = None
    while question := input("You: ").strip():
        extra = {"previous_response_id": previous_id} if previous_id else {}  # keeps the conversation going
        try:
            response = client.responses.create(model=MODEL, instructions=SYSTEM_MESSAGE, input=question, **extra)
        except Exception as error:  # noqa: BLE001 — show a friendly fix instead of a stack trace
            print(f"\n⚠️  {explain(error)}\n")
            continue
        previous_id = response.id
        print(f"Assistant: {response.output_text}")
        print(f"   [{response.usage.input_tokens} in / {response.usage.output_tokens} out tokens]\n")


if __name__ == "__main__":
    main()
