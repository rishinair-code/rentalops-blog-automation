import os
import json
import requests
import random
import re
import time
from datetime import datetime

# GSC-driven topic selection (falls back gracefully when cache/API unavailable)
try:
    from gsc_topic_selector import pick_topic_gsc_driven
except ImportError:
    pick_topic_gsc_driven = None

# API Keys / config from GitHub Secrets
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')

# Model is overridable via env var so a future Google deprecation doesn't require
# a code edit — just update the GEMINI_MODEL secret/variable in the workflow.
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.6-flash')
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

# ─────────────────────────────────────────────────────────────
# GEMINI: structured content generation
# ─────────────────────────────────────────────────────────────

def generate_blog_content(persona, topic):
    if not GEMINI_API_KEY:
        raise ValueError(
            "Missing Gemini API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) "
            "as a GitHub Actions secret."
        )

    prompt = f"""You are an expert Canadian tax accountant and property management advisor writing for rentalops.ca.

Write a comprehensive, SEO-optimized blog post for a "{persona}" targeting the keyword phrase: "{topic}".

Requirements:
- Reference specific CRA rules or context (like the T776 form, or real estate rules for 2026) where applicable.
- Professional, authoritative, friendly peer-to-peer tone. No generic filler language.
- Use markdown with ## and ### headings inside the "content" field.
- Aim for 1200-2000 words in "content".

Return ONLY a JSON object with exactly these keys:
- "title": SEO-friendly title (string)
- "metaDescription": a compelling 140-160 character search-result description (string)
- "tags": an array of 4-6 short topical tags (strings)
- "content": the full article body in markdown (string)
"""

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "metaDescription": {"type": "STRING"},
                    "tags": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "content": {"type": "STRING"},
                },
                "required": ["title", "metaDescription", "tags", "content"],
            },
            "maxOutputTokens": 8192,
        },
    }
    params = {"key": GEMINI_API_KEY}

    RETRYABLE_STATUS_CODES = {429, 503}
    MAX_ATTEMPTS = 4
    BACKOFF_SECONDS = [15, 30, 60]

    response = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers, params=params)

        if response.ok:
            break

        if response.status_code in RETRYABLE_STATUS_CODES and attempt < MAX_ATTEMPTS:
            wait = BACKOFF_SECONDS[attempt - 1]
            print(
                f"⏳ Gemini returned {response.status_code} (attempt {attempt}/{MAX_ATTEMPTS}) "
                f"— retrying in {wait}s..."
            )
            time.sleep(wait)
            continue

        try:
            error_body = response.json()
        except ValueError:
            error_body = response.text
        raise RuntimeError(
            f"Gemini API request failed with status {response.status_code} "
            f"(after {attempt} attempt{'s' if attempt > 1 else ''}). "
            f"URL: {response.url}\n"
            f"Response body: {error_body}"
        )

    response_data = response.json()

    candidates = response_data.get('candidates')
    if not candidates:
        block_reason = response_data.get('promptFeedback', {}).get('blockReason')
        raise RuntimeError(
            f"Gemini returned no candidates. blockReason={block_reason!r}. "
            f"Full response: {response_data}"
        )

    parts = candidates[0].get('content', {}).get('parts', [])
    if not parts or 'text' not in parts[0]:
        raise RuntimeError(f"Unexpected Gemini response shape: {response_data}")

    finish_reason = candidates[0].get('finishReason')
    if finish_reason == 'MAX_TOKENS':
        raise RuntimeError(
            "Gemini's response was cut off before finishing (finishReason=MAX_TOKENS), "
            "so the JSON is incomplete. Raise maxOutputTokens in generate_blog_content() "
            "and try again."
        )

    raw_text = parts[0]['text'].strip()

    if raw_text.startswith('```'):
        raw_text = re.sub(r'^```[a-zA-Z]*\n?', '', raw_text)
        raw_text = re.sub(r'\n?```$', '', raw_text).strip()

    try:
        blog_data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        start = max(0, e.pos - 200)
        end = min(len(raw_text), e.pos + 200)
        raise RuntimeError(
            f"Gemini's response wasn't valid JSON despite responseSchema "
            f"(finishReason={finish_reason!r}, {len(raw_text)} chars total). "
            f"Parse error: {e}\n"
            f"Text around the failure point (char {e.pos}):\n"
            f"...{raw_text[start:end]}..."
        ) from e

    required = ['title', 'metaDescription', 'tags', 'content']
    missing = [f for f in required if f not in blog_data]
    if missing:
        raise RuntimeError(f"Gemini JSON is missing required fields: {missing}")

    if not isinstance(blog_data['tags'], list):
        blog_data['tags'] = []
    blog_data['tags'] = blog_data['tags'][:6]

    return blog_data


# ─────────────────────────────────────────────────────────────
# UNSPLASH: cover image
# ─────────────────────────────────────────────────────────────

