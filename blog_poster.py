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
# PERSONAS
# ─────────────────────────────────────────────
PERSONAS = [
    {
        "name": "First-Time Landlord",
        "description": "Someone who recently became a landlord and is overwhelmed by taxes, compliance, and paperwork. Has 1-2 properties.",
        "topics": [
            "rental property tax deductions Canada 2026",
            "how to fill out T776 form Canada step by step",
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
        ],
    },
    {
        "name": "Portfolio Builder",
        "description": "A small landlord with 2-5 properties looking to manage efficiently and minimize tax burden without an accountant for every question.",
        "topics": [
            "tracking rental income expenses multiple properties Canada",
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
            "mileage travel deductions landlord Canada",
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
# Comprehensive 3000+ word guides that anchor
# each topic cluster. Written once per cluster.
# ─────────────────────────────────────────────
PILLAR_POSTS = [
    {
        "id": "cra-tax-pillar",
        "cluster": "CRA Tax & Reporting",
        "topic": "rental income tax Canada complete guide small landlords 2026",
        "title_hint": "Rental Income Tax in Canada: Complete Guide for Small Landlords (2026)",
        "description": "The definitive guide covering everything a 1-5 property Canadian landlord needs to know about rental income tax, T776, CRA compliance, and deductions.",
        "target_word_count": 3500,
        "cluster_posts": [
            "rental property tax deductions Canada 2026",
            "how to fill out T776 form Canada step by step",
            "CRA audit rental income what triggers it Canada",
            "is rental income taxable in Canada",
            "landlord tax deductions Canada complete guide",
            "failing to report rental income CRA consequences",
            "year end tax checklist Canadian landlords multiple properties",
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
# Add new entries after each post publishes
# (the log at end of each run tells you what to add)
# ─────────────────────────────────────────────
PUBLISHED_POSTS = [
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

# ─────────────────────────────────────────────
# PILLAR POST TRACKING
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# USED TOPICS
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# SLUG GENERATION
# ─────────────────────────────────────────────
def generate_slug(title: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    if len(slug) > 70:
        slug = slug[:70]
        last_hyphen = slug.rfind('-')
        if last_hyphen > 40:
            slug = slug[:last_hyphen]
    return slug


# ─────────────────────────────────────────────
# PERSONA SELECTION
# ─────────────────────────────────────────────
def get_current_persona():
    day_of_year = datetime.now().timetuple().tm_yday
    persona_index = day_of_year % len(PERSONAS)
    return PERSONAS[persona_index]


# ─────────────────────────────────────────────
# INTERNAL LINKS BUILDER
# Prioritises same-cluster posts
# ─────────────────────────────────────────────
def get_internal_links(current_topic: str, current_cluster: str = None) -> str:
    BASE_URL = "https://www.rentalops.ca/blog"

    candidates = [p for p in PUBLISHED_POSTS if p["topic"] != current_topic]

    current_words = set(current_topic.lower().split())
    scored = []
    for post in candidates:
        post_words = set(post["topic"].lower().split())
        keyword_score = len(current_words & post_words)
        cluster_bonus = 2 if (
            current_cluster and post.get("cluster") == current_cluster
        ) else 0
        scored.append((keyword_score + cluster_bonus, post))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [p for _, p in scored[:3]]

    if not selected:
        return ""

    links_block = "\n".join(
        f'- [{p["title"]}]({BASE_URL}/{p["slug"]})'
        for p in selected
    )
    return f"""
- Naturally include 2-3 internal links to related RentalOps blog posts within the article body.
  Use the anchor text and URLs exactly as listed below.
  Only link where it makes contextual sense — do NOT force links:
{links_block}"""


# ─────────────────────────────────────────────
# PILLAR POST INTERNAL LINKS
# ─────────────────────────────────────────────
def get_pillar_internal_links(pillar: dict) -> str:
    BASE_URL = "https://www.rentalops.ca/blog"
    links = pillar.get("internal_links", [])
    if not links:
        return ""
    links_block = "\n".join(
        f'- [{l["title"]}]({BASE_URL}/{l["slug"]})'
        for l in links
    )
    return f"""
- This is a PILLAR post. Link to these related cluster posts naturally within the content:
{links_block}
- Also mention that readers can explore the full RentalOps blog for more detailed guides on each sub-topic."""


# ─────────────────────────────────────────────
# CHECK IF PILLAR POST IS DUE TODAY
# Runs on day 1 and day 15 of each month
# Only if that pillar hasn't been written yet
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# IMAGE QUERY GENERATOR
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# UNSPLASH
# ─────────────────────────────────────────────
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
        credit = (
            f"Photo by [{photographer}]"
            f"(https://unsplash.com/@{data['user']['username']}) "
            f"on [Unsplash](https://unsplash.com)"
        )
        print(f"✅ Image found by {photographer}")
        return {"url": image_url, "credit": credit}
    except Exception as e:
        print(f"⚠️  Unsplash fetch failed: {e}")
        return None


# ─────────────────────────────────────────────
# GROQ API — shared helper
# max_tokens set to 6000 to allow 1800-2500
# word posts without truncation
# ─────────────────────────────────────────────
def call_groq(
    messages: list,
    max_tokens: int = 6000,
    temperature: float = 0.7
) -> str | None:
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
        "response_format": {"type": "json_object"},
    }
    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=120
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Groq API call failed: {e}")
        return None


# ─────────────────────────────────────────────
# PILLAR POST GENERATION
# 3000-3500 words, comprehensive guide format
# ─────────────────────────────────────────────
def generate_pillar_content(pillar: dict):
    print(f"📌 Generating PILLAR post: {pillar['cluster']}")
    print(f"   Topic: {pillar['topic']}")

    internal_links_instruction = get_pillar_internal_links(pillar)
    cluster_posts_list = "\n".join(
        f"  - {t}" for t in pillar["cluster_posts"]
    )

    messages = [
        {
            "role": "system",
            "content": f"""You are a senior content strategist for RentalOps, a Canadian landlord 
expense tracking and tax preparation tool built for small landlords with 1-5 properties.

Your audience: Canadian landlords who are NOT accountants. They are regular people 
who own 1-5 rental properties and are overwhelmed by CRA rules, T776 forms, and 
provincial regulations. They need plain-English education, not jargon.

Your job: Write the definitive pillar guide on this topic. It must be so thorough 
and helpful that a landlord bookmarks it and shares it with other landlords.

RentalOps mission: Educate landlords so they understand their obligations, then 
show them how RentalOps makes compliance effortless — accurate T776 filing, 
expense tracking, and CRA-compliant records without needing an accountant for 
every question.

You MUST respond with ONLY valid JSON. No markdown fences. Raw JSON only.""",
        },
        {
            "role": "user",
            "content": f"""Write a comprehensive PILLAR blog post for the topic cluster: "{pillar['cluster']}"

Suggested title: {pillar['title_hint']}
Core topic: {pillar['topic']}
Post description: {pillar['description']}

This pillar post must cover these sub-topics (each will have its own dedicated 
blog post that links back to this pillar):
{cluster_posts_list}

Requirements:
- PRIMARY KEYWORD: "{pillar['topic']}" — use in title, first paragraph, and 2+ H2 headings
- Title: Use the suggested title above or very close variant. Keep under 70 characters.
- Meta description: 150-160 characters EXACTLY. Include primary keyword. End with a benefit.
- Content: 3000-3500 words minimum. This is a comprehensive reference guide.
- Tone: Plain English. Reassuring not scary. Written for a non-accountant landlord.
  Avoid jargon. When you must use tax terms explain them immediately.
- Structure:
    * Introduction — Why this matters for small landlords specifically (1-5 properties)
      Hook with a relatable scenario (e.g. "You just got your first rent cheque...")
      Use primary keyword in first 100 words
    * 5-7 H2 sections covering the sub-topics listed above
      Each H2 section 300-500 words with H3 sub-sections
    * "Quick Reference" section — bullet list of the most important rules/numbers
    * "Common Mistakes Small Landlords Make" section — specific and actionable
    * "Key Takeaways" section — 5-7 bullet points summarising everything
    * Conclusion with strong CTA to try RentalOps free
- Include real Canadian numbers: CRA deadlines, T776 line numbers, CAD amounts,
  provincial rule references, penalty amounts where relevant
- Mention RentalOps 3-4 times naturally — each tied to a specific pain point{internal_links_instruction}
- Tags: 5 highly specific SEO tags (real search terms, not generic words)

Return ONLY this JSON:
{{
  "title": "...",
  "metaDescription": "...",
  "content": "... full markdown 3000-3500 words ...",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "persona": "Small Landlord",
  "postType": "pillar",
  "cluster": "{pillar['cluster']}"
}}

CRITICAL:
- metaDescription must be 150-160 characters exactly. Count carefully.
- content must be 3000-3500 words. Do not cut short under any circumstances.
- Raw JSON only — no markdown fences, no commentary outside the JSON.""",
        },
    ]

    raw = call_groq(messages, max_tokens=8000, temperature=0.65)
    if not raw:
        return None, None

    try:
        blog_data = json.loads(raw)
        required = ["title", "metaDescription", "content", "tags"]
        for field in required:
            if field not in blog_data:
                print(f"❌ Missing field in pillar response: {field}")
                return None, None

        word_count = len(blog_data["content"].split())
        print(f"✅ Pillar content generated")
        print(f"   Title: {blog_data['title'][:70]}")
        print(f"   Meta ({len(blog_data['metaDescription'])} chars): {blog_data['metaDescription']}")
        print(f"   Word count: ~{word_count} words")
        print(f"   Tags: {', '.join(blog_data['tags'])}")

        if word_count < 2500:
            print(f"⚠️  WARNING: Pillar only {word_count} words — target is 3000-3500")

        return blog_data, pillar["topic"]

    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error on pillar: {e}")
        return None, None


# ─────────────────────────────────────────────
# REGULAR BLOG POST GENERATION
# 1800-2500 words, cluster-aware
# Returns None, None if word count too low
# so main() can retry
# ─────────────────────────────────────────────
def generate_blog_content():
    persona = get_current_persona()
    print(f"🎯 Target persona: {persona['name']}")

    used_topics = get_used_topics()
    available_topics = [t for t in persona["topics"] if t not in used_topics]

    if not available_topics:
        print(f"🔄 All topics for {persona['name']} used — resetting")
        available_topics = persona["topics"]

    day_of_year = datetime.now().timetuple().tm_yday
    topic_index = day_of_year % len(available_topics)
    topic = available_topics[topic_index]

    print(f"🤖 Generating content about: {topic}")

    # Determine cluster for this topic
    current_cluster = None
    for pillar in PILLAR_POSTS:
        if topic in pillar["cluster_posts"]:
            current_cluster = pillar["cluster"]
            break
    print(f"🗂️  Cluster: {current_cluster or 'General'}")

    # Link back to pillar if it has been published
    pillar_link_instruction = ""
    published_pillars = get_published_pillars()
    for pillar in PILLAR_POSTS:
        if (
            pillar["cluster"] == current_cluster
            and pillar["id"] in published_pillars
        ):
            pillar_slug = generate_slug(pillar["title_hint"])
            pillar_link_instruction = f"""
- This post is part of the "{pillar['cluster']}" cluster.
  Link back to the pillar guide naturally once in the article:
  [{pillar['title_hint']}](https://www.rentalops.ca/blog/{pillar_slug})
  Use anchor text that fits naturally in context."""
            break

    include_roi = random.random() < 0.3
    roi_instruction = ""
    if include_roi:
        roi_instruction = """
- Include a section: "What This Costs You Without the Right Tools"
  Compare doing this manually (time + risk of errors) vs using RentalOps.
  Be specific: e.g. "2-3 hours per month tracking receipts manually 
  vs RentalOps doing it automatically for $6.99/month".
  Include RentalOps pricing starting at $6.99/month."""

    print(f"💰 ROI/cost section: {'Yes' if include_roi else 'No'}")

    internal_links_instruction = get_internal_links(topic, current_cluster)

    messages = [
        {
            "role": "system",
            "content": f"""You are a content writer for RentalOps, a Canadian landlord expense 
tracking and tax preparation tool designed for small landlords with 1-5 properties.

Your audience: Regular Canadians who own 1-5 rental properties. They are NOT 
accountants. They are confused about CRA rules, worried about audits, and just 
want to do things right without hiring expensive help for every question.

Your tone: Plain English. Reassuring and practical. Like a knowledgeable friend 
explaining things — not a textbook or a lawyer. Use real numbers, real examples, 
real Canadian context (CRA, T776, LTB, CAD amounts, provincial rules).

RentalOps helps landlords track income/expenses, prepare for tax season, file 
T776 accurately, and stay CRA-compliant — without the guesswork.

Target persona: {persona['name']} — {persona['description']}
You MUST respond with ONLY valid JSON. No markdown fences. Raw JSON only.""",
        },
        {
            "role": "user",
            "content": f"""Write a complete blog post about: {topic}

Remember the reader: A Canadian landlord with 1-5 properties who is NOT an 
accountant and is genuinely confused or worried about this topic. Start from 
their perspective — acknowledge the confusion, then educate clearly.

Requirements:
- PRIMARY KEYWORD: "{topic}" — use this exact phrase or very close variant
  in the title, first paragraph, and at least 2 H2 headings
- Title: Natural, keyword-first. Under 65 characters if possible.
  Format options:
    "[Keyword]: What Canadian Landlords Need to Know"
    "[Year] Guide: [Keyword] for Small Landlords"
    "The Small Landlord's Guide to [Keyword]"
- Meta description: 150-160 characters EXACTLY.
  Include primary keyword. End with a clear benefit or action.
- Content: 1800-2500 words in markdown.
  YOU MUST WRITE AT LEAST 1800 WORDS. This is a firm requirement.
  Do not stop early. If you are approaching the end of a section,
  add more detail, examples, or sub-sections before moving on.
- Tone: Plain English. Conversational. Reassuring not scary.
  Explain every tax term the first time you use it.
- Structure:
    * Introduction — relatable hook (scenario or question the reader faces)
      Primary keyword in first 100 words
    * 4-6 H2 sections — keyword variants in headings
      Each section with H3 sub-headings where it helps clarity
      Each H2 section must be at least 250 words
    * Real Canadian numbers: CRA deadlines, T776 line numbers,
      penalty amounts, CAD dollar examples
    * "Common Mistakes" section — at least 3 specific mistakes small landlords make
    * "Key Takeaways" — 5 bullet points max, plain English
    * Conclusion — strong CTA to try RentalOps free{roi_instruction}{pillar_link_instruction}{internal_links_instruction}
- Mention RentalOps 2-3 times naturally — each tied to a specific pain point
- Tags: 5 SEO tags — real search terms, specific to Canada

Return ONLY this JSON:
{{
  "title": "...",
  "metaDescription": "...",
  "content": "... full markdown minimum 1800 words ...",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "persona": "{persona['name']}",
  "postType": "cluster",
  "cluster": "{current_cluster or 'General'}"
}}

CRITICAL:
- metaDescription must be 150-160 characters. Count carefully.
- content must be minimum 1800 words. Count carefully. Do not stop early.
- Raw JSON only — no markdown fences, no commentary.""",
        },
    ]

    raw = call_groq(messages, max_tokens=6000, temperature=0.7)
    if not raw:
        return None, None

    try:
        blog_data = json.loads(raw)
        required = ["title", "metaDescription", "content", "tags"]
        for field in required:
            if field not in blog_data:
                print(f"❌ Missing required field: {field}")
                return None, None

        word_count = len(blog_data["content"].split())
        print(f"✅ Content generated successfully")
        print(f"   Persona: {persona['name']}")
        print(f"   Cluster: {blog_data.get('cluster', 'General')}")
        print(f"   Title: {blog_data['title'][:70]}")
        print(
            f"   Meta ({len(blog_data['metaDescription'])} chars): "
            f"{blog_data['metaDescription']}"
        )
        print(f"   Tags: {', '.join(blog_data['tags'])}")
        print(f"   Word count: ~{word_count} words")

        if word_count < 1200:
            print(
                f"⚠️  Word count too low ({word_count} words) — "
                f"returning None to trigger retry"
            )
            return None, None

        return blog_data, topic

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        return None, None


# ─────────────────────────────────────────────
# PUBLISH TO DEV.TO
# canonical_url ensures SEO credit goes to
# rentalops.ca not Dev.to
# ─────────────────────────────────────────────
def publish_to_devto(blog_data, image_data, slug):
    print("📤 Publishing to Dev.to...")

    content = blog_data["content"]
    if image_data:
        content = f"{content}\n\n---\n\n*{image_data['credit']}*"

    def clean_tag(tag):
        return tag.lower().replace(" ", "").replace("-", "").replace("/", "")[:20]

    tags = [clean_tag(t) for t in blog_data.get("tags", [])[:4]]
    canonical_url = f"https://www.rentalops.ca/blog/{slug}"

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
        response = requests.post(
            "https://dev.to/api/articles",
            headers={
                "api-key": DEVTO_API_KEY,
                "Content-Type": "application/json",
            },
            json=article_payload,
            timeout=30,
        )

        if response.status_code not in [200, 201]:
            print(f"❌ Dev.to returned status {response.status_code}")
            print(f"❌ Dev.to response: {response.text}")

        response.raise_for_status()
        result = response.json()
        post_url = result.get("url", "https://dev.to")
        print(f"✅ Dev.to post published!")
        print(f"🔗 Dev.to URL: {post_url}")
        print(f"🏠 Canonical: {canonical_url}")
        return True, post_url

    except Exception as e:
        print(f"❌ Error publishing to Dev.to: {e}")
        return False, None


# ─────────────────────────────────────────────
# LINKEDIN
# ─────────────────────────────────────────────
def generate_linkedin_post(blog_data, blog_url):
    print("🔗 Generating LinkedIn post...")

    post_type = blog_data.get("postType", "cluster")
    cluster = blog_data.get("cluster", "")

    if post_type == "pillar":
        type_instruction = (
            "This is a COMPREHENSIVE GUIDE (pillar post). "
            "The hook should reflect that this is the definitive resource. "
            'e.g. "I just published the most complete guide to [topic] '
            'for Canadian landlords..." Emphasise depth and completeness.'
        )
    else:
        type_instruction = (
            "This is a focused practical guide on one specific topic. "
            "The hook should speak directly to the pain point. "
            'e.g. "Did you know most Canadian landlords miss this deduction?" '
            "Be specific and relatable."
        )

    messages = [
        {
            "role": "system",
            "content": """You are a LinkedIn content writer for RentalOps, a Canadian landlord 
tax and expense tracking tool for small landlords with 1-5 properties.
Write posts that feel human and real — like a landlord sharing something 
useful with other landlords. Not corporate. Not salesy.
You MUST respond with ONLY valid JSON. No markdown fences. Raw JSON only.""",
        },
        {
            "role": "user",
            "content": f"""Write a LinkedIn post for this blog article.

Blog title: {blog_data['title']}
Blog summary: {blog_data['metaDescription']}
Target persona: {blog_data.get('persona', 'Canadian landlord')}
Cluster: {cluster}
Article URL: {blog_url}

Post type guidance: {type_instruction}

Rules:
- 150-200 words maximum
- First line is the hook — make it impossible to scroll past
- Write as if you are a landlord sharing something useful, not a marketer
- Reference specific Canadian context (CRA, T776, Ontario LTB, etc.)
- One clear call to action at the end linking to the article
- 4-5 relevant hashtags on the last line
- Zero corporate buzzwords

Return ONLY this JSON:
{{
  "post": "full linkedin post text including hashtags"
}}""",
        },
    ]

    raw = call_groq(messages, max_tokens=500, temperature=0.8)
    if not raw:
        return None
    try:
        post_data = json.loads(raw)
        linkedin_text = post_data.get("post", "")
        print(f"✅ LinkedIn post generated ({len(linkedin_text)} chars)")
        return linkedin_text
    except Exception as e:
        print(f"⚠️  LinkedIn post generation failed: {e}")
        return None


def upload_image_to_linkedin(access_token, image_url, org_id):
    print("🖼️  Uploading image to LinkedIn...")

    try:
        # Download image first
        image_response = requests.get(image_url, timeout=15)
        image_response.raise_for_status()
        image_bytes = image_response.content

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

        # Register upload using the stable assets API
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:organization:{org_id}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }
                ],
            }
        }

        register_response = requests.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers=headers,
            json=register_payload,
            timeout=15,
        )
        register_response.raise_for_status()
        register_data = register_response.json()

        upload_url = register_data["value"]["uploadMechanism"][
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]
        asset_urn = register_data["value"]["asset"]

        # Upload image bytes
        upload_response = requests.put(
            upload_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/octet-stream",
            },
            data=image_bytes,
            timeout=30,
        )
        upload_response.raise_for_status()

        print(f"✅ Image uploaded to LinkedIn — asset: {asset_urn}")
        return asset_urn

    except Exception as e:
        print(f"⚠️  Image upload failed — posting without image: {e}")
        return None


def post_to_linkedin(post_text, image_url=None):
    print("📤 Posting to LinkedIn...")

    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    org_id = os.environ.get("LINKEDIN_ORGANIZATION_ID")

    if not access_token:
        print("⚠️  LINKEDIN_ACCESS_TOKEN not set — skipping")
        return False
    if not org_id:
        print("⚠️  LINKEDIN_ORGANIZATION_ID not set — skipping")
        return False

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202501",
    }

    try:
        profile_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers=headers,
            timeout=10,
        )
        profile_response.raise_for_status()
        member_id = profile_response.json().get("sub")
        if not member_id:
            print("❌ Could not retrieve LinkedIn member ID")
            return False
        print("👤 LinkedIn member ID found")
    except Exception as e:
        print(f"❌ Failed to get LinkedIn profile: {e}")
        return False

    image_urn = None
    if image_url:
        image_urn = upload_image_to_linkedin(access_token, image_url, org_id)

    author_urn = f"urn:li:organization:{org_id}"

    if image_urn:
        post_payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": post_text},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": image_urn,
                            "mediaType": "urn:li:digitalmediaMediaType:image",
                        }
                    ],
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }
    else:
        post_payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": post_text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }

    try:
        post_response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json=post_payload,
            timeout=15,
        )
        if post_response.status_code not in [200, 201]:
            print(f"❌ LinkedIn post failed: {post_response.status_code}")
            print(f"❌ Response: {post_response.text}")
            return False
        print("✅ Posted to LinkedIn successfully!")
        return True
    except Exception as e:
        print(f"❌ LinkedIn post failed: {e}")
        return False


