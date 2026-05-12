import os
import json
import requests
import random
from datetime import datetime
 
# API Keys from GitHub Secrets
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
HASHNODE_API_KEY = os.environ.get('HASHNODE_API_KEY')
HASHNODE_PUBLICATION_ID = os.environ.get('HASHNODE_PUBLICATION_ID')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
HASHNODE_BLOG_HOST = os.environ.get('HASHNODE_BLOG_HOST')
 
PERSONAS = [
    {
        "name": "Accidental Landlord",
        "description": "Inherited or bought 1-3 rental units. Self-managing with spreadsheets and e-transfers. Scared of the provincial tribunal. No system, doesn't know the rules, hates chasing rent.",
        "channels": "Facebook Groups, Reddit r/OntarioLandlord r/PersonalFinanceCanada, Kijiji forums",
        "tone": "reassuring, plain language, no jargon, step-by-step guidance",
        "topics": [
            "what to do when a tenant stops paying rent in Canada",
            "how to serve an eviction notice correctly in your province",
            "simple rent tracking system for small Canadian landlords",
            "provincial rental tribunal process explained for first-time landlords",
            "Canadian Standard Lease agreements explained simply",
            "how to handle a tenant maintenance request legally in Canada",
            "what landlords must disclose before signing a lease in Canada",
            "e-transfer rent collection risks and better alternatives for Canadian landlords",
            "how to screen tenants legally under Canadian human rights law",
            "what happens if you don't use your province's standard lease form",
            "rent arrears process in BC vs Ontario vs Alberta — key differences",
            "first-time landlord checklist for Canadian rental properties"
        ]
    },
    {
        "name": "Portfolio Builder",
        "description": "Growing intentionally with 4-15 units across one or more Canadian provinces. Uses WhatsApp, spreadsheets, and bank alerts. Wants to look professional and save admin time. Pain: no cross-unit visibility, manual tenant screening, tax prep is a mess.",
        "channels": "BiggerPockets Canada, LinkedIn, real estate investor meetups, YouTube, REIN",
        "tone": "professional, data-driven, efficiency-focused, respects their time",
        "topics": [
            "how to track expenses across multiple rental properties in Canada",
            "tenant screening checklist for Canadian landlords with multiple units",
            "CRA rental income rules every Canadian landlord must know",
            "how to prepare for tax season as a small portfolio landlord in Canada",
            "automating rent collection across multiple Canadian properties",
            "provincial rent increase guidelines across Canada for 2025",
            "capital expense vs operating expense for Canadian rental properties",
            "how to scale from 3 to 10 rental units without losing control",
            "cross-unit maintenance tracking for growing Canadian landlords",
            "how to create a professional landlord system without expensive US software",
            "rental property depreciation (CCA) rules for Canadian landlords",
            "GST HST implications for Canadian landlords — what you need to know"
        ]
    },
    {
        "name": "Part-Time Property Manager",
        "description": "Manages 15-50 units for self plus family or friends across Canada. Paying in USD for US tools that don't understand Canadian provincial law. Needs owner statements, e-signature leases, provincial tribunal forms built in.",
        "channels": "LPMA, FRPO, IPOANS, SKLA, LinkedIn, local REIN chapters, REIC",
        "tone": "authoritative, compliance-focused, efficiency and professionalism",
        "topics": [
            "why US property management software fails Canadian landlords",
            "provincial rental tribunal forms every Canadian property manager needs",
            "how to create owner statements for informal property management in Canada",
            "eviction notice types by province — BC RTB vs Ontario LTB vs Alberta RTDRS",
            "Canadian rent increase rules vs US states — key differences",
            "how to manage properties for family members legally in Canada",
            "e-signature lease agreements and legal validity across Canadian provinces",
            "EFT rent collection in CAD — why USD tools create problems",
            "provincial landlord association compliance checklist for Canadian PMs",
            "rent control rules by province — which provinces have it and which don't",
            "how to handle security deposits legally in each Canadian province",
            "owner reporting best practices for informal Canadian property managers"
        ]
    }
]
 
