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
# PERSONA AND TOPIC SELECTION
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# INTERNAL LINKS BUILDER
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
# PILLAR INTERNAL LINKS
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
- Also mention readers can explore the RentalOps blog for detailed guides on each sub-topic."""


# ─────────────────────────────────────────────
# CHECK IF PILLAR IS DUE TODAY
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
#
# KEY CHANGE: response_format is NOT used for
# content generation calls. Removing JSON mode
# gives the model its full token budget for
# content instead of spending tokens on JSON
# structure overhead. We parse JSON manually.
#
# JSON mode IS still used for short structured
# responses (LinkedIn post) where length is not
# a concern.
# ─────────────────────────────────────────────
def call_groq(
    messages: list,
    max_tokens: int = 6000,
    temperature: float = 0.7,
    force_json_mode: bool = False,
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
    }
    # Only add JSON mode for short structured calls
    # NOT for long content generation
    if force_json_mode:
        payload["response_format"] = {"type": "json_object"}

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
# JSON EXTRACTOR
# Pulls JSON from model response even when the
# model adds markdown fences or preamble text.
# Needed because we removed response_format
# for content generation calls.
# ─────────────────────────────────────────────
def extract_json(raw: str) -> dict | None:
    if not raw:
        return None

    # Strip markdown code fences if present
    cleaned = re.sub(r'^```(?:json)?\s*', '', raw.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r'\s*```$', '', cleaned.strip(), flags=re.MULTILINE)

    # Try direct parse first
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Find the first { and last } and try parsing that block
    start = cleaned.find('{')
    end = cleaned.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start:end + 1])
        except json.JSONDecodeError:
            pass

    print(f"❌ Could not extract JSON from response (first 300 chars): {raw[:300]}")
    return None


# ─────────────────────────────────────────────
# DEV.TO DUPLICATE CHECK
# Check if a canonical URL is already taken
# before attempting to publish
# ─────────────────────────────────────────────
def devto_canonical_exists(canonical_url: str) -> bool:
    """
    Returns True if Dev.to already has an article
    with this canonical URL — so we skip publishing.
    Uses the Dev.to API to search our own articles.
    """
    if not DEVTO_API_KEY:
        return False
    try:
        response = requests.get(
            "https://dev.to/api/articles/me/published",
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
        # If check fails, attempt publish anyway
        return False


# ─────────────────────────────────────────────
# PILLAR POST GENERATION
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
            "content": """You are a senior content strategist for RentalOps, a Canadian landlord
expense tracking and tax preparation tool for small landlords with 1-5 properties.

Audience: Canadian landlords who are NOT accountants. Regular people overwhelmed
by CRA rules, T776 forms, and provincial regulations. Need plain-English education.

Write the definitive pillar guide — so thorough a landlord bookmarks and shares it.

RentalOps mission: Educate landlords on their obligations, then show how RentalOps
makes compliance effortless — T776 filing, expense tracking, CRA-compliant records.

IMPORTANT: Respond with a JSON object. Use this exact structure:
{"title": "...", "metaDescription": "...", "content": "...", "tags": [...], "persona": "...", "postType": "pillar", "cluster": "..."}
The content field must contain the full markdown article.""",
        },
        {
            "role": "user",
            "content": f"""Write a comprehensive PILLAR blog post for cluster: "{pillar['cluster']}"

Suggested title: {pillar['title_hint']}
Core topic: {pillar['topic']}
Description: {pillar['description']}

Sub-topics — write a full H2 section (400+ words) for each:
{cluster_posts_list}

Requirements:
- PRIMARY KEYWORD: "{pillar['topic']}" — in title, first paragraph, 2+ H2 headings
- Title: Use suggested title or close variant. Under 70 characters.
- metaDescription: 150-160 characters EXACTLY. Primary keyword included. Ends with benefit.
- content: Full markdown article, minimum 3000 words.
  Write every section in full — do not summarise or skip content.
  Each H2 section must be at least 400 words with H3 sub-sections.
- Tone: Plain English. Reassuring. Explain every tax term on first use.
- Include: Introduction with hook, 5-7 H2 sections, Quick Reference section,
  Common Mistakes section (3+ mistakes), Key Takeaways (5-7 bullets), CTA conclusion
- Real Canadian numbers: CRA deadlines, T776 line numbers, CAD amounts, penalties
- Mention RentalOps 3-4 times naturally tied to specific pain points{internal_links_instruction}
- tags: array of 5 specific SEO search terms used by Canadian landlords

