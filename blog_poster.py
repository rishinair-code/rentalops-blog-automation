import os
import json
import requests
import random
import re
from datetime import datetime

# GSC-driven topic selection (falls back gracefully when cache/API unavailable)
try:
    from gsc_topic_selector import pick_topic_gsc_driven
except ImportError:
    pick_topic_gsc_driven = None

# API Keys / config from GitHub Secrets
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

# Model is overridable via env var so a future Google deprecation doesn't require
# a code edit — just update the GEMINI_MODEL secret/variable in the workflow.
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

# ─────────────────────────────────────────────
# PERSONAS & HIGH-INTENT CRA TOPICS
# ─────────────────────────────────────────────
PERSONAS = [
    {
        "name": "First-Time Landlord",
        "description": "Someone who recently became a landlord and is overwhelmed by taxes, compliance, and paperwork. Has 1-2 properties.",
        "topics": [
            "rental property tax deductions Canada 2026",
            "how to fill out T776 form Canada step by step",
            "CRA Line 8960: Repairs vs Capital Expenses for Canadian Landlords",
            "Ontario landlord tenant board rules 2026",
            "how to screen tenants legally Canada",
            "security deposit rules Ontario landlords",
            "first time landlord mistakes Canada",
            "how to set rent price Canadian rental property",
            "landlord tenant board Ontario how it works",
            "how to write lease agreement Ontario",
            "CRA audit rental income what triggers it Canada",
            "is rental income taxable in Canada",
            "landlord tax deductions Canada complete guide",
            "what can landlords claim CRA landlord tax deductions checklist",
        ],
    },
    {
        "name": "Portfolio Builder",
        "description": "A small landlord with 2-5 properties looking to manage efficiently and minimize tax burden without an accountant for every question.",
        "topics": [
            "tracking rental income expenses multiple properties Canada",
            "Can Landlords Deduct Mortgage Interest in Canada Line 8710",
            "capital cost allowance rental property Canada explained",
            "GST HST Canadian landlords what you need to know",
            "how to incorporate rental properties Canada",
            "automating rent collection multiple properties Canada",
            "refinancing rental properties Canada tax implications",
            "holding company rental properties Canada benefits",
            "landlord multiple provinces Canada rules",
            "property manager vs self managing Canada tax comparison",
            "year end tax checklist Canadian landlords multiple properties",
            "rental property depreciation Canada CCA guide",
            "capital gains rental property Canada landlord guide",
        ],
    },
    {
        "name": "Accidental Landlord",
        "description": "Someone renting out a property by necessity — inherited home, relocated for work, couldn't sell. 1 property, very uncertain about rules.",
        "topics": [
            "tax rules renting out principal residence Canada",
            "reporting rental income part year landlord Canada",
            "renting out basement suite Canada rules",
            "CRA Line 9220: Deducting Utilities for a Basement Suite",
            "capital gains selling rental property Canada",
            "failing to report rental income CRA consequences",
            "short term vs long term rental tax rules Canada",
            "Airbnb tax rules Canadian landlords 2026",
            "converting rental property back to personal use Canada",
            "insurance requirements renting home Canada",
            "CRA principal residence exemption rental income Canada",
            "what happens CRA audit rental property Canada",
            "rental income affect tax bracket Canada",
        ],
    },
    {
        "name": "Part-Time Property Manager",
        "description": "Someone managing 2-5 properties for family or as side income alongside a full-time job. Wants simple systems not complexity.",
        "topics": [
            "rental income tax bracket Canada 2026",
            "home office deduction landlord Canada",
            "record keeping requirements Canadian landlords CRA",
            "splitting rental income spouse Canada tax",
            "How to Calculate Motor Vehicle Expenses for Landlords Line 9281",
            "rental property accounting software vs spreadsheets Canada",
            "property management software Canada landlords",
            "tax season preparation part time landlord Canada",
            "professional fees deduction landlord Canada legal accounting",
            "passive income rental income CRA rules Canada",
            "landlord accounting software Canada review",
            "best rental income tracker Canada",
        ],
    },
]

