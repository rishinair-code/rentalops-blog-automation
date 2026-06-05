import os
import json
import requests
import random
import re
import time
from datetime import datetime

# API Keys from GitHub Secrets
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
DEVTO_API_KEY = os.environ.get('DEVTO_API_KEY')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')

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
            {
                "slug": "navigating-the-cra-principal-residence-exemption-a-guide-for-canadian-landlords",
                "title": "Navigating the CRA Principal Residence Exemption: A Guide for Canadian Landlords",
            },
            {
                "slug": "reporting-rental-income-in-canada-a-guide-for-part-year-landlords",
                "title": "Reporting Rental Income in Canada: A Guide for Part-Year Landlords",
            },
        ],
    },
]

# ─────────────────────────────────────────────
# PUBLISHED POSTS INDEX
# ─────────────────────────────────────────────
PUBLISHED_POSTS = [
    {
        "slug": "cra-compliant-bookkeeping-canadian-landlords-complete-guide",
        "title": "CRA-Compliant Bookkeeping for Canadian Landlords: The Complete Guide",
        "topic": "rental income tax Canada complete guide small landlords 2026",
        "cluster": "CRA Tax & Reporting",
    },
    {
        "slug": "ontario-landlord-guide-2026",
        "title": "Ontario Landlord Guide 2026: Rules, Rights and Responsibilities",
        "topic": "Ontario landlord guide 2026 rules rights responsibilities small landlords",
        "cluster": "Ontario Landlord Rules",
    },
    {
        "slug": "converting-rental-property-to-personal-use-in-canada-a-step-by-step-guide",
        "title": "Converting Rental Property to Personal Use in Canada: A Step-by-Step Guide",
        "topic": "converting rental property back to personal use Canada",
        "cluster": "Ontario Landlord Rules",
    },
    {
        "slug": "failing-to-report-rental-income-to-cra-a-costly-mistake-for-canadian-landlords",
        "title": "Failing to Report Rental Income to CRA: A Costly Mistake for Canadian Landlords",
        "topic": "failing to report rental income CRA consequences",
        "cluster": "CRA Tax & Reporting",
    },
    {
        "slug": "navigating-the-cra-principal-residence-exemption-a-guide-for-canadian-landlords",
        "title": "Navigating the CRA Principal Residence Exemption: A Guide for Canadian Landlords",
        "topic": "CRA principal residence exemption rental income Canada",
        "cluster": "CRA Tax & Reporting",
    },
    {
        "slug": "reporting-rental-income-in-canada-a-guide-for-part-year-landlords",
        "title": "Reporting Rental Income in Canada: A Guide for Part-Year Landlords",
        "topic": "reporting rental income part year landlord Canada",
        "cluster": "CRA Tax & Reporting",
    },
    {
        "slug": "setting-the-right-rent-price-for-your-canadian-rental-property",
        "title": "Setting the Right Rent Price for Your Canadian Rental Property",
        "topic": "how to set rent price Canadian rental property",
        "cluster": "Ontario Landlord Rules",
    },
    {
        "slug": "simplifying-rental-property-accounting-software-vs-spreadsheets-for-canadian-landlords",
        "title": "Simplifying Rental Property Accounting: Software vs Spreadsheets for Canadian Landlords",
        "topic": "rental property accounting software vs spreadsheets Canada",
        "cluster": "General",
    },
    {
        "slug": "tracking-rental-income-and-expenses-across-multiple-properties-a-canadian-landlord-guide",
        "title": "Tracking Rental Income and Expenses Across Multiple Properties: A Canadian Landlord Guide",
        "topic": "tracking rental income expenses multiple properties Canada",
        "cluster": "CRA Tax & Reporting",
    },
    {
        "slug": "year-end-tax-checklist-for-canadian-landlords-a-comprehensive-guide",
        "title": "Year-End Tax Checklist for Canadian Landlords: A Comprehensive Guide",
        "topic": "year end tax checklist Canadian landlords multiple properties",
        "cluster": "CRA Tax & Reporting",
    },
    {
        "slug": "airbnb-tax-rules-canadian-landlords-2026",
        "title": "Airbnb Tax Rules: Canadian Landlords 2026",
        "topic": "Airbnb tax rules Canadian landlords 2026",
        "cluster": "CRA Tax & Reporting",
    },
]

