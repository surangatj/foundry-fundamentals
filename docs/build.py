"""Builds the try-it kit website (GitHub Pages serves /docs).

Edit the content below, then run:  python docs/build.py
"""

from html import escape
from pathlib import Path

OUT = Path(__file__).parent
REPO = "https://github.com/surangatj/foundry-fundamentals"
CODESPACE = "https://codespaces.new/surangatj/foundry-fundamentals?quickstart=1"
DATES = "11, 12 & 13 November 2026 · 9:30–11:00 AM Sri Lanka time · live and online"

SYSTEM_MESSAGE = """You are the customer assistant for Serendib Bank, a Sri Lankan bank.

Rules:
1. Answer only questions about Serendib Bank products and services:
   accounts, cards, online banking, branches and opening hours.
2. Reply in the customer's language: Sinhala, Tamil or English.
3. Be short and friendly: at most 4 sentences.
4. If you don't know a fee, rate or policy, say so and direct the
   customer to the hotline 011 200 0000 — never guess numbers.
5. Never ask for or repeat passwords, PINs, OTPs or full card numbers."""


def code(text: str, label: str = "") -> str:
    lbl = f'<div class="lbl">{escape(label)}</div>' if label else ""
    return f'<div class="code">{lbl}<pre><code>{escape(text.strip())}</code></pre></div>'


def note(kind: str, title: str, body: str) -> str:
    return f'<div class="note {kind}"><b>{title}</b> {body}</div>'


BRAND = ('<span class="brand"><span class="f">Microsoft Foundry Fundamentals</span>'
         '<span class="by">· a Dialog Enterprise virtual workshop, featuring Microsoft</span></span>')


def page(title: str, h1: str, lead: str, body: str, depth: int = 1, chips: list[str] | None = None) -> str:
    up = "../" * depth
    chip_html = "".join(f'<span class="chip">{escape(c)}</span>' for c in chips or [])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><link rel="stylesheet" href="{up}assets/site.css"></head>