# ─────────────────────────────────────────────
# PILLAR POSTS
# ─────────────────────────────────────────────
PILLAR_POSTS = [
    {
        "id": "cra-tax-pillar",
        "cluster": "CRA Tax & Reporting",
        "topic": "rental income tax Canada complete guide small landlords 2026",
        "title_hint": "Rental Income Tax in Canada: Complete Guide for Small Landlords (2026)",
        "description": "The definitive guide covering everything a 1-3 property Canadian landlord needs to know about rental income tax, T776, CRA compliance, and deductions.",
        "target_word_count": 3500,
        "cluster_posts": [
            "rental property tax deductions Canada 2026",
            "how to fill out T776 form Canada step by step",
            "CRA Line 8960: Repairs vs Capital Expenses for Canadian Landlords",
            "Can Landlords Deduct Mortgage Interest in Canada Line 8710",
            "CRA Line 9220: Deducting Utilities for a Basement Suite",
            "How to Calculate Motor Vehicle Expenses for Landlords Line 9281",
            "what can landlords claim CRA landlord tax deductions checklist",
        ],
        "internal_links": [
            {
                "slug": "failing-to-report-rental-income-to-cra-a-costly-mistake-for-canadian-landlords",
                "title": "Failing to Report Rental Income to CRA: A Costly Mistake for Canadian Landlords",
            },
            {
                "slug": "year-end-tax-checklist-for-canadian-landlords-a-comprehensive-guide",
                "title": "Year-End Tax Checklist for Canadian Landlords: A Comprehensive Guide",
            },
            {
                "slug": "reporting-rental-income-in-canada-a-guide-for-part-year-landlords",
                "title": "Reporting Rental Income in Canada: A Guide for Part-Year Landlords",
            },
        ],
    },
    {
        "id": "ontario-landlord-pillar",
        "cluster": "Ontario Landlord Rules",
        "topic": "Ontario landlord guide 2026 rules rights responsibilities small landlords",
        "title_hint": "Ontario Landlord Guide 2026: Rules, Rights and Responsibilities",
        "description": "Everything a small Ontario landlord needs to know about the LTB, lease agreements, tenant screening, security deposits, and eviction rules.",
        "target_word_count": 3500,
        "cluster_posts": [
            "Ontario landlord tenant board rules 2026",
            "how to write lease agreement Ontario",
            "security deposit rules Ontario landlords",
            "how to screen tenants legally Canada",
            "landlord tenant board Ontario how it works",
            "converting rental property back to personal use Canada",
            "reporting rental income part year landlord Canada",
        ],
        "internal_links": [
            {
                "slug": "converting-rental-property-to-personal-use-in-canada-a-step-by-step-guide",
                "title": "Converting Rental Property to Personal Use in Canada: A Step-by-Step Guide",
            },
        ],
    },
]


# ─────────────────────────────────────────────────────────────
# GEMINI API CALL
# ─────────────────────────────────────────────────────────────

def call_gemini_api(prompt_text):
    """
    Calls the Gemini API's generateContent endpoint and returns the generated text.
    Raises a clear error if the API key is missing, the model is rejected (404),
    or the response doesn't contain the expected content.
    """
    if not GEMINI_API_KEY:
        raise ValueError(
            "Missing Gemini API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) "
            "as a GitHub Actions secret."
        )

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    params = {"key": GEMINI_API_KEY}

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers, params=params)

    if response.status_code == 404:
        raise RuntimeError(
            f"Gemini model '{GEMINI_MODEL}' returned 404 — it's likely been "
            f"deprecated or renamed. Check the current model list in Google AI "
            f"Studio and set the GEMINI_MODEL env var/secret to the current name."
        )

    response.raise_for_status()
    response_data = response.json()

    candidates = response_data.get('candidates')
    if not candidates:
        # Most common cause: the prompt was blocked by a safety filter.
        block_reason = response_data.get('promptFeedback', {}).get('blockReason')
        raise RuntimeError(
            f"Gemini returned no candidates. blockReason={block_reason!r}. "
            f"Full response: {response_data}"
        )

    parts = candidates[0].get('content', {}).get('parts', [])
    if not parts or 'text' not in parts[0]:
        raise RuntimeError(f"Unexpected Gemini response shape: {response_data}")

    return parts[0]['text']