CANADIAN_DIFFERENTIATOR = """
RentalOps is built specifically for Canadian landlords — not adapted from a US tool.
 
Key Canadian realities to reference where relevant:
- FEDERAL: CRA rental income reporting, capital cost allowance (CCA), GST/HST rules
- ONTARIO: LTB (Landlord and Tenant Board), N4/N12/N13 forms, Ontario Standard Lease, rent control exemptions for post-2018 units
- BC: Residential Tenancy Branch (RTB), BC Standard Lease, rent increase rules, security deposit limits (half month)
- ALBERTA: RTDRS (Residential Tenancy Dispute Resolution Service), no rent control, fixed vs periodic tenancy rules
- QUEBEC: Tribunal administratif du logement (TAL), French-language lease requirements, strict rent increase process
- OTHER PROVINCES: Reference the relevant provincial tribunal and rules for Manitoba (RTB), Saskatchewan (SKLA), Nova Scotia, New Brunswick, PEI, Newfoundland as appropriate
 
Always position US tools (DoorLoop, Buildium, AppFolio) as missing these Canadian realities.
Always write amounts in CAD. Always reference Canadian banking (EFT, Interac e-Transfer).
"""
 
RENTALOPS_FEATURES = """
RentalOps (rentalops.ca) is a Canadian-built rental expense and tax tracking tool — not adapted from a US product. Built specifically for landlords who need to file CRA Form T776.
 
FEATURES TO REFERENCE NATURALLY WHERE RELEVANT:
- CRA AUTO-CATEGORIZATION: Automatically sorts every expense into the correct CRA category and maps it to the right T776 line (e.g., line 9270 for professional fees, 9200 for repairs). No tax knowledge required from the landlord.
- RECEIPT CAPTURE: Snap a photo of any receipt from your phone in ~15 seconds. Stored permanently — nothing gets lost before tax season.
- PORTFOLIO HEALTH DASHBOARD: Real-time view of gross income, net profit, and top deductions across all properties year-round.
- MISSED DEDUCTION FINDER: Flags deductions landlords commonly miss — helps maximize the annual refund.
- ACCOUNTANT-READY EXPORT: One-click export produces a clean, audit-ready file organized by CRA category. No more handing over a shoebox of receipts.
- MULTI-USER (Pro): Lets a spouse, partner, or bookkeeper access the same account.
- AI INSIGHTS (Pro): Deeper financial analysis across large or multi-property portfolios.
 
PRICING (always mention the free trial when referencing cost):
- Starter: $6.99/mo — 1 property, T776 summary, income/expense tracking
- Core: $9.99/mo — up to 5 properties, receipt upload, priority support
- Pro: $19.99/mo — unlimited properties, AI insights, multi-user access
- All plans: 7-day free trial, no credit card required
 
INTEGRATION RULES:
- Mention RentalOps once or twice per post maximum
- The mention must connect directly to the topic — never feel like an ad
- Always link as [RentalOps](https://rentalops.ca) when mentioned
- Lead with the problem the feature solves, then introduce RentalOps as the solution
"""
 
# ── Topic tracking ──────────────────────────────────────────────────────────
 
def get_used_topics():
    try:
        if os.path.exists("used_topics.json"):
            with open("used_topics.json", "r") as f:
                used = json.load(f)
            print(f"📋 Found {len(used)} previously used topics")
            return used
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
 
# ── Persona & topic selection ────────────────────────────────────────────────
 
def get_current_persona():
    week_number = datetime.now().isocalendar()[1]
    return PERSONAS[week_number % len(PERSONAS)]
 
 
def should_include_roi_section():
    return datetime.now().isocalendar()[1] % 3 == 0
 
# ── Cross-linking ────────────────────────────────────────────────────────────
 