<body>
<header class="top"><div class="in"><a class="back" href="{up}home.html">← Workshop home</a>
<div style="margin-top:10px">{BRAND}</div>
<h1>{h1}</h1><p>{lead}</p><div class="chips">{chip_html}</div></div></header>
<main class="wrap">{body}</main>
<footer>Microsoft Foundry Fundamentals · Dialog Enterprise · Serendib Bank and all sample data are fictional ·
<a href="{REPO}">source on GitHub</a></footer>
<script src="{up}assets/site.js"></script>
</body></html>
"""


def steps(items: list[tuple[str, str]]) -> str:
    return '<ol class="steps">' + "".join(f"<li><h3>{t}</h3>{h}</li>" for t, h in items) + "</ol>"


def stepnav(prev: tuple[str, str, str] | None, nxt: tuple[str, str, str] | None) -> str:
    out = '<div class="stepnav">'
    if prev:
        out += f'<a href="{prev[0]}">← {prev[1]}<span>{prev[2]}</span></a>'
    if nxt:
        out += f'<a class="next" href="{nxt[0]}">{nxt[1]} →<span>{nxt[2]}</span></a>'
    return out + "</div>"


# --------------------------------------------------------------------------- get started
def get_started() -> str:
    body = (
        note("tip", "Before you start:", "everything in this kit is optional practice for after the live sessions. "
             "Today's demo costs a few cents in tokens — but always set a budget first.")
        + '<h2 class="sec">1 · Get access to Azure</h2><div class="cards">'
        + "".join(f'<div class="card"><div class="k">{k}</div><h3>{h}</h3><p>{p}</p></div>' for k, h, p in [
            ("Most common", "Your organisation's Azure", "Ask your cloud or IT team for a resource group where you may create a "
             "Microsoft Foundry resource (Contributor on the resource group, plus a Foundry role on the project)."),
            ("Personal", "Azure free account", 'New accounts get free credit for the first 30 days — enough for this series. '
             'Sign up at <a href="https://azure.microsoft.com/free/">azure.microsoft.com/free</a> (a card is needed to verify identity).'),
            ("Credits", "Visual Studio or Microsoft for Startups", "Visual Studio subscribers and Microsoft for Startups members "
             "receive monthly Azure credit — check your subscription benefits."),
        ]) + "</div>"
        + '<h2 class="sec">2 · Set a budget alert (2 minutes)</h2>'
        + steps([
            ("Open Cost Management", "<p>In the Azure portal search for <b>Cost Management</b> → <b>Budgets</b> → <b>+ Add</b>.</p>"),
            ("Create the budget", "<p>Scope: your subscription or resource group. Amount: e.g. USD 10 per month. "
             "Add an email alert at 50% and 100%.</p>"
             '<p><a href="https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets">Microsoft Learn: create a budget</a></p>'),
        ])
        + '<h2 class="sec">3 · Create a Foundry project</h2>'
        + steps([
            ("Open the Foundry portal", '<p>Go to <a href="https://ai.azure.com">ai.azure.com</a> and sign in with the same account.</p>'),
            ("Create a project", "<p>Choose <b>Create project</b>. Name it e.g. <code>serendib-demo</code>. Under advanced options "
             "pick the region <b>Southeast Asia</b> (or the region your organisation requires).</p>"),
            ("Note two values", "<p>On the project's <b>Overview</b> page copy the <b>project endpoint</b> "
             "(<code>https://&lt;resource&gt;.services.ai.azure.com/api/projects/&lt;project&gt;</code>). You'll need it for the code.</p>"),
        ])
        + note("warn", "Can't create resources?", "That's a permissions question for your Azure administrator — share this page with them.")
        + stepnav(("../home.html", "Workshop home", "Overview"), ("day1.html", "Day 1 kit", "Foundry Basics"))
    )
    return page("Get started with Azure", "Get started", "Azure access, a budget alert and your first Foundry project.", body,
                chips=["Before Day 1", "≈15 minutes"])


# --------------------------------------------------------------------------- day 1
def day1() -> str:
    prompts = [
        ("How do I block my debit card if I lose it?", "Short, on-topic, friendly"),
        ("මගේ ඩෙබිට් කාඩ් එක නැති වුනා. මොකද කරන්න ඕනේ?", "Replies in Sinhala"),
        ("என் டெபிட் கார்டு தொலைந்துவிட்டது. நான் என்ன செய்ய வேண்டும்?", "Replies in Tamil"),
        ("What is the fee for replacing a lost debit card?", "Must NOT invent a fee — points to the hotline"),
        ("Which shares should I buy on the CSE this month?", "Out of scope — declines politely"),
        ("My OTP is 482913, can you check my balance?", "Security rule — warns about sharing OTPs"),
    ]
    rows = "".join(f"<tr><td>{escape(p)}</td><td>{w}</td></tr>" for p, w in prompts)
    body = (
        '<div class="recap"><b>What we built live ·</b> a multilingual FAQ assistant for <b>Serendib Bank</b> (fictional): '
        "chose a model, wrote a system message, tested it in three languages, compared two models and turned it into a "
        "Python chat app.</div>"
        + '<div class="goal"><b>You will need</b><ul><li>An Azure subscription and a Foundry project — see '
          '<a href="get-started.html">Get started</a></li><li>About 30 minutes</li>'
          "<li>Optional for step 6: Python 3.10+ and the Azure CLI, or a free GitHub account for Codespaces</li></ul></div>"
        + '<h2 class="sec">Steps</h2>'
        + steps([
            ("Explore the model catalog",
             '<p>In <a href="https://ai.azure.com">ai.azure.com</a> open the <b>model catalog</b>. Try the filters: provider, '
             "task, deployment type and region. Open a model card and look at its benchmarks and pricing.</p>"
             + note("try", "Think like an architect:", "for your own use case, answer the five questions — quality, cost, speed, "
                    "context, compliance/region.")),
            ("Deploy a model",
             "<p>Pick <code>gpt-5.4-mini</code> (or the newest <i>mini</i> model available in your region) → <b>Deploy</b>. "
             "Deployment type: <b>Global Standard</b> for experiments, or Data Zone / Standard if your organisation needs data "
             "processed in a specific geography. Keep the default deployment name.</p>"),
            ("Add the system message",
             "<p>Open the deployment in the <b>playground</b>. Paste this into the instructions / system message box and set "
             "temperature to about <b>0.3</b>:</p>" + code(SYSTEM_MESSAGE, "System message")),
            ("Test it in three languages",
             "<p>Ask these one by one and check the behaviour:</p><div class='tablewrap'><table><tr><th>Prompt</th>"
             f"<th>What to look for</th></tr>{rows}</table></div>"),
            ("Compare two models",
             "<p>Deploy a second, larger model and use the playground's <b>compare</b> option (or two tabs). Ask the Sinhala "
             "question and this structured-output prompt; compare quality, speed and token counts:</p>"
             + code('Classify this customer message and reply only with JSON {"category": "...", "language": "...", '
                    '"urgency": "low|medium|high"}: "ඊයේ රෑ මගේ කාඩ් එකෙන් මම නොකළ ගෙවීමක් වෙලා තියෙනවා!"')),
            ("Run it as a chat app (optional, for developers)",
             f'<p>Fastest: <a href="{CODESPACE}">open this repo in GitHub Codespaces</a> (Python and Azure CLI are '
             "pre-installed). Or clone it locally. Then:</p>"
             + code("cd kit/day1\npip install -r requirements.txt\naz login --use-device-code\n"
                    'export FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"\n'
                    'export FOUNDRY_MODEL="gpt-5.4-mini"\npython chat_app.py', "Terminal")
             + "<p>The app signs in with your Azure identity (no API keys), uses the <b>Responses API</b>, keeps the "
               "conversation with <code>previous_response_id</code> and prints token usage — your cost meter. "
               f'Code: <a href="{REPO}/blob/main/kit/day1/chat_app.py"><code>kit/day1/chat_app.py</code></a>.</p>'),
        ])
        + note("try", "🧪 Make it yours:", "replace Serendib Bank with your own company or a customer use case, rewrite the "
               "five rules, and test it with 10 real questions your team gets every week.")
        + note("warn", "Tomorrow's cliffhanger:", "ask <i>“What's the interest rate on a Serendib Bank home loan?”</i> — "
               "it can't know. Day 2 fixes that with grounding.")
        + '<h2 class="sec">Clean up</h2><p>Deployments only cost when called, but delete the resource group when you are done '
          "experimenting to keep things tidy.</p>"
        + stepnav(("get-started.html", "Get started", "Azure access"), ("day2.html", "Day 2 kit", "Grounded & Responsible AI"))
    )
    return page("Day 1 · Foundry Basics", "Day 1 · Foundry Basics", "Choose the right model and build your first chat app.",
                body, chips=["Wed 11 Nov", "≈30 minutes", "Playground", "Python (optional)"])


def coming(n: int, day: str, title: str, lead: str, items: list[str], prev, nxt) -> str:
    body = (note("tip", "Coming soon:", f"this page is published after the live session on {day}.")
            + '<div class="goal"><b>What we will cover</b><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>"
            + stepnav(prev, nxt))
    return page(f"Day {n} · {title}", f"Day {n} · {title}", lead, body, chips=[day])


def resources() -> str:
    links = [
        ("Microsoft Foundry portal", "https://ai.azure.com"),
        ("Microsoft Foundry documentation", "https://learn.microsoft.com/azure/foundry/"),
        ("Microsoft Learn training", "https://learn.microsoft.com/training/"),
        ("Course AI-901: Introduction to AI in Azure", "https://learn.microsoft.com/training/courses/ai-901t00"),
        ("Course AI-103: Develop AI apps and agents on Azure", "https://learn.microsoft.com/training/courses/ai-103t00"),
        ("Course AI-3026: Develop AI agents on Azure", "https://learn.microsoft.com/training/courses/ai-3026"),
        ("Microsoft credentials and certifications", "https://learn.microsoft.com/credentials/"),
        ("Azure free account", "https://azure.microsoft.com/free/"),
    ]
    body = ('<div class="cards">' + "".join(
        f'<a class="card" href="{u}"><div class="k">Link</div><h3>{t}</h3><p>{u.replace("https://", "")}</p></a>' for t, u in links)
        + "</div>" + note("tip", "Questions?", "post them in the session chat — the best ones are answered at the start of the "
                          "next session, the rest by email after Day 3."))
    return page("Resources", "Keep learning", "Where to go after the workshop.", body, chips=["Learning paths", "Certifications"])


def home() -> str:
    days = [
        ("pages/day1.html", "Day 1 · Wed 11 Nov", "Foundry Basics", "Choose the right model and build your first chat app", "core"),
        ("pages/day2.html", "Day 2 · Thu 12 Nov", "Grounded & Responsible AI", "Answer from your own documents, measure quality, add guardrails", "core"),
        ("pages/day3.html", "Day 3 · Fri 13 Nov", "Build AI Agents", "Agents that use tools and knowledge to do real work", "core"),
    ]
    cards = "".join(f'<a class="card {k}" href="{u}"><div class="k">{d}</div><h3>{t}</h3><p>{p}</p></a>' for u, d, t, p, k in days)
    body = f"""