PILLAR_POSTS_FILE = "published_pillars.json"

def get_published_pillars():
    try:
        if os.path.exists(PILLAR_POSTS_FILE):
            with open(PILLAR_POSTS_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"⚠️  Could not read published pillars: {e}")
        return []

def save_published_pillar(pillar_id):
    try:
        published = get_published_pillars()
        if pillar_id not in published:
            published.append(pillar_id)
        with open(PILLAR_POSTS_FILE, "w") as f:
            json.dump(published, f, indent=2)
        print(f"✅ Pillar saved: {pillar_id}")
    except Exception as e:
        print(f"⚠️  Could not save pillar: {e}")

def get_used_topics():
    try:
        if os.path.exists("used_topics.json"):
            with open("used_topics.json", "r") as f:
                used = json.load(f)
            print(f"📋 Found {len(used)} previously used topics")
            return used
        else:
            print("📋 No used_topics.json found — starting fresh")
            return []
    except Exception as e:
        print(f"⚠️  Could not read used topics: {e}")
        return []

def save_used_topic(topic):
    try:
        used = get_used_topics()
        if topic not in used:
            used.append(topic)
        with open("used_topics.json", "w") as f:
            json.dump(used, f, indent=2)
        print(f"✅ Topic saved: {topic[:50]}")
    except Exception as e:
        print(f"⚠️  Could not save used topic: {e}")

