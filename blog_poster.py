import os
import json
import requests
import random
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
        "description": "Someone who recently became a landlord and is overwhelmed by taxes, compliance, and paperwork.",
        "topics": [
            "what expenses can Canadian landlords deduct on their taxes",
            "how to fill out the T776 rental income form in Canada",
            "Ontario landlord obligations under the Residential Tenancies Act",
            "how to screen tenants legally in Canada",
            "security deposits rules for Ontario landlords",
            "first-year mistakes new Canadian landlords make",
            "how to set rent price for your first rental property in Canada",
            "what is the landlord and tenant board and how does it work",
            "how to write a lease agreement in Ontario",
            "CRA audit risk for rental income — what triggers it",
        ],
    },
    {
        "name": "Portfolio Builder",
        "description": "A landlord with 2–10 properties looking to scale efficiently and minimize tax burden.",
        "topics": [
            "how to track rental income and expenses across multiple properties",
            "capital cost allowance for Canadian rental properties explained",
            "GST HST implications for Canadian landlords — what you need to know",
            "how to incorporate your rental properties in Canada",
            "automating rent collection across multiple Canadian properties",
            "refinancing rental properties in Canada — tax implications",
            "how to use a holding company for rental properties in Canada",
            "inter-provincial landlord rules if you own properties in multiple provinces",
            "hiring a property manager vs self-managing — tax and cost comparison",
            "year-end tax checklist for Canadian landlords with multiple properties",
        ],
    },
    {
        "name": "Accidental Landlord",
        "description": "Someone renting out a property by necessity — inherited home, relocated for work, couldn't sell.",
        "topics": [
            "tax rules for renting out your principal residence in Canada",
            "how to report rental income if you only rented part of the year",
            "renting out your basement suite in Canada — what you need to know",
            "capital gains implications when you sell a property you rented out",
            "what happens if you don't report rental income to CRA",
            "short-term vs long-term rental tax rules in Canada",
            "Airbnb tax rules for Canadian landlords",
            "how to convert rental property back to personal use in Canada",
            "insurance requirements when renting your home in Canada",
            "CRA principal residence exemption — how it interacts with rental income",
        ],
    },
    {
        "name": "Part-Time Property Manager",
        "description": "Someone managing properties for family or as a side income alongside a full-time job.",
        "topics": [
            "how rental income affects your tax bracket in Canada",
            "deducting home office expenses as a landlord in Canada",
            "record keeping requirements for Canadian landlords",
            "how to split rental income with a spouse in Canada",
            "mileage and travel deductions for Canadian landlords",
            "using software vs spreadsheets for rental property accounting",
            "why US property management software fails Canadian landlords",
            "how to prepare for tax season as a part-time landlord",
            "deducting professional fees legal and accounting for landlords",
            "passive income rules and rental income — what CRA says",
        ],
    },
]

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
# PERSONA SELECTION
# ─────────────────────────────────────────────
def get_current_persona():
    day_of_year = datetime.now().timetuple().tm_yday
    persona_index = day_of_year % len(PERSONAS)
    return PERSONAS[persona_index]


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
            params={"query": query, "orientation": "landscape", "content_filter": "high"},
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


# ─────────────────────────────────────────────
# CONTENT GENERATION
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

    # Decide if this post should include an ROI/cost section
    include_roi = random.random() < 0.3
    roi_instruction = ""
    if include_roi:
        roi_instruction = """
- Include a section comparing the cost of doing this manually vs using RentalOps (be specific with time estimates and dollar amounts)
- Mention RentalOps pricing starting at $6.99/month where relevant"""

    print(f"💰 ROI/cost section: {'Yes' if include_roi else 'No'}")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": f"""You are a content writer for RentalOps, a Canadian landlord expense tracking and tax preparation tool.
Write authoritative, practical blog posts aimed at Canadian landlords.
Always reference Canadian-specific context: CRA, T776, Ontario LTB, provincial rules, CAD amounts.
RentalOps helps landlords track income/expenses, prepare for tax season, and stay CRA-compliant.
Target persona: {persona['name']} — {persona['description']}
You MUST respond with ONLY valid JSON. No markdown, no code blocks. Raw JSON only.""",
            },
            {
                "role": "user",
                "content": f"""Write a complete blog post about: {topic}

Requirements:
- Title: compelling, SEO-friendly, Canadian context
- Meta description: 150-160 characters
- Content: 800-1200 words in markdown format
- Use H2 and H3 headers
- Include practical, actionable advice
- Reference CRA rules, provincial regulations where applicable
- Mention RentalOps naturally 2-3 times as a solution tool (not spammy)
- End with a clear call to action to try RentalOps{roi_instruction}
- Tags: 5 relevant tags for Canadian landlord/real estate content