def fetch_recent_posts():
    if not HASHNODE_BLOG_HOST:
        print("⚠️  HASHNODE_BLOG_HOST not set — skipping cross-link fetch")
        return []
    try:
        query = """
        query GetRecentPosts($host: String!) {
            publication(host: $host) {
                posts(first: 20) {
                    edges { node { title url } }
                }
            }
        }
        """
        response = requests.post(
            "https://gql.hashnode.com",
            headers={"Authorization": HASHNODE_API_KEY, "Content-Type": "application/json"},
            json={"query": query, "variables": {"host": HASHNODE_BLOG_HOST}},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        if 'errors' in result:
            print(f"⚠️  Cross-link fetch error: {result['errors']}")
            return []
        edges = result['data']['publication']['posts']['edges']
        posts = [{"title": e['node']['title'], "url": e['node']['url']} for e in edges]
        print(f"📚 Found {len(posts)} existing posts available for cross-linking")
        return posts
    except Exception as e:
        print(f"⚠️  Cross-link fetch failed (non-critical): {e}")
        return []
 
 
def find_related_post(posts, topic):
    if not posts:
        return None
    stopwords = {'a', 'an', 'the', 'and', 'or', 'for', 'in', 'of', 'to', 'vs', 'how', 'what', 'why', 'your'}
    topic_words = set(topic.lower().split()) - stopwords
    best_match, best_score = None, 0
    for post in posts:
        score = len(topic_words & (set(post['title'].lower().split()) - stopwords))
        if score > best_score:
            best_score, best_match = score, post
    if best_score >= 1:
        print(f"🔗 Cross-link match found: '{best_match['title']}'")
        return best_match
    print("🔗 No keyword match — using most recent post as cross-link")
    return posts[0]
 
# ── Content generation ───────────────────────────────────────────────────────
 
def generate_blog_content():
    persona = get_current_persona()
 
    used_topics = get_used_topics()
    available_topics = [t for t in persona["topics"] if t not in used_topics]
    if not available_topics:
        print(f"🔄 All topics for {persona['name']} used — resetting")
        available_topics = persona["topics"]
 
    topic = available_topics[datetime.now().timetuple().tm_yday % len(available_topics)]
 
    print(f"🎯 Target persona: {persona['name']}")
    print(f"🤖 Generating content about: {topic}")
 
    recent_posts = fetch_recent_posts()
    related_post = find_related_post(recent_posts, topic)
    include_roi = should_include_roi_section()
    print(f"💰 ROI/cost section: {'Yes' if include_roi else 'No'}")
 
    crosslink_instruction = ""
    if related_post:
        crosslink_instruction = f"""
CROSS-LINKING (mandatory):
Naturally link to this related post somewhere in the article body where it genuinely fits:
Title: "{related_post['title']}"
URL: {related_post['url']}
Use descriptive anchor text — never just "click here".
"""
 
    roi_instruction = ""
    if include_roi:
        roi_instruction = """
COST/ROI SECTION (mandatory for this post):
Include a section titled "## What This Mistake Actually Costs You" or "## Is [Tool/System] Worth It? A Real-Money Breakdown".
Use realistic CAD figures. Show cost of manual/wrong approach vs. doing it properly.
End the section with a natural mention of how [RentalOps](https://rentalops.ca) addresses this cost.
"""
 
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": f"""You are a content writer for RentalOps, a property management tool built specifically for Canadian landlords — not adapted from a US product.
 
TARGET READER: {persona['name']}
WHO THEY ARE: {persona['description']}
WHERE THEY HANG OUT: {persona['channels']}
TONE TO USE: {persona['tone']}
 
CANADIAN CONTEXT (always apply where relevant):
{CANADIAN_DIFFERENTIATOR}
 
PRODUCT CONTEXT (reference naturally, never forced):
{RENTALOPS_FEATURES}
 
{crosslink_instruction}
{roi_instruction}
 
WRITING RULES:
- Write for Canadian landlords. Reference correct provincial tribunal, legislation, and rules.
- Never give generic US advice. Everything must be Canada-specific.
- Do not recommend US tools as viable options for Canadian landlords.
- You MUST respond with ONLY valid JSON. No markdown, no code blocks, no explanations. Raw JSON only."""
            },
            {
                "role": "user",
                "content": f"""Write a blog post targeting {persona['name']} landlords about: {topic}
 
Return ONLY this JSON structure:
{{
  "title": "SEO-optimized title written for {persona['name']} in Canada",
  "metaDescription": "Compelling 140-150 character description for this persona",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "content": "Full article in markdown with ## headers (900-1200 words). Written in {persona['tone']} tone. Canada-specific throughout.",
  "persona": "{persona['name']}"
}}"""
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4000,
        "response_format": {"type": "json_object"}
    }
 
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        ai_response = response.json()['choices'][0]['message']['content']
        print(f"📥 Raw AI response (first 200 chars): {ai_response[:200]}...")
 
        cleaned = ai_response.strip()
        if cleaned.startswith('```'):
            lines, cleaned_lines, in_block = cleaned.split('\n'), [], False
            for line in lines:
                if line.strip().startswith('```'):
                    in_block = not in_block
                    continue
                if not in_block:
                    cleaned_lines.append(line)
            cleaned = '\n'.join(cleaned_lines).strip()
 
        start, end = cleaned.find('{'), cleaned.rfind('}')
        if start == -1 or end == -1:
            print("❌ No JSON object found in response")
            return None, None
 
        blog_data = json.loads(cleaned[start:end + 1])
        missing = [f for f in ['title', 'metaDescription', 'tags', 'content'] if f not in blog_data]
        if missing:
            print(f"❌ Missing required fields: {missing}")
            return None, None
 
        if not isinstance(blog_data['tags'], list):
            blog_data['tags'] = []
        blog_data['tags'] = blog_data['tags'][:5]
 
        print("✅ Content generated successfully")
        print(f"   Persona: {persona['name']}")
        print(f"   Title: {blog_data['title'][:60]}...")
        print(f"   Tags: {', '.join(blog_data['tags'])}")
        print(f"   Content length: {len(blog_data['content'])} characters")
        return blog_data, topic
 
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        import traceback
        print(traceback.format_exc())
        return None, None
 
# ── Image ────────────────────────────────────────────────────────────────────
 
def generate_image_query(title):
    topic_map = [
        (["eviction", "tribunal", "ltb", "rtb", "notice"], "tenant landlord dispute paperwork"),
        (["tax", "cra", "t776", "deduction", "refund", "cca", "gst", "hst"], "canadian tax documents accounting"),
        (["receipt", "expense", "tracking", "bookkeeping"], "receipt invoice bookkeeping desk"),
        (["rent", "collection", "payment", "arrears"], "rent payment money transfer"),
        (["screening", "tenant", "application"], "rental application interview"),
        (["maintenance", "repair", "inspection"], "home repair maintenance tools"),
        (["lease", "agreement", "contract", "sign"], "signing rental contract documents"),
        (["insurance", "liability"], "home insurance protection"),
        (["scale", "portfolio", "multiple", "units", "properties"], "apartment building investment"),
        (["software", "tool", "app", "system", "spreadsheet"], "property management laptop"),
        (["mortgage", "interest", "financing", "bank"], "canadian real estate mortgage"),
        (["deposit"], "keys apartment handover"),
    ]
    title_lower = title.lower()
    for keywords, query in topic_map:
        if any(k in title_lower for k in keywords):
            print(f"🖼️  Image query: '{query}'")
            return query
    fallbacks = [
        "canadian rental property exterior",
        "apartment building Canada",
        "landlord property keys",
        "rental home neighbourhood Canada",
        "residential property investment"
    ]
    query = random.choice(fallbacks)
    print(f"🖼️  Image query (fallback): '{query}'")
    return query
 
 
def get_unsplash_image(query):
    print(f"🖼️  Fetching image for: {query}")
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={"query": query, "orientation": "landscape", "client_id": UNSPLASH_ACCESS_KEY}
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ Image found by {data['user']['name']}")
        return {
            'url': data['urls']['regular'],
            'credit': f"Photo by [{data['user']['name']}]({data['user']['links']['html']}) on [Unsplash](https://unsplash.com)"
        }
    except Exception as e:
        print(f"⚠️  Error fetching image: {e}")
        return None
 
# ── Hashnode ─────────────────────────────────────────────────────────────────
 
def publish_to_hashnode(blog_data, image_data):
    print("📤 Publishing to Hashnode...")
 
    # Photographer credit at bottom — image set via coverImageOptions, NOT embedded in markdown
    content = blog_data['content']
    if image_data:
        content = f"{content}\n\n---\n\n*{image_data['credit']}*"
 
    tags = []
    for tag in blog_data.get('tags', [])[:5]:
        tag_slug = tag.lower().replace(' ', '-').replace('_', '-')
        tags.append({"slug": tag_slug, "name": tag})
 
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post { id title url slug }
        }
    }
    """
 
    post_input = {
        "title": blog_data['title'],
        "contentMarkdown": content,
        "tags": tags,
        "publicationId": HASHNODE_PUBLICATION_ID,
        "metaTags": {"description": blog_data['metaDescription']}
    }
 
    if image_data and image_data.get('url'):
        post_input["coverImageOptions"] = {"coverImageURL": image_data['url']}
 
    try:
        response = requests.post(
            "https://gql.hashnode.com",
            headers={"Authorization": HASHNODE_API_KEY, "Content-Type": "application/json"},
            json={"query": mutation, "variables": {"input": post_input}}
        )
 
        if response.status_code != 200:
            print(f"❌ Hashnode returned status {response.status_code}")
            print(f"❌ Hashnode response body: {response.text}")
 
        response.raise_for_status()
        result = response.json()
 
        if 'errors' in result:
            print(f"❌ Hashnode GraphQL Error: {result['errors']}")
            return False, None
 
        post = result['data']['publishPost']['post']
        print(f"✅ Post published successfully!")
        print(f"📝 Title: {post['title']}")
        print(f"🔗 URL: {post['url']}")
        return True, post['url']
 
    except Exception as e:
        print(f"❌ Error publishing to Hashnode: {e}")
        return False, None
 
# ── LinkedIn ─────────────────────────────────────────────────────────────────
 
def generate_linkedin_post(blog_data, blog_url):
    print("🔗 Generating LinkedIn post...")
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are a LinkedIn content writer for RentalOps, a Canadian landlord tax and expense tracking tool. Write punchy, engaging posts that feel human. Respond with ONLY valid JSON. No markdown, no code blocks."
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
- Conversational, first person tone
- Reference Canadian context (CRA, LTB, Ontario etc.) where relevant
- End with 1 clear call to action linking to the full article
- Include 4-5 relevant hashtags on the last line
 
Return ONLY this JSON:
{{"post": "the full linkedin post text including hashtags"}}"""
            }
        ],
        "temperature": 0.8,
        "max_tokens": 500,
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        linkedin_text = json.loads(response.json()['choices'][0]['message']['content']).get('post', '')
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
        "X-Restli-Protocol-Version": "2.0.0"
    }
    try:
        # Step 1 — register upload
        reg = requests.post(
            "https://api.linkedin.com/rest/images?action=initializeUpload",
            headers=headers,
            json={"initializeUploadRequest": {"owner": f"urn:li:organization:{org_id}"}},
            timeout=15
        )
        reg.raise_for_status()
        reg_data = reg.json()
        upload_url = reg_data['value']['uploadUrl']
        image_urn = reg_data['value']['image']  # extract URN from response
 
        # Step 2 — download image bytes
        image_bytes = requests.get(image_url, timeout=15).content
 
        # Step 3 — upload to LinkedIn
        requests.put(
            upload_url,
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/octet-stream"},
            data=image_bytes,
            timeout=30
        ).raise_for_status()
 
        print("✅ Image uploaded to LinkedIn successfully")
        return image_urn
    except Exception as e:
        print(f"⚠️  Image upload failed — will post without image: {e}")
        return None
 
 
def post_to_linkedin(post_text, image_url=None):
    print("📤 Posting to LinkedIn...")
 
    access_token = os.environ.get('LINKEDIN_ACCESS_TOKEN')
    org_id = os.environ.get('LINKEDIN_ORGANIZATION_ID')
 
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
        "LinkedIn-Version": "202501"
    }
 
    image_urn = upload_image_to_linkedin(access_token, image_url, org_id) if image_url else None
 
    post_payload = {
        "author": f"urn:li:organization:{org_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "IMAGE" if image_urn else "NONE",
                **({"media": [{"status": "READY", "media": image_urn}]} if image_urn else {})
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
 
    try:
        post_response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json=post_payload,
            timeout=15
        )
        print(f"LinkedIn response status: {post_response.status_code}")
        print(f"LinkedIn response body: {post_response.text}")
        post_response.raise_for_status()
        print("✅ Posted to LinkedIn successfully!")
        return True
    except Exception as e:
        print(f"❌ LinkedIn post failed: {e}")
        return False
 
# ── Main ─────────────────────────────────────────────────────────────────────
 
def main():
    print("=" * 60)
    print("🚀 RentalOps Blog Automation Starting...")
    print("=" * 60)
 
    if not all([GROQ_API_KEY, HASHNODE_API_KEY, HASHNODE_PUBLICATION_ID, UNSPLASH_ACCESS_KEY]):
        print("❌ Missing API keys! Please check GitHub Secrets.")
        return
 
    blog_data, topic = generate_blog_content()
    if not blog_data or not topic:
        print("❌ Failed to generate content. Exiting.")
        return
 
    image_data = get_unsplash_image(generate_image_query(blog_data['title']))
    success, post_url = publish_to_hashnode(blog_data, image_data)
 
    if success:
        save_used_topic(topic)
        blog_url = post_url if post_url else "https://blog.rentalops.ca"
        linkedin_text = generate_linkedin_post(blog_data, blog_url)
        if linkedin_text:
            post_to_linkedin(linkedin_text, image_data['url'] if image_data else None)
        print("\n" + "=" * 60)
        print("✅ Blog post automation completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Blog post automation failed.")
        print("=" * 60)
 
 
if __name__ == "__main__":
    main()
