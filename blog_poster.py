import os
import json
import requests
from datetime import datetime

# API Keys from GitHub Secrets (automatically loaded)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
HASHNODE_API_KEY = os.environ.get('HASHNODE_API_KEY')
HASHNODE_PUBLICATION_ID = os.environ.get('HASHNODE_PUBLICATION_ID')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
HASHNODE_BLOG_HOST = os.environ.get('HASHNODE_BLOG_HOST')

# Blog topics for rental operations
import hashlib

# Persona definitions — Canada-wide
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
def fetch_recent_posts():
    """Fetch recent post titles and URLs from Hashnode for cross-linking"""
    if not HASHNODE_BLOG_HOST:
        print("⚠️  HASHNODE_BLOG_HOST not set — skipping cross-link fetch")
        return []

    url = "https://gql.hashnode.com"
    headers = {
        "Authorization": HASHNODE_API_KEY,
        "Content-Type": "application/json"
    }

    query = """
    query GetRecentPosts($host: String!) {
        publication(host: $host) {
            posts(first: 20) {
                edges {
                    node {
                        title
                        url
                    }
                }
            }
        }
    }
    """

    payload = {
        "query": query,
        "variables": {"host": HASHNODE_BLOG_HOST}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        if 'errors' in result:
            print(f"⚠️  Could not fetch posts for cross-linking: {result['errors']}")
            return []

        edges = result['data']['publication']['posts']['edges']
        posts = [{"title": e['node']['title'], "url": e['node']['url']} for e in edges]
        print(f"📚 Found {len(posts)} existing posts available for cross-linking")
        return posts

    except Exception as e:
        print(f"⚠️  Cross-link fetch failed (non-critical, continuing): {e}")
        return []


def find_related_post(posts, topic):
    """Find the most topically related existing post to cross-link"""
    if not posts:
        return None

    topic_words = set(topic.lower().split())
    # Remove common filler words that would create false matches
    stopwords = {'a', 'an', 'the', 'and', 'or', 'for', 'in', 'of', 'to', 'vs', 'how', 'what', 'why', 'your'}
    topic_words -= stopwords

    best_match = None
    best_score = 0

    for post in posts:
        title_words = set(post['title'].lower().split()) - stopwords
        score = len(topic_words & title_words)
        if score > best_score:
            best_score = score
            best_match = post

    if best_score >= 1 and best_match:
        print(f"🔗 Cross-link match found: '{best_match['title']}'")
        return best_match

    # Fall back to most recent post if no keyword match
    if posts:
        print(f"🔗 No keyword match — using most recent post as cross-link")
        return posts[0]

    return None


def should_include_roi_section():
    """Return True every 3rd week — those posts include a cost/ROI section"""
    week_number = datetime.now().isocalendar()[1]
    return week_number % 3 == 0
def get_used_topics():
    """Read used topics from local file (checked out by Actions)"""
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
    """Save used topic to local file — git commit happens in workflow"""
    try:
        used = get_used_topics()
        if topic not in used:
            used.append(topic)
        with open("used_topics.json", "w") as f:
            json.dump(used, f, indent=2)
        print(f"✅ Topic saved: {topic[:50]}")
    except Exception as e:
        print(f"⚠️  Could not save used topic: {e}")

def get_current_persona():
    """Rotate personas evenly using the current week number — no state file needed"""
    week_number = datetime.now().isocalendar()[1]
    persona_index = week_number % len(PERSONAS)
    return PERSONAS[persona_index]

def generate_blog_content():
    """Generate persona-targeted blog post using Groq AI"""
    
    persona = get_current_persona()

    # Pick a topic that hasn't been used yet
    used_topics = get_used_topics()
    available_topics = [t for t in persona["topics"] if t not in used_topics]

    if not available_topics:
        print(f"🔄 All topics for {persona['name']} used — resetting")
        available_topics = persona["topics"]

    day_of_year = datetime.now().timetuple().tm_yday
    topic_index = day_of_year % len(available_topics)
    topic = available_topics[topic_index]

    print(f"🎯 Target persona: {persona['name']}")
    print(f"🤖 Generating content about: {topic}")

    # Fetch existing posts for cross-linking
    recent_posts = fetch_recent_posts()
    related_post = find_related_post(recent_posts, topic)

    # Decide if this post gets a cost/ROI section
    include_roi = should_include_roi_section()
    print(f"💰 ROI/cost section: {'Yes' if include_roi else 'No'}")

    # Build optional prompt additions
    crosslink_instruction = ""
    if related_post:
        crosslink_instruction = f"""
CROSS-LINKING (mandatory):
Naturally link to this related post somewhere in the article body where it genuinely fits:
Title: "{related_post['title']}"
URL: {related_post['url']}
Use descriptive anchor text — never just "click here". Example: [how to serve an N4 notice correctly]({related_post['url']})
"""

    roi_instruction = ""
    if include_roi:
        roi_instruction = """
COST/ROI SECTION (mandatory for this post):
Include a section titled "## What This Mistake Actually Costs You" or "## Is [Tool/System] Worth It? A Real-Money Breakdown".
Use realistic CAD figures relevant to Canadian landlords. Show the cost of the manual/wrong approach vs. the cost of doing it properly (time saved, fines avoided, missed deductions recovered, etc.).
Example structure: "A missed CRA deduction on a $2,400 repair bill costs a landlord in the 33% tax bracket roughly $792 in avoidable tax. Over 5 years of similar misses, that's nearly $4,000 left on the table."
End the section with a natural mention of how [RentalOps](https://rentalops.ca) addresses this specific cost.
"""
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
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
- Write for Canadian landlords. Reference the correct provincial tribunal, legislation, and rules for the topic.
- If the topic is province-specific, go deep on that province. If it applies nationally, compare provinces where useful.
- Never give generic US advice. Everything must be Canada-specific.
- Do not recommend US tools as viable options for Canadian landlords.
- You MUST respond with ONLY valid JSON. No markdown, no code blocks, no explanations. Raw JSON only."""

            },
            {
                "role": "user",
                "content": f"""Write a blog post targeting {persona['name']} landlords about: {topic}

Return ONLY this JSON structure (no other text, no markdown):
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
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        print(f"📥 Raw AI response (first 200 chars): {ai_response[:200]}...")
        
        cleaned_response = ai_response.strip()
        
        if cleaned_response.startswith('```'):
            lines = cleaned_response.split('\n')
            cleaned_lines = []
            in_code_block = False
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if not in_code_block:
                    cleaned_lines.append(line)
            cleaned_response = '\n'.join(cleaned_lines).strip()
        
        start_idx = cleaned_response.find('{')
        end_idx = cleaned_response.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            print(f"❌ No JSON object found in response")
            return None
        
        json_str = cleaned_response[start_idx:end_idx + 1]
        blog_data = json.loads(json_str)
        
        required_fields = ['title', 'metaDescription', 'tags', 'content']
        missing_fields = [field for field in required_fields if field not in blog_data]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return None
        
        if not isinstance(blog_data['tags'], list):
            blog_data['tags'] = []
        blog_data['tags'] = blog_data['tags'][:5]
        
        print("✅ Content generated successfully")
        print(f"   Persona: {persona['name']}")
        print(f"   Title: {blog_data['title'][:60]}...")
        print(f"   Tags: {', '.join(blog_data['tags'])}")
        print(f"   Content length: {len(blog_data['content'])} characters")
        
        return blog_data
        
    except requests.exceptions.Timeout:
        print(f"❌ Error: API request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error making API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        print(traceback.format_exc())
        return None
def generate_image_query(title):
    """Extract a short, varied Unsplash search query from the blog title"""
    # Map common rental topics to visually distinct search terms
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
    ]

    title_lower = title.lower()
    for keywords, query in topic_map:
        if any(k in title_lower for k in keywords):
            print(f"🖼️  Image query: '{query}'")
            return query

    # Fallback — generic but at least varied by adding a random aspect
    import random
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
    """Fetch relevant image from Unsplash"""
    print(f"🖼️  Fetching image for: {query}")
    
    url = f"https://api.unsplash.com/photos/random"
    params = {
        "query": query,
        "orientation": "landscape",
        "client_id": UNSPLASH_ACCESS_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        image_data = response.json()
        image_url = image_data['urls']['regular']
        photographer = image_data['user']['name']
        photographer_url = image_data['user']['links']['html']
        
        print(f"✅ Image found by {photographer}")
        
        return {
            'url': image_url,
            'credit': f"Photo by [{photographer}]({photographer_url}) on [Unsplash](https://unsplash.com)"
        }
        
    except Exception as e:
        print(f"⚠️  Error fetching image: {e}")
        return None

def publish_to_hashnode(blog_data, image_data):
    """Publish blog post to Hashnode"""
    print("📤 Publishing to Hashnode...")
    
    url = "https://gql.hashnode.com"
    
    headers = {
        "Authorization": HASHNODE_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Add image to content if available
    content = blog_data['content']
    if image_data:
        content = f"![Cover Image]({image_data['url']})\n\n{content}\n\n---\n\n*{image_data['credit']}*"
    
    # Prepare tags - Hashnode expects tag slugs
    tags = []
    for tag in blog_data.get('tags', [])[:5]:
        # Convert tag to slug format (lowercase, hyphenated)
        tag_slug = tag.lower().replace(' ', '-').replace('_', '-')
        tags.append({"slug": tag_slug, "name": tag})
    
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post {
                id
                title
                url
                slug
            }
        }
    }
    """
    
    variables = {
        "input": {
            "title": blog_data['title'],
            "contentMarkdown": content,
            "tags": tags,
            "publicationId": HASHNODE_PUBLICATION_ID,
            "metaTags": {
                "description": blog_data['metaDescription']
            }
        }
    }
    
    payload = {
        "query": mutation,
        "variables": variables
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if 'errors' in result:
            print(f"❌ Hashnode API Error: {result['errors']}")
            return False
        
        post = result['data']['publishPost']['post']
        print(f"✅ Post published successfully!")
        print(f"📝 Title: {post['title']}")
        print(f"🔗 URL: {post['url']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error publishing to Hashnode: {e}")
        return False

def main():
    """Main function to orchestrate the blog posting"""
    print("=" * 60)
    print("🚀 RentalOps Blog Automation Starting...")
    print("=" * 60)
    
    # Check if all API keys are present
    if not all([GROQ_API_KEY, HASHNODE_API_KEY, HASHNODE_PUBLICATION_ID, UNSPLASH_ACCESS_KEY]):
        print("❌ Missing API keys! Please check GitHub Secrets.")
        return
    
    blog_data = generate_blog_content()
    if not blog_data:
        print("❌ Failed to generate content. Exiting.")
        return
    
    # Get cover image
    image_search_query = generate_image_query(blog_data['title'])
    image_data = get_unsplash_image(image_search_query)
    
    # Publish to Hashnode
    success = publish_to_hashnode(blog_data, image_data)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Blog post automation completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Blog post automation failed.")
        print("=" * 60)

if __name__ == "__main__":
    main()