Return ONLY this JSON structure:
{{
  "title": "...",
  "metaDescription": "...",
  "content": "... full markdown content ...",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "persona": "{persona['name']}"
}}""",
            },
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
        "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]

        print(f"📥 Raw AI response (first 200 chars): {ai_response[:200]}")

        blog_data = json.loads(ai_response)

        required_fields = ["title", "metaDescription", "content", "tags"]
        for field in required_fields:
            if field not in blog_data:
                print(f"❌ Missing required field: {field}")
                return None, None

        print(f"✅ Content generated successfully")
        print(f"   Persona: {persona['name']}")
        print(f"   Title: {blog_data['title'][:60]}...")
        print(f"   Tags: {', '.join(blog_data['tags'])}")
        print(f"   Content length: {len(blog_data['content'])} characters")

        return blog_data, topic

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        return None, None


# ─────────────────────────────────────────────
# PUBLISH TO DEV.TO
# ─────────────────────────────────────────────
def publish_to_devto(blog_data, image_data):
    print("📤 Publishing to Dev.to...")

    content = blog_data["content"]
    if image_data:
        content = f"{content}\n\n---\n\n*{image_data['credit']}*"

    # Dev.to tags: lowercase, no spaces or hyphens, max 20 chars, max 4 tags
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
        print(f"✅ Post published successfully!")
        print(f"📝 Title: {result['title']}")
        print(f"🔗 URL: {post_url}")
        return True, post_url

    except Exception as e:
        print(f"❌ Error publishing to Dev.to: {e}")
        return False, None


# ─────────────────────────────────────────────
# LINKEDIN
# ─────────────────────────────────────────────
def generate_linkedin_post(blog_data, blog_url):
    print("🔗 Generating LinkedIn post...")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": """You are a LinkedIn content writer for RentalOps, a Canadian landlord tax and expense tracking tool.
Write punchy, engaging LinkedIn posts that feel human — not like marketing copy.
You MUST respond with ONLY valid JSON. No markdown, no code blocks. Raw JSON only.""",
            },
            {
                "role": "user",
                "content": f"""Write a LinkedIn post based on this blog article.

Blog title: {blog_data['title']}
Blog summary: {blog_data['metaDescription']}
Target persona: {blog_data.get('persona', 'Canadian landlord')}
Full article URL: {blog_url}

Rules:
- 150-200 words maximum
- Start with a hook — a question, surprising stat, or bold statement
- Write in first person, conversational tone
- Reference Canadian context (Ontario, CRA, LTB etc.) where relevant
- End with 1 clear call to action linking to the full article
- Include 4-5 relevant hashtags on the last line
- Do NOT use corporate-speak or buzzwords

Return ONLY this JSON:
{{
  "post": "the full linkedin post text including hashtags"
}}""",
            },
        ],
        "temperature": 0.8,
        "max_tokens": 500,
        "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        post_data = json.loads(ai_response)
        linkedin_text = post_data.get("post", "")
        print(f"✅ LinkedIn post generated ({len(linkedin_text)} chars)")
        return linkedin_text
    except Exception as e:
        print(f"⚠️  LinkedIn post generation failed: {e}")
        return None


def upload_image_to_linkedin(access_token, image_url, org_id):
    print("🖼️  Uploading image to LinkedIn...")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202501",
    }

    register_payload = {
        "initializeUploadRequest": {
            "owner": f"urn:li:organization:{org_id}"
        }
    }

    try:
        register_response = requests.post(
            "https://api.linkedin.com/rest/images?action=initializeUpload",
            headers=headers,
            json=register_payload,
            timeout=15,
        )
        register_response.raise_for_status()
        register_data = register_response.json()

        upload_url = register_data["value"]["uploadUrl"]
        image_urn = register_data["value"]["image"]

        # Download image from Unsplash
        image_response = requests.get(image_url, timeout=15)
        image_response.raise_for_status()
        image_bytes = image_response.content

        # Upload to LinkedIn
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

        print("✅ Image uploaded to LinkedIn successfully")
        return image_urn

    except Exception as e:
        print(f"⚠️  Image upload failed — will post without image: {e}")
        return None


def post_to_linkedin(post_text, image_url=None):
    print("📤 Posting to LinkedIn...")

    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    org_id = os.environ.get("LINKEDIN_ORGANIZATION_ID")

    if not access_token:
        print("⚠️  LINKEDIN_ACCESS_TOKEN not set — skipping LinkedIn post")
        return False

    if not org_id:
        print("⚠️  LINKEDIN_ORGANIZATION_ID not set — skipping LinkedIn post")
        return False

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202501",
    }

    # Get member ID (still needed for userinfo check)
    try:
        profile_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers=headers,
            timeout=10,
        )
        profile_response.raise_for_status()
        profile = profile_response.json()
        member_id = profile.get("sub")
        if not member_id:
            print("❌ Could not retrieve LinkedIn member ID")
            return False
        print("👤 LinkedIn member ID found")
    except Exception as e:
        print(f"❌ Failed to get LinkedIn profile: {e}")
        return False

    # Upload image if available
    image_urn = None
    if image_url:
        image_urn = upload_image_to_linkedin(access_token, image_url, org_id)

    # Build post payload
    author_urn = f"urn:li:organization:{org_id}"

    if image_urn:
        post_payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": post_text},
                    "shareMediaCategory": "IMAGE",
                    "media": [{"status": "READY", "media": image_urn}],
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
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("🚀 RentalOps Blog Automation Starting...")
    print("=" * 60)

    # Generate content
    blog_data, topic = generate_blog_content()
    if not blog_data or not topic:
        print("❌ Failed to generate content. Exiting.")
        print("\n" + "=" * 60)
        print("❌ Blog post automation failed.")
        print("=" * 60)
        return

    # Get cover image
    image_search_query = generate_image_query(blog_data["title"])
    image_data = get_unsplash_image(image_search_query)

    # Publish to Dev.to
    success, post_url = publish_to_devto(blog_data, image_data)

    if success:
        save_used_topic(topic)

        blog_url = post_url if post_url else "https://dev.to"

        # LinkedIn
        linkedin_text = generate_linkedin_post(blog_data, blog_url)
        if linkedin_text:
            image_url = image_data["url"] if image_data else None
            post_to_linkedin(linkedin_text, image_url)

        print("\n" + "=" * 60)
        print("✅ Blog post automation completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Blog post automation failed.")
        print("=" * 60)


if __name__ == "__main__":
    main()