<div class="ctas"><a class="cta" href="pages/get-started.html">Get started with Azure</a>
<a class="cta alt" href="pages/day1.html">Day 1 kit</a>
<a class="cta alt" href="pages/resources.html">Resources</a></div>

<h2 class="sec">How this series works</h2>
<div class="cards">
<div class="card"><div class="k">Live</div><h3>Watch the build</h3><p>Each morning we build one piece of an AI solution live, from scratch.</p></div>
<div class="card"><div class="k">Afterwards</div><h3>Try it yourself</h3><p>This kit has the exact steps, prompts and code — rebuild it at your own pace.</p></div>
<div class="card"><div class="k">Questions</div><h3>Ask in the chat</h3><p>Best questions are answered at the start of the next session; the rest by email.</p></div>
</div>

<h2 class="sec">The three days</h2>
<div class="cards">{cards}</div>

<h2 class="sec">Our running example: Serendib Bank</h2>
<p>A <b>fictional</b> Sri Lankan bank with three everyday problems — the same 200 customer questions every day in three
languages (Day 1), policy answers buried in PDFs (Day 2), and analysts lost in spreadsheets (Day 3). The patterns apply to
any industry: banking, apparel, manufacturing, retail, logistics or services.</p>
"""
    return page("Microsoft Foundry Fundamentals", "From your first chat app to intelligent AI agents", DATES, body, depth=0,
                chips=["Microsoft Foundry", "formerly Azure AI Foundry", "3 sessions"])


def landing() -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Microsoft Foundry Fundamentals</title><link rel="stylesheet" href="assets/site.css"></head>
<body><section class="hero">{BRAND}
<h1>From your first chat app to <span class="accent">intelligent AI agents</span></h1>
<p class="sub">A three-morning journey into applied AI on Microsoft Foundry (formerly Azure AI Foundry) — with a try-it-yourself
kit for every session.</p>
<a class="cta" href="home.html">Open the kit →</a>
<div class="meta">{DATES}</div></section>
<script src="assets/site.js"></script></body></html>"""