def generate_slug(title: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    # Increase length to 100 to support long-tail keywords
    if len(slug) > 100:
        slug = slug[:100]
        last_hyphen = slug.rfind('-')
        if last_hyphen > 50:
            slug = slug[:last_hyphen]
            
    # Clean up dangling stop words at the end of the URL
    slug = re.sub(r'-(for|and|the|a|in|to|of|on)$', '', slug)
    return slug

def get_current_persona():
    day_of_year = datetime.now().timetuple().tm_yday
    persona_index = day_of_year % len(PERSONAS)
    return PERSONAS[persona_index]

def pick_topic(persona: dict, used_topics: list, offset: int = 0) -> str | None:
    available = [t for t in persona["topics"] if t not in used_topics]
    if not available:
        print(f"🔄 All topics for {persona['name']} used — resetting pool")
        available = persona["topics"]
    day_of_year = datetime.now().timetuple().tm_yday
    topic_index = (day_of_year + offset) % len(available)
    topic = available[topic_index]
    print(f"🤖 Topic (offset {offset}): {topic}")
    return topic

def get_internal_links(current_topic: str, current_cluster: str = None) -> str:
    BASE_URL = "https://www.rentalops.ca/blog"
    candidates = [p for p in PUBLISHED_POSTS if p["topic"] != current_topic]
    current_words = set(current_topic.lower().split())
    scored = []
    for post in candidates:
        post_words = set(post["topic"].lower().split())
        keyword_score = len(current_words & post_words)
        cluster_bonus = 2 if (current_cluster and post.get("cluster") == current_cluster) else 0
        scored.append((keyword_score + cluster_bonus, post))
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [p for _, p in scored[:3]]
    if not selected:
        return ""
    links_block = "\n".join(f'- [{p["title"]}]({BASE_URL}/{p["slug"]})' for p in selected)
    return f"""
- Naturally include 2-3 internal links to related RentalOps blog posts within the article body.
  Use the anchor text and URLs exactly as listed below.
  Only link where it makes contextual sense — do NOT force links:
{links_block}"""

def get_pillar_internal_links(pillar: dict) -> str:
    BASE_URL = "https://www.rentalops.ca/blog"
    links = pillar.get("internal_links", [])
    if not links:
        return ""
    links_block = "\n".join(f'- [{l["title"]}]({BASE_URL}/{l["slug"]})' for l in links)
    return f"""
- This is a PILLAR post. Link to these related cluster posts naturally within the content:
{links_block}
- Also mention readers can explore the RentalOps blog for detailed guides on each sub-topic."""

def get_pending_pillar() -> dict | None:
    today = datetime.now().day
    published_pillars = get_published_pillars()
    if today not in [1, 15]:
        return None
    for pillar in PILLAR_POSTS:
        if pillar["id"] not in published_pillars:
            print(f"📌 Pillar post due: {pillar['cluster']}")
            return pillar
    print("✅ All pillar posts already published")
    return None

def generate_image_query(title):
    topic_map = [
        (["eviction", "tribunal", "LTB", "RTB", "notice"], "tenant landlord dispute paperwork"),
        (["tax", "CRA", "T776", "deduction", "refund", "CCA"], "canadian tax documents accounting"),
        (["receipt", "expense", "tracking", "bookkeeping"], "receipt invoice bookkeeping desk"),
        (["rent", "collection", "payment", "arrears"], "rent payment money transfer"),
        (["screening", "tenant", "application"], "rental application interview"),
        (["maintenance", "repair", "inspection"], "home repair maintenance tools"),
        (["lease", "agreement", "contract", "sign"], "signing rental contract documents"),
        (["insurance", "liability"], "home insurance protection"),
        (["scale", "portfolio", "multiple", "units", "properties"], "apartment building investment"),
        (["software", "tool", "app", "system", "spreadsheet"], "property management laptop"),
        (["mortgage", "interest", "financing", "bank"], "canadian real estate mortgage"),
        (["security deposit", "deposit"], "keys apartment handover"),
        (["GST", "HST", "sales tax"], "canadian tax forms accounting"),
        (["incorporate", "holding company", "corporation"], "business incorporation documents"),
        (["Airbnb", "short-term", "vacation rental"], "vacation rental property"),
        (["principal residence", "capital gains"], "canadian home ownership"),
        (["basement", "suite", "secondary unit"], "basement apartment rental"),
        (["guide", "complete", "everything"], "canadian landlord reading documents"),
        (["Ontario", "rules", "rights"], "ontario canada property rental"),
    ]
    title_lower = title.lower()
    for keywords, query in topic_map:
        if any(k.lower() in title_lower for k in keywords):
            print(f"🖼️  Image query: '{query}'")
            return query
    fallbacks = [
        "canadian rental property exterior",
        "apartment building Canada",
        "landlord property keys",
        "rental home neighbourhood Canada",
        "residential property investment",
    ]
    query = random.choice(fallbacks)
    print(f"🖼️  Image query (fallback): '{query}'")
    return query

def get_unsplash_image(query):
    print(f"🖼️  Fetching image for: {query}")
    if not UNSPLASH_ACCESS_KEY:
        print("⚠️  UNSPLASH_ACCESS_KEY not set — skipping image")
        return None
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": query,
                "orientation": "landscape",
                "content_filter": "high",
            },
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        image_url = data["urls"]["regular"]
        photographer = data["user"]["name"]
        credit = f"Photo by [{photographer}](https://unsplash.com/@{data['user']['username']}) on [Unsplash](https://unsplash.com)"
        print(f"✅ Image found by {photographer}")
        return {"url": image_url, "credit": credit}
    except Exception as e:
        print(f"⚠️  Unsplash fetch failed: {e}")
        return None

