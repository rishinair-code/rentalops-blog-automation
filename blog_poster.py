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
        "description": "A landlord with 2–10 properties looking to scale efficiently and minimize tax burden.",
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
        "description": "Someone renting out a property by necessity — inherited home, relocated for work, couldn't sell.",
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
        "description": "Someone managing properties for family or as a side income alongside a full-time job.",
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
- PRIMARY KEYWORD: "{topic}" — use this exact phrase 
  or very close variant in the title, first paragraph, 
  and at least 2 H2 headings
- Title: Use the primary keyword naturally. 
  Format: "[Keyword]: [Benefit/Context] for Canadian Landlords"
  or "[Year] Guide: [Keyword]". Keep under 60 characters if possible.
- Meta description: 150-160 characters EXACTLY. 
  Include the primary keyword. 
  End with a benefit or call to action.
- Content: 900-1200 words in markdown
- Structure: Introduction (with keyword in first 100 words), 
  3-5 H2 sections with keyword variants, Conclusion with CTA
- Use H2 and H3 headers
- Include practical, actionable Canadian-specific advice
- Reference CRA rules, T776, provincial regulations where applicable
- Mention RentalOps naturally 2-3 times as a solution tool
- End with a clear CTA to try RentalOps free
- Include a "Key Takeaways" or summary section
- Tags: 5 SEO-relevant tags (use actual search terms people use){roi_instruction}

Return ONLY this JSON structure:
{{
  "title": "...",
  "metaDescription": "...",
  "content": "... full markdown content ...",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "persona": "{persona['name']}"
}}

IMPORTANT: The meta description must be 
150-160 characters. Count carefully.""",
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

def save_post_to_repo(blog_data, image_data, post_slug):
    """Save the blog post as a JSON file in the posts/ directory"""
    try:
        os.makedirs("posts", exist_ok=True)

        post = {
            "title": blog_data["title"],
            "metaDescription": blog_data["metaDescription"],
            "content": blog_data["content"],
            "tags": blog_data.get("tags", []),
            "persona": blog_data.get("persona", ""),
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
        print(f"⚠️  Could not save post to repo: {e}")
        return None

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
        # Generate slug from title
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', blog_data["title"].lower()).strip('-')[:80]

    # Save post to repo
    save_post_to_repo(blog_data, image_data, slug)

    # Also publish to Dev.to as backup/SEO (optional — can remove)
    success, post_url = publish_to_devto(blog_data, image_data)

    if success or os.path.exists(f"posts/{slug}.json"):
        save_used_topic(topic)

        blog_url = f"https://www.rentalops.ca/blog/{slug}"

        # LinkedIn
        linkedin_text = generate_linkedin_post(blog_data, blog_url)
        if linkedin_text:
            post_to_linkedin(linkedin_text)

        print("\n" + "=" * 60)
        print("✅ Blog post automation completed successfully!")
        print(f"🔗 Live at: {blog_url}")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Blog post automation failed.")
        print("=" * 60)

if __name__ == "__main__":
    main()