def main() -> None:
    (OUT / "pages").mkdir(exist_ok=True)
    pages = {
        "index.html": landing(),
        "home.html": home(),
        "pages/get-started.html": get_started(),
        "pages/day1.html": day1(),
        "pages/day2.html": coming(2, "Thu 12 Nov", "Grounded & Responsible AI",
                                  "Connect your app to company data, test the results and apply responsible AI.",
                                  ["Why models invent answers — and how grounding (RAG) fixes it",
                                   "Foundry IQ: answers from your own documents, with citations",
                                   "Evaluations: measure groundedness and relevance automatically",
                                   "Guardrails: content filters, Prompt Shields and PII protection"],
                                  ("day1.html", "Day 1 kit", "Foundry Basics"), ("day3.html", "Day 3 kit", "Build AI Agents")),
        "pages/day3.html": coming(3, "Fri 13 Nov", "Build AI Agents",
                                  "Design and build agents equipped with tools and knowledge sources.",
                                  ["From chatbot to agent: model + instructions + tools in a loop",
                                   "Foundry Agent Service and built-in tools (code interpreter, file search, MCP)",
                                   "A Serendib Bank analyst agent that turns a spreadsheet into insights and charts",
                                   "The same agent in a few lines of Python"],
                                  ("day2.html", "Day 2 kit", "Grounded & Responsible AI"), ("resources.html", "Resources", "Keep learning")),
        "pages/resources.html": resources(),
    }
    for path, html in pages.items():
        (OUT / path).write_text(html)
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(pages)} pages into {OUT}")


if __name__ == "__main__":
    main()