def call_groq(messages: list, max_tokens: int = 6000, temperature: float = 0.7, force_json_mode: bool = False) -> str | None:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if force_json_mode:
        payload["response_format"] = {"type": "json_object"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Groq API call failed: {e}")
        return None

def repair_json(raw: str) -> str:
    start = raw.find('{')
    end = raw.rfind('}')
    if start == -1 or end == -1:
        return raw
    raw = raw[start:end + 1]

    result = []
    in_string = False
    escape_next = False

    for char in raw:
        if escape_next:
            result.append(char)
            escape_next = False
            continue

        if char == '\\':
            result.append(char)
            escape_next = True
            continue

        if char == '"':
            in_string = not in_string
            result.append(char)
            continue

        if in_string:
            if char == '\n':
                result.append('\\n')
            elif char == '\r':
                result.append('\\r')
            elif char == '\t':
                result.append('\\t')
            else:
                result.append(char)
        else:
            result.append(char)

    return ''.join(result)

def extract_json(raw: str) -> dict | None:
    if not raw:
        return None
    # Safely building the markdown fence strings to prevent premature parser exit
    ticks = "```"
    cleaned = re.sub(r'^' + ticks + r'(?:json)?\s*', '', raw.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r'\s*' + ticks + r'$', '', cleaned.strip(), flags=re.MULTILINE)
    repaired = repair_json(cleaned)
    try:
        return json.loads(repaired)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse failed after repair: {e}")
        return None

def devto_canonical_exists(canonical_url: str) -> bool:
    if not DEVTO_API_KEY:
        return False
    try:
        response = requests.get(
            "[https://dev.to/api/articles/me/published](https://dev.to/api/articles/me/published)",
            headers={"api-key": DEVTO_API_KEY},
            params={"per_page": 100},
            timeout=15,
        )
        response.raise_for_status()
        articles = response.json()
        for article in articles:
            if article.get("canonical_url") == canonical_url:
                return True
        return False
    except Exception as e:
        print(f"⚠️  Could not check Dev.to for duplicates: {e}")
        return False

# ─────────────────────────────────────────────
# REWRITTEN CONTENT MATRIX PLUGINS
# ─────────────────────────────────────────────
def generate_pillar_content(pillar: dict):
    print(f"📌 Generating PILLAR post: {pillar['cluster']}")
    print(f"   Topic: {pillar['topic']}")

    internal_links_instruction = get_pillar_internal_links(pillar)
    cluster_posts_list = "\n".join(f"  - {t}" for t in pillar["cluster_posts"])

    messages = [
        {
            "role": "system",
            "content": """You are a senior content strategist for RentalOps, a Canadian landlord expense tracking and tax preparation platform built specifically for small landlords (1-3 properties) who have a full-time day job.

Audience: "The Accidental Landlord" and "Small Investor". They are busy professionals, not accountants. They dread tax season and find CRA rules overwhelming. Write in plain, clear, jargon-free English using relatable comparisons.

Conversion Strategy: Your main goal is to drive readers to download our free spreadsheet tool located at [https://www.rentalops.ca/free-landlord-t776-excel-template](https://www.rentalops.ca/free-landlord-t776-excel-template). Frame the spreadsheet as the perfect bridge to get organized, and mention RentalOps software trial as the ultimate hands-free automated upgrade.

OUTPUT FORMAT: You must output a single valid JSON object with these exact keys:
title, metaDescription, content, tags, persona, postType, cluster
The content value must be a single string containing the full markdown article with escaped newlines (\\n). Do not output text outside the JSON object.""",
        },
        {
            "role": "user",
            "content": f"""Write a comprehensive PILLAR blog post for cluster: "{pillar['cluster']}"

Suggested title: {pillar['title_hint']}
Core topic: {pillar['topic']}
Description: {pillar['description']}

Sub-topics — write a full H2 section (400+ words) for each:
{cluster_posts_list}

Strict SEO & Conversion Requirements:
- PRIMARY KEYWORD: "{pillar['topic']}" — must appear in the title, the first paragraph, and at least 3 H2/H3 headings.
- TARGET KEYWORDS TO WEAVE IN NATURALLY: "T776 form software Canada", "CRA rental expense tracker landlord", "rental bookkeeping software Canada", "what can landlords claim CRA".
- metaDescription: 150-160 characters EXACTLY. Must include the primary keyword and end with a clear benefit.
- Content Depth: Minimum 3000 words. Fully develop every single section. Do not summarize or use placeholders. 
- Tone: Plain English. Explain complex tax rules using easy comparisons (e.g., explaining capital cost allowance vs. current repairs).
- Contextual Canadian Data: Explicitly reference real CRA deadlines (April 30th), actual T776 form line numbers (e.g., Line 8710 for interest, Line 8960 for repairs), and real tax implications.
- The Core Conversion Hook: In the introduction and again in the final conclusion section, pitch the "Free Canadian Landlord T776 Excel Template" available at [https://www.rentalops.ca/free-landlord-t776-excel-template](https://www.rentalops.ca/free-landlord-t776-excel-template) as the solution to stop the March tax scramble. Emphasize that it is pre-mapped directly to the CRA guidelines so they don't lose unclaimed deductions.{internal_links_instruction}
- tags: array of 5 highly relevant Canadian landlord search terms.
- persona: "Small Landlord"
- postType: "pillar"
- cluster: "{pillar['cluster']}"

Output only the JSON object. No raw conversational text before or after it.""",
        },
    ]

    raw = call_groq(messages, max_tokens=8000, temperature=0.65, force_json_mode=False)
    blog_data = extract_json(raw)

    if not blog_data:
        return None, None

    required = ["title", "metaDescription", "content", "tags"]
    for field in required:
        if field not in blog_data:
            print(f"❌ Missing field: {field}")
            return None, None

    blog_data["postType"] = "pillar"
    blog_data["cluster"] = pillar["cluster"]

    word_count = len(blog_data["content"].split())
    print(f"✅ Pillar content generated")
    print(f"   Word count: ~{word_count} words")

    return blog_data, pillar["topic"]


def generate_blog_content(topic: str, persona: dict):
    print(f"🎯 Target persona: {persona['name']}")
    print(f"🤖 Generating content about: {topic}")

    current_cluster = None
    for pillar in PILLAR_POSTS:
        if topic in pillar["cluster_posts"]:
            current_cluster = pillar["cluster"]
            break
    print(f"🗂️  Cluster: {current_cluster or 'General'}")

    pillar_link_instruction = ""
    published_pillars = get_published_pillars()
    for pillar in PILLAR_POSTS:
        if pillar["cluster"] == current_cluster and pillar["id"] in published_pillars:
            pillar_slug = generate_slug(pillar["title_hint"])
            pillar_link_instruction = f"""
- This post is part of the "{pillar['cluster']}" cluster. Link back to the pillar guide naturally once in the article: [{pillar['title_hint']}](https://www.rentalops.ca/blog/{pillar_slug})"""
            break

    include_roi = random.random() < 0.3
    roi_instruction = ""
    if include_roi:
        roi_instruction = """
- Include a section: "What This Costs You Without the Right Tools" comparing manual spreadsheets vs RentalOps. e.g. "2-3 hours/month tracking receipts manually vs $6.99/month for RentalOps"."""

    internal_links_instruction = get_internal_links(topic, current_cluster)

    messages = [
        {
            "role": "system",
            "content": f"""You are an expert financial content writer for RentalOps, a Canadian rental income tracking tool optimized for busy accidental landlords who have a full-time day job.

Audience: {persona['name']} — {persona['description']}. They keep receipts in folder apps or shoeboxes, work full-time, and need simple compliance frameworks without confusing financial jargon.

Conversion Strategy: Do not force an immediate software sale. Instead, capture their interest by pushing them to our free, pre-mapped T776 spreadsheet tool at [https://www.rentalops.ca/free-landlord-t776-excel-template](https://www.rentalops.ca/free-landlord-t776-excel-template). Introduce it as the free way to skip the spreadsheet-building headache.

OUTPUT FORMAT: You must output a single valid JSON object with these exact keys:
title, metaDescription, content, tags, persona, postType, cluster
The content value must be a single string with the full markdown article using escaped newlines (\\n). Do not output text outside the JSON object.""",
        },
        {
            "role": "user",
            "content": f"""Write a highly thorough, educational blog post about: {topic}

Requirements:
- PRIMARY KEYWORD: "{topic}" — must appear in the title, the first paragraph, and at least two H2 headings.
- metaDescription: 150-160 characters EXACTLY containing the primary keyword.
- Structural Depth: Minimum 1200 words. Do not write a quick overview. Fully break down the rules, regulations, and exact line-item definitions under the CRA framework.
- Core Sections to Include: 
  1. An empathetic introduction acknowledging how hard it is to track this while holding down a day job.
  2. 4-6 detailed body sections with practical financial examples using Canadian dollar amounts.
  3. A "Common Mistakes Small Landlords Make" section listing at least 3 specific errors (e.g., missing structural depreciation or misclassifying line items).
  4. A "Key Takeaways" summary list.
- Exact CRA Alignment: Use explicit CRA tax line references (such as Line 8520 for Advertising, Line 8710 for Interest, Line 8960 for Maintenance) to show absolute authority.
- Actionable Lead Magnet Call-To-Action: Conclude with an undeniable push to download the Free T776 Landlord Excel Template at [https://www.rentalops.ca/free-landlord-t776-excel-template](https://www.rentalops.ca/free-landlord-t776-excel-template). Explain that it sets up their record-keeping perfectly for their accountant. Position RentalOps automatic tracking software as the next seamless step to eliminate data entry entirely.{roi_instruction}{pillar_link_instruction}{internal_links_instruction}
- tags: array of 5 real Canadian landlord search terms.
- persona: "{persona['name']}"
- postType: "cluster"
- cluster: "{current_cluster or 'General'}"

Output only the JSON object. No text before or after it.""",
        },
    ]

    raw = call_groq(messages, max_tokens=6000, temperature=0.7, force_json_mode=False)
    blog_data = extract_json(raw)

    if not blog_data:
        return None

    required = ["title", "metaDescription", "content", "tags"]
    for field in required:
        if field not in blog_data:
            print(f"❌ Missing required field: {field}")
            return None

    blog_data["postType"] = "cluster"
    blog_data["cluster"] = current_cluster or "General"

    word_count = len(blog_data["content"].split())
    print(f"✅ Content generated. Word count: ~{word_count} words")

    if word_count < 600:
        return None
    return blog_data

# ─────────────────────────────────────────────
# CORE DISTRIBUTION CHANNEL PUBLISHING
# ─────────────────────────────────────────────
def publish_to_devto(blog_data, image_data, slug):
    print("📤 Publishing to Dev.to...")
    canonical_url = f"[https://www.rentalops.ca/blog/](https://www.rentalops.ca/blog/){slug}"

    if devto_canonical_exists(canonical_url):
        print(f"⚠️  Skipping Dev.to — already exists")
        return False, None

    content = blog_data["content"]
    if image_data:
        content = f"{content}\n\n---\n\n*{image_data['credit']}*"

    def clean_tag(tag):
        return tag.lower().replace(" ", "").replace("-", "").replace("/", "")[:20]

    tags = [clean_tag(t) for t in blog_data.get("tags", [])[:4]]

    article_payload = {
        "article": {
            "title": blog_data["title"],
            "body_markdown": content,
            "published": True,
            "description": blog_data["metaDescription"],
            "tags": tags,
            "main_image": image_data["url"] if image_data else None,
            "canonical_url": canonical_url,
        }
    }

    try:
        response = requests.post("[https://dev.to/api/articles](https://dev.to/api/articles)", headers={"api-key": DEVTO_API_KEY, "Content-Type": "application/json"}, json=article_payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Dev.to post published! URL: {result.get('url')}")
        return True, result.get("url")
    except Exception as e:
        print(f"❌ Error publishing to Dev.to: {e}")
        return False, None

def generate_linkedin_post(blog_data, blog_url):
    print("🔗 Generating LinkedIn post...")
    post_type = blog_data.get("postType", "cluster")
    cluster = blog_data.get("cluster", "")
    type_instruction = "This is a COMPREHENSIVE GUIDE. Hook should convey it is the definitive resource." if post_type == "pillar" else "Focused practical guide. Hook should speak directly to the specific line-item pain point."

    messages = [
        {
            "role": "system",
            "content": """You are a LinkedIn content writer for RentalOps, a Canadian landlord tax tool. Write human-to-human posts that feel like a property owner sharing value, not corporate sales jargon. Respond with JSON: {"post": "text"}""",
        },
        {
            "role": "user",
            "content": f"""Write a LinkedIn post. Title: {blog_data['title']}. Summary: {blog_data['metaDescription']}. URL: {blog_url}. Type: {type_instruction}. Max 200 words. Force an unscrollable first-line hook, reference real CRA/T776 pain points, and output exact JSON formatting.""",
        },
    ]
    raw = call_groq(messages, max_tokens=500, temperature=0.8, force_json_mode=True)
    if not raw: return None
    try:
        return json.loads(raw).get("post", "")
    except Exception: return None

def upload_image_to_linkedin(access_token, image_url, org_id):
    print("🖼️  Uploading image to LinkedIn...")
    try:
        image_response = requests.get(image_url, timeout=15)
        image_response.raise_for_status()
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0"}
        register_payload = {"registerUploadRequest": {"recipes": ["urn:li:digitalmediaRecipe:feedshare-image"], "owner": f"urn:li:organization:{org_id}", "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]}}
        register_response = requests.post("[https://api.linkedin.com/v2/assets?action=registerUpload](https://api.linkedin.com/v2/assets?action=registerUpload)", headers=headers, json=register_payload, timeout=15)
        register_response.raise_for_status()
        register_data = register_response.json()
        upload_url = register_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset_urn = register_data["value"]["asset"]
        requests.put(upload_url, headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/octet-stream"}, data=image_response.content, timeout=30).raise_for_status()
        return asset_urn
    except Exception as e:
        print(f"⚠️  Image upload failed: {e}")
        return None

def post_to_linkedin(post_text, image_url=None):
    print("📤 Posting to LinkedIn...")
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    org_id = os.environ.get("LINKEDIN_ORGANIZATION_ID")
    if not access_token or not org_id: return False

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0", "LinkedIn-Version": "202501"}
    image_urn = upload_image_to_linkedin(access_token, image_url, org_id.strip())
    author_urn = f"urn:li:organization:{org_id.strip()}"

    post_payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "IMAGE" if image_urn else "NONE",
                **({"media": [{"status": "READY", "media": image_urn, "mediaType": "urn:li:digitalmediaMediaType:image"}]} if image_urn else {})
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    try:
        requests.post("[https://api.linkedin.com/v2/ugcPosts](https://api.linkedin.com/v2/ugcPosts)", headers=headers, json=post_payload, timeout=15).raise_for_status()
        print("✅ Posted to LinkedIn successfully!")
        return True
    except Exception as e:
        print(f"❌ LinkedIn post failed: {e}")
        return False

def save_post_to_repo(blog_data, image_data, post_slug):
    try:
        os.makedirs("posts", exist_ok=True)
        post = {
            "title": blog_data["title"],
            "metaDescription": blog_data["metaDescription"],
            "content": blog_data["content"],
            "tags": blog_data.get("tags", []),
            "persona": blog_data.get("persona", ""),
            "postType": blog_data.get("postType", "cluster"),
            "cluster": blog_data.get("cluster", "General"),
            "coverImage": image_data["url"] if image_data else None,
            "coverImageCredit": image_data["credit"] if image_data else None,
            "publishedAt": datetime.now().isoformat(),
            "slug": post_slug,
        }
        filename = f"posts/{post_slug}.json"
        with open(filename, "w") as f:
            json.dump(post, f, indent=2)
        print(f"✅ Post saved to {filename}")
        return filename
    except Exception as e:
        print(f"⚠️  Could not save post: {e}")
        return None

def log_new_post_for_index(title: str, slug: str, topic: str, cluster: str):
    print("\n" + "─" * 60 + "\n📌 ADD THIS TO PUBLISHED_POSTS in blog_poster.py:\n" + "─" * 60)
    print(f"""    {{
        "slug": "{slug}",
        "title": "{title}",
        "topic": "{topic}",
        "cluster": "{cluster}",
    }},""")
    print("─" * 60 + "\n")

def main():
    print("=" * 60 + "\n🚀 RentalOps Blog Automation Starting...\n" + "=" * 60)
    is_pillar = False
    blog_data = None
    topic = None
    persona = get_current_persona()
    used_topics = get_used_topics()
    pending_pillar = get_pending_pillar()

    if pending_pillar:
        blog_data, topic = generate_pillar_content(pending_pillar)
        is_pillar = True
    else:
        for attempt in range(3):
            topic = pick_topic(persona, used_topics, offset=attempt)
            blog_data = generate_blog_content(topic, persona)
            if blog_data: break
            if attempt < 2: time.sleep(10)

    if not blog_data or not topic:
        return

    slug = generate_slug(blog_data["title"])
    image_data = get_unsplash_image(generate_image_query(blog_data["title"]))
    saved_file = save_post_to_repo(blog_data, image_data, slug)
    success, _ = publish_to_devto(blog_data, image_data, slug)

    if saved_file or success:
        save_used_topic(topic)
        if is_pillar and pending_pillar:
            save_published_pillar(pending_pillar["id"])

        blog_url = f"[https://www.rentalops.ca/blog/](https://www.rentalops.ca/blog/){slug}"
        log_new_post_for_index(blog_data["title"], slug, topic, blog_data.get("cluster", "General"))
        linkedin_text = generate_linkedin_post(blog_data, blog_url)
        if linkedin_text:
            post_to_linkedin(linkedin_text, image_data["url"] if image_data else None)

if __name__ == "__main__":
    main()