# ─────────────────────────────────────────────────────────────
# TOPIC SELECTION
# ─────────────────────────────────────────────────────────────

def _fallback_topic(persona, used_topics):
    """Pick a topic for this persona that hasn't been used yet, falling back
    to a random repeat if every topic has already been covered."""
    unused = [t for t in persona.get("topics", []) if t not in used_topics]
    return random.choice(unused) if unused else random.choice(persona["topics"])


def _cluster_for_topic(topic):
    """Best-effort mapping of a topic string to a content cluster, used for
    both predefined and GSC-discovered topics."""
    lower = topic.lower()
    if "t776" in lower or "expense" in lower or "tracker" in lower:
        return "CRA Tax & Reporting"
    if "ontario" in lower or "board" in lower:
        return "Ontario Landlord Rules"
    return "General"


def select_topic(used_topics):
    """Pick a persona, then pick a topic for that persona — using GSC demand
    data when available, falling back to the predefined topic list."""
    chosen_persona = random.choice(PERSONAS)
    target_persona = chosen_persona["name"]

    if pick_topic_gsc_driven:
        print("🔍 Auditing Google Search Console performance data...")
        try:
            target_topic = pick_topic_gsc_driven(
                chosen_persona, used_topics, fallback_fn=_fallback_topic
            )
        except Exception as e:
            print(f"⚠️ GSC data processing encountered an error: {e}. Falling back.")
            target_topic = _fallback_topic(chosen_persona, used_topics)
    else:
        print("⚠️ GSC selector not available. Selecting from predefined strategy matrix...")
        target_topic = _fallback_topic(chosen_persona, used_topics)

    cluster_group = _cluster_for_topic(target_topic)
    return target_persona, target_topic, cluster_group


# ─────────────────────────────────────────────────────────────
# MAIN EXECUTION ROUTINE
# ─────────────────────────────────────────────────────────────

def main():
    print("============================================================")
    print("🚀 RentalOps Blog Automation Starting...")
    print("============================================================")

    used_topics = []
    if os.path.exists("used_topics.json"):
        with open("used_topics.json", "r") as f:
            used_topics = json.load(f)
    print(f"📋 Found {len(used_topics)} previously used topics")

    target_persona, target_topic, cluster_group = select_topic(used_topics)

    print(f"👤 Target Persona Match: {target_persona}")
    print(f"🤖 Generating optimized content around target keyword: '{target_topic}'")
    print(f"🗂️ Strategic Content Cluster Assignment: {cluster_group}")

    prompt = f"""
You are an expert Canadian tax accountant and property management advisor writing for rentalops.ca.
Write an incredibly comprehensive, highly technical yet accessible SEO-optimized blog post for a '{target_persona}' targeting the keyword phrase: '{target_topic}'.
Structure requirements:
1. Include clear H2 and H3 markdown headings.
2. Reference specific CRA rules or context (like the T776 form or real estate rules for 2026) where applicable.
3. Keep a professional, authoritative, yet friendly peer-to-peer tone. Do not use generic fluffy filler language.
"""

    blog_text = call_gemini_api(prompt)

    slug = re.sub(r'[^a-z0-9]+', '-', target_topic.lower()).strip('-')
    post_data = {
        "title": f"The Complete Guide to {target_topic.title()}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "persona": target_persona,
        "cluster": cluster_group,
        "target_keyword": target_topic,
        "slug": slug,
        "content": blog_text,
    }

    os.makedirs("posts", exist_ok=True)
    with open(f"posts/{slug}.json", "w") as f:
        json.dump(post_data, f, indent=2)
    print(f"✅ Success! Content successfully compiled to posts/{slug}.json")

    if target_topic not in used_topics:
        used_topics.append(target_topic)
        with open("used_topics.json", "w") as f:
            json.dump(used_topics, f, indent=2)


if __name__ == "__main__":
    main()
