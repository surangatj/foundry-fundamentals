"""Serendib Bank home-loan agent in a few lines of Python (Microsoft Agent Framework).

Microsoft Foundry Fundamentals · Day 3 · Dialog Enterprise
Serendib Bank is fictional; numbers are indicative only.

1. pip install -r requirements.txt
2. Copy .env.example to .env and fill it in
3. az login        (skip if you use the API-key option in .env)
4. python agent_app.py
"""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()
logging.getLogger("azure").setLevel(logging.CRITICAL)
for stream in (sys.stdout, sys.stdin):  # Sinhala and Tamil on Windows consoles
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

from agent_framework import Agent, tool  # noqa: E402

MODEL = os.getenv("FOUNDRY_MODEL", "gpt-5.4-mini")


# ---------------------------------------------------------------- tools: plain Python functions
@tool(approval_mode="never_require")
def monthly_instalment(principal_lkr: float, annual_rate_percent: float, years: int) -> str:
    """Calculate the monthly instalment of a loan with the standard amortisation formula."""
    r, n = annual_rate_percent / 1200, years * 12
    instalment = principal_lkr * r * (1 + r) ** n / ((1 + r) ** n - 1)
    print(f"   🔧 tool: monthly_instalment({principal_lkr:,.0f}, {annual_rate_percent}%, {years} years) = {instalment:,.0f}")
    return f"LKR {instalment:,.0f} per month"


@tool(approval_mode="never_require")
def home_loan_rules() -> str:
    """Serendib Bank home loan rules (from the Home Loan Product Policy)."""
    print("   🔧 tool: home_loan_rules()")
    return ("Salaried, salary credited to Serendib Bank: 11.5% fixed for 3 years, then AWPLR + 2.5%. "
            "Salaried, salary at another bank: 12.25% fixed for 3 years, then AWPLR + 3.0%. "
            "Maximum tenure 25 years, repaid before age 65. Maximum 80% of property value. "
            "Instalment must not exceed 40% of net monthly income. Processing fee 0.5% (min LKR 15,000, max LKR 75,000).")


INSTRUCTIONS = """You are Serendib Bank's home-loan advisor (Serendib Bank is fictional).
Always call home_loan_rules first, then use monthly_instalment for every calculation - never calculate in your head.
Check affordability against the 40% rule. Be brief, show the numbers, and end with:
'This is an indicative estimate, not a loan offer.'"""


def make_client():
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    if api_key:  # Option B: quick demo fallback
        from agent_framework.openai import OpenAIChatClient

        resource = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip().rstrip("/")
        print("Using API key (demo mode). For real apps use Entra ID.\n")
        return OpenAIChatClient(model=MODEL, api_key=api_key, base_url=f"{resource}/openai/v1/")
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "").strip()
    if "/api/projects/" not in endpoint:
        sys.exit("Set FOUNDRY_PROJECT_ENDPOINT in .env: https://<resource>.services.ai.azure.com/api/projects/<project>")
    from agent_framework.foundry import FoundryChatClient  # Option A: Entra ID, no keys
    from azure.identity import AzureCliCredential

    return FoundryChatClient(project_endpoint=endpoint, model=MODEL, credential=AzureCliCredential())


async def main() -> None:
    agent = Agent(client=make_client(), name="serendib-loan-advisor", instructions=INSTRUCTIONS,
                  tools=[home_loan_rules, monthly_instalment])
    question = " ".join(sys.argv[1:]) or (
        "I earn LKR 450,000 a month after tax and my salary comes to Serendib Bank. "
        "Can I afford a LKR 15 million home loan over 20 years?")
    print(f"👤 {question}\n")
    try:
        result = await agent.run(question)
    except Exception as error:  # noqa: BLE001 - friendly message instead of a stack trace
        text = repr(error)
        hint = ("Azure CLI not installed: install it, run `az login`, or use the API-key option in .env" if "Azure CLI not found" in text
                else "Not signed in: run `az login`" if "az login" in text or "CredentialUnavailable" in text
                else "Signed in but not allowed: add the 'Azure AI User' role on the project, or use the API-key option" if "401" in text or "403" in text
                else f"Deployment not found: set FOUNDRY_MODEL to your deployment name (now '{MODEL}')" if "404" in text
                else "Can't reach the endpoint: check the URL in .env and your network/VPN" if "Connection error" in text
                else text[:300])
        sys.exit(f"\n⚠️  {hint}")
    print(f"\n🤖 {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