# ─────────────────────────────────────────────
# SAVE POST TO REPO
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# TRIGGER VERCEL REDEPLOY
# Kept as utility — primary trigger is the
# GitHub Actions workflow step after git push
# ─────────────────────────────────────────────
def trigger_vercel_redeploy():
    hook_url = os.environ.get("VERCEL_DEPLOY_HOOK_URL")
    if not hook_url:
        print("⚠️  VERCEL_DEPLOY_HOOK_URL not set — skipping")
        return False
    try:
        print("🚀 Triggering Vercel redeploy...")
        response = requests.post(hook_url, timeout=15)
        if response.status_code in [200, 201]:
            job_id = response.json().get("job", {}).get("id", "unknown")
            print(f"✅ Vercel redeploy triggered! Job ID: {job_id}")
            return True
        print(f"❌ Vercel hook returned: {response.status_code}")
        return False
    except Exception as e:
        print(f"❌ Vercel redeploy failed: {e}")
        return False


# ─────────────────────────────────────────────
# LOG NEW POST FOR INDEX
# ─────────────────────────────────────────────
def log_new_post_for_index(title: str, slug: str, topic: str, cluster: str):
    print("\n" + "─" * 60)
    print("📌 ADD THIS TO PUBLISHED_POSTS in blog_poster.py:")
    print("─" * 60)
    print(f"""    {{
        "slug": "{slug}",
        "title": "{title}",
        "topic": "{topic}",
        "cluster": "{cluster}",
    }},""")
    print("─" * 60 + "\n")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("🚀 RentalOps Blog Automation Starting...")
    print("=" * 60)

    is_pillar = False
    blog_data = None
    topic = None

    # Check if a pillar post is due today
    pending_pillar = get_pending_pillar()

    if pending_pillar:
        print(f"\n📌 PILLAR POST MODE — {pending_pillar['cluster']}")
        blog_data, topic = generate_pillar_content(pending_pillar)
        is_pillar = True
    else:
        print(f"\n📝 REGULAR POST MODE")
        # Retry up to 2 times if content comes back too short
        for attempt in range(1, 3):
            print(f"   Attempt {attempt}/2...")
            blog_data, topic = generate_blog_content()
            if blog_data and topic:
                break
            if attempt < 2:
                print(f"   Content too short or failed — retrying in 15 seconds...")
                time.sleep(15)

    if not blog_data or not topic:
        print("❌ Failed to generate content after all attempts. Exiting.")
        print("\n" + "=" * 60)
        print("❌ Blog post automation failed.")
        print("=" * 60)
        return

    # Generate slug
    slug = generate_slug(blog_data["title"])
    print(f"🔗 Slug: {slug}")

    # Get cover image
    image_search_query = generate_image_query(blog_data["title"])
    image_data = get_unsplash_image(image_search_query)

    # Save post to repo
    saved_file = save_post_to_repo(blog_data, image_data, slug)

    # Publish to Dev.to with canonical URL pointing to rentalops.ca
    success, post_url = publish_to_devto(blog_data, image_data, slug)

    if saved_file or success:
        save_used_topic(topic)

        # Mark pillar as done so it never runs again
        if is_pillar and pending_pillar:
            save_published_pillar(pending_pillar["id"])

        blog_url = f"https://www.rentalops.ca/blog/{slug}"
        cluster = blog_data.get("cluster", "General")

        # Log entry to add to PUBLISHED_POSTS
        log_new_post_for_index(blog_data["title"], slug, topic, cluster)

        # LinkedIn
        linkedin_text = generate_linkedin_post(blog_data, blog_url)
        if linkedin_text:
            post_to_linkedin(
                linkedin_text,
                image_data["url"] if image_data else None,
            )

        print("\n" + "=" * 60)
        post_type_label = "PILLAR" if is_pillar else "CLUSTER"
        print(f"✅ [{post_type_label}] Blog post automation completed!")
        print(f"🔗 Will be live at: {blog_url}")
        print(f"🗂️  Cluster: {cluster}")
        print(f"🗺️  Vercel redeploy triggered by GitHub Actions after commit")
        print("=" * 60)

    else:
        print("\n" + "=" * 60)
        print("❌ Blog post automation failed.")
        print("=" * 60)


if __name__ == "__main__":
    main()