UNSPLASH_QUERY_POOLS = {
    "CRA Tax & Reporting": [
        "tax documents desk paperwork",
        "accountant calculator receipts",
        "financial paperwork filing folder",
        "home office tax season",
    ],
    "Ontario Landlord Rules": [
        "apartment building exterior",
        "house keys rental property",
        "lease agreement signing",
        "residential apartment complex",
    ],
    "General": [
        "small house exterior for rent",
        "modern apartment building",
        "house keys real estate",
        "duplex rental home",
    ],
}


def get_unsplash_image(cluster="General"):
    if not UNSPLASH_ACCESS_KEY:
        print("⚠️  No UNSPLASH_ACCESS_KEY set — skipping cover image.")
        return None

    query = random.choice(UNSPLASH_QUERY_POOLS.get(cluster, UNSPLASH_QUERY_POOLS["General"]))

    try:
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": query,
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY,
            },
            timeout=15,
        )
        response.raise_for_status()
        image_data = response.json()

        image_url = image_data['urls']['regular']
        photographer = image_data['user']['name']
        photographer_url = image_data['user']['links']['html']

        return {
            'url': image_url,
            'credit': f"Photo by [{photographer}]({photographer_url}) on [Unsplash](https://unsplash.com)",
        }
    except Exception as e:
        print(f"⚠️  Unsplash image fetch failed (non-fatal): {e}")
        return None


# ─────────────────────────────────────────────────────────────
# TOPIC SELECTION
# ─────────────────────────────────────────────────────────────

def _fallback_topic(persona, used_topics):
    unused = [t for t in persona.get("topics", []) if t not in used_topics]
    return random.choice(unused) if unused else random.choice(persona["topics"])


def _cluster_for_topic(topic):
    lower = topic.lower()
    if "t776" in lower or "expense" in lower or "tracker" in lower:
        return "CRA Tax & Reporting"
    if "ontario" in lower or "board" in lower:
        return "Ontario Landlord Rules"
    return "General"


def select_topic(used_topics):
    """Pick a topic — using coordinator for monthly planning + GSC demand
    data, falling back to the predefined topic list."""
    target_topic = None
    target_persona = None
    is_coordinator_pick = False

    # Try the coordinator from the main repo first for smarter scheduling
    coordinator_path = "../rental-management-app/scripts/content_coordinator.py"
    coordinator_local = "content_coordinator.py"
    coordinator = None

    if os.path.exists(coordinator_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("content_coordinator", coordinator_path)
        coordinator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(coordinator)
    elif os.path.exists(coordinator_local):
        import importlib.util
        spec = importlib.util.spec_from_file_location("content_coordinator", coordinator_local)
        coordinator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(coordinator)

    if coordinator:
        print("🎯 Using content coordinator for intelligent topic selection...")
        competitor_kw = coordinator.get_competitor_keywords()
        pick = coordinator.select_weekly_topic(used_topics, competitor_kw)
        target_topic = pick["topic"]
        target_persona = pick["persona"]
        is_coordinator_pick = True
        print(f"   Source: {pick['source']} | Score: {round(pick.get('score', 0), 1)} | GSC Impr: {pick.get('impressions', 0)} | Pos: {round(pick.get('position', 100), 1)}")
        if pick.get("competitor_matches"):
            print(f"   Competitor overlaps: {len(pick['competitor_matches'])}")
    else:
        print("⚠️ Coordinator not available. Using basic GSC selection...")
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

    if not target_topic:
        matched_persona = next((p for p in PERSONAS if p["name"] == target_persona), PERSONAS[0])
        target_topic = _fallback_topic(matched_persona, used_topics)

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

    blog_data = generate_blog_content(target_persona, target_topic)
    image_data = get_unsplash_image(cluster_group)

    slug = re.sub(r'[^a-z0-9]+', '-', target_topic.lower()).strip('-')

    post_data = {
        "title": blog_data["title"],
        "metaDescription": blog_data["metaDescription"],
        "content": blog_data["content"],
        "tags": blog_data["tags"],
        "persona": target_persona,
        "postType": "cluster",
        "cluster": cluster_group,
        "coverImage": image_data["url"] if image_data else None,
        "coverImageCredit": image_data["credit"] if image_data else None,
        "publishedAt": datetime.now().isoformat(),
        "slug": slug,
    }

    os.makedirs("posts", exist_ok=True)
    with open(f"posts/{slug}.json", "w") as f:
        json.dump(post_data, f, indent=2)
    print(f"✅ Success! Content successfully compiled to posts/{slug}.json")

    if target_topic not in used_topics:
        used_topics.append(target_topic)
        with open("used_topics.json", "w") as f:
            json.dump(used_topics, f, indent=2)

    # Sync used_topics to the main repo's cache if coordinator was used
    # so both repos share state on the 3x/week schedule
    main_repo_used = "../rental-management-app/data/gsc_cache/used_topics.json"
    if os.path.exists("../rental-management-app"):
        os.makedirs("../rental-management-app/data/gsc_cache", exist_ok=True)
        save_data = {"used_topics": used_topics, "updated_at": datetime.now().isoformat()}
        with open(main_repo_used, "w") as f:
            json.dump(save_data, f, indent=2)


if __name__ == "__main__":
    main()