Return a single JSON object. No markdown fences around it. Just the raw JSON.""",
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

    # Ensure postType and cluster are set
    blog_data["postType"] = "pillar"
    blog_data["cluster"] = pillar["cluster"]

    word_count = len(blog_data["content"].split())
    print(f"✅ Pillar content generated")
    print(f"   Title: {blog_data['title'][:70]}")
    print(f"   Meta ({len(blog_data['metaDescription'])} chars): {blog_data['metaDescription']}")
    print(f"   Word count: ~{word_count} words")
    print(f"   Tags: {', '.join(blog_data['tags'])}")

    if word_count < 2000:
        print(f"⚠️  WARNING: Pillar only {word_count} words — target is 3000+")

    return blog_data, pillar["topic"]


# ─────────────────────────────────────────────
# REGULAR BLOG POST GENERATION
# ─────────────────────────────────────────────
def generate_blog_content(topic: str, persona: dict):
    print(f"🎯 Target persona: {persona['name']}")
    print(f"🤖 Generating content about: {topic}")

    # Determine cluster
    current_cluster = None
    for pillar in PILLAR_POSTS:
        if topic in pillar["cluster_posts"]:
            current_cluster = pillar["cluster"]
            break
    print(f"🗂️  Cluster: {current_cluster or 'General'}")

    # Link back to pillar if published
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
  [{pillar['title_hint']}](https://www.rentalops.ca/blog/{pillar_slug})"""
            break

    include_roi = random.random() < 0.3
    roi_instruction = ""
    if include_roi:
        roi_instruction = """
- Include a section: "What This Costs You Without the Right Tools"
  Compare manual effort vs RentalOps. Be specific with time and money.
  e.g. "2-3 hours/month tracking receipts manually vs $6.99/month for RentalOps"."""

    print(f"💰 ROI/cost section: {'Yes' if include_roi else 'No'}")

    internal_links_instruction = get_internal_links(topic, current_cluster)

    messages = [
        {
            "role": "system",
            "content": f"""You are a content writer for RentalOps, a Canadian landlord expense
tracking and tax preparation tool for small landlords with 1-5 properties.

Audience: Regular Canadians with 1-5 rental properties. NOT accountants.
Confused about CRA rules, worried about audits, want to do things right.

Tone: Plain English. Reassuring and practical. Real numbers, real Canadian context.
RentalOps helps track income/expenses, file T776 accurately, stay CRA-compliant.

Persona: {persona['name']} — {persona['description']}

IMPORTANT: Respond with a JSON object using this exact structure:
{{"title": "...", "metaDescription": "...", "content": "...", "tags": [...], "persona": "...", "postType": "cluster", "cluster": "..."}}
The content field must contain the full markdown article with all sections complete.""",
        },
        {
            "role": "user",
            "content": f"""Write a complete, thorough blog post about: {topic}

The reader is a Canadian landlord with 1-5 properties — NOT an accountant —
who is confused or worried about this topic.

Requirements:
- PRIMARY KEYWORD: "{topic}" — in title, first paragraph, at least 2 H2 headings
- title: Natural, keyword-first. Under 65 characters if possible.
- metaDescription: 150-160 characters EXACTLY. Primary keyword included.
- content: Write a THOROUGH article. Do not stop after a brief overview.
  Each section must be fully developed with real examples and Canadian specifics.
  Write until the topic is completely covered. Do not end early.
  Minimum expectation: Introduction + 4-6 full H2 sections + Mistakes + Takeaways + CTA.
  Each H2 section must be at least 200 words with examples.
- Tone: Plain English. Conversational. Explain every tax term on first use.
- Include throughout: CRA deadlines, T776 line numbers, CAD dollar examples,
  provincial rule references, specific penalty amounts
- "Common Mistakes" section: at least 3 specific mistakes small landlords make
- "Key Takeaways": up to 5 bullet points, plain English
- Conclusion: strong CTA to try RentalOps free{roi_instruction}{pillar_link_instruction}{internal_links_instruction}
- Mention RentalOps 2-3 times naturally tied to specific pain points
- tags: array of 5 real Canadian landlord search terms

Return a single JSON object. No markdown fences. Just the raw JSON.""",
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

    # Ensure postType and cluster are always set
    blog_data["postType"] = "cluster"
    blog_data["cluster"] = current_cluster or "General"

    word_count = len(blog_data["content"].split())
    print(f"✅ Content generated")
    print(f"   Cluster: {blog_data.get('cluster', 'General')}")
    print(f"   Title: {blog_data['title'][:70]}")
    print(
        f"   Meta ({len(blog_data['metaDescription'])} chars): "
        f"{blog_data['metaDescription']}"
    )
    print(f"   Tags: {', '.join(blog_data['tags'])}")
    print(f"   Word count: ~{word_count} words")

    if word_count < 600:
        print(f"⚠️  Word count critically low ({word_count}) — skipping")
        return None

    if word_count < 1000:
        print(f"⚠️  Word count below target ({word_count} words) — publishing anyway")

    return blog_data


# ─────────────────────────────────────────────
# PUBLISH TO DEV.TO
# Checks for duplicate canonical before posting
# ─────────────────────────────────────────────
def publish_to_devto(blog_data, image_data, slug):
    print("📤 Publishing to Dev.to...")

    canonical_url = f"https://www.rentalops.ca/blog/{slug}"

    # Check if this canonical URL is already on Dev.to
    if devto_canonical_exists(canonical_url):
        print(f"⚠️  Dev.to already has a post with canonical: {canonical_url}")
        print(f"   Skipping Dev.to — post already exists there")
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
            "This is a COMPREHENSIVE GUIDE. "
            "Hook should convey it is the definitive resource on this topic."
        )
    else:
        type_instruction = (
            "This is a focused practical guide. "
            "Hook should speak directly to the specific pain point."
        )

    messages = [
        {
            "role": "system",
            "content": """You are a LinkedIn content writer for RentalOps, a Canadian landlord
tax and expense tracking tool for small landlords with 1-5 properties.
Write posts that feel human — like a landlord sharing something useful with others.
Not corporate. Not salesy.
Respond with a JSON object: {"post": "full linkedin post text including hashtags"}""",
        },
        {
            "role": "user",
            "content": f"""Write a LinkedIn post for this blog article.

Title: {blog_data['title']}
Summary: {blog_data['metaDescription']}
Persona: {blog_data.get('persona', 'Canadian landlord')}
Cluster: {cluster}
URL: {blog_url}
Type guidance: {type_instruction}

Rules:
- 150-200 words maximum
- First line is the hook — impossible to scroll past
- Human voice — landlord sharing with landlords, not marketing
- Specific Canadian context (CRA, T776, Ontario LTB, etc.)
- One clear CTA linking to the article
- 4-5 relevant hashtags on last line
- Zero buzzwords

Return only this JSON: {{"post": "full post text with hashtags"}}""",
        },
    ]

    # LinkedIn post is short so JSON mode is fine here
    raw = call_groq(messages, max_tokens=500, temperature=0.8, force_json_mode=True)
    if not raw:
        return None
    try:
        post_data = json.loads(raw)
        linkedin_text = post_data.get("post", "")
        print(f"✅ LinkedIn post generated ({len(linkedin_text)} chars)")
        return linkedin_text
    except Exception as e:
        print(f"⚠️  LinkedIn generation failed: {e}")
        return None


def upload_image_to_linkedin(access_token, image_url, org_id):
    print("🖼️  Uploading image to LinkedIn...")
    try:
        image_response = requests.get(image_url, timeout=15)
        image_response.raise_for_status()
        image_bytes = image_response.content

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

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

        requests.put(
            upload_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/octet-stream",
            },
            data=image_bytes,
            timeout=30,
        ).raise_for_status()

        print(f"✅ Image uploaded — asset: {asset_urn}")
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

    # Validate org ID format — must be numeric only
    org_id_clean = org_id.strip()
    if not org_id_clean.isdigit():
        print(f"❌ LINKEDIN_ORGANIZATION_ID must be a plain number.")
        print(f"   Current value appears to have extra characters.")
        print(f"   Go to LinkedIn → Company Page → Admin tools → Account")
        print(f"   The org ID is the number in the URL: linkedin.com/company/12345678/admin/")
        print(f"   Update the GitHub secret with just the number, no other text.")
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
        image_urn = upload_image_to_linkedin(access_token, image_url, org_id_clean)

    author_urn = f"urn:li:organization:{org_id_clean}"

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
    persona = get_current_persona()
    used_topics = get_used_topics()

    # Check if a pillar post is due today
    pending_pillar = get_pending_pillar()

    if pending_pillar:
        print(f"\n📌 PILLAR POST MODE — {pending_pillar['cluster']}")
        blog_data, topic = generate_pillar_content(pending_pillar)
        is_pillar = True
    else:
        print(f"\n📝 REGULAR POST MODE")
        # Try up to 3 different topics via offset
        for attempt in range(3):
            topic = pick_topic(persona, used_topics, offset=attempt)
            print(f"\n   Attempt {attempt + 1}/3 — topic: {topic}")
            blog_data = generate_blog_content(topic, persona)
            if blog_data:
                break
            if attempt < 2:
                print(f"   Failed — trying next topic in 10 seconds...")
                time.sleep(10)

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

    # Publish to Dev.to (skips gracefully if already exists)
    success, post_url = publish_to_devto(blog_data, image_data, slug)

    if saved_file or success:
        save_used_topic(topic)

        if is_pillar and pending_pillar:
            save_published_pillar(pending_pillar["id"])

        blog_url = f"https://www.rentalops.ca/blog/{slug}"
        cluster = blog_data.get("cluster", "General")

        log_new_post_for_index(blog_data["title"], slug, topic, cluster)

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
