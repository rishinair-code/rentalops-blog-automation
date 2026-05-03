import os
import json
import requests
import random
from datetime import datetime

# API Keys from GitHub Secrets (automatically loaded)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
HASHNODE_API_KEY = os.environ.get('HASHNODE_API_KEY')
HASHNODE_PUBLICATION_ID = os.environ.get('HASHNODE_PUBLICATION_ID')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')

# Blog topics for rental operations
TOPICS = [
    "tenant screening best practices",
    "property maintenance schedules",
    "lease agreement essentials",
    "rent collection strategies",
    "landlord legal compliance",
    "property marketing tips",
    "handling difficult tenants",
    "property inspection checklists",
    "rental property insurance",
    "eviction process guidelines",
    "rental property accounting",
    "property management software comparison",
    "seasonal property maintenance",
    "tenant retention strategies",
    "rental pricing optimization"
]

def generate_blog_content(topic):
    """Generate blog post using Groq AI"""
    print(f"🤖 Generating content about: {topic}")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert blog writer specializing in rental property management and operations. Write engaging, SEO-optimized, practical blog posts that help landlords and property managers. Always return valid JSON only, no other text."
            },
            {
                "role": "user",
                "content": f"""Write a comprehensive blog post (900-1200 words) about: {topic}

Return ONLY valid JSON with these exact keys:
- title: (catchy, SEO-optimized title)
- metaDescription: (compelling 140-150 character description)
- tags: (array of exactly 5 relevant tags)
- content: (full article in markdown format with ## headers, bullet points, and actionable tips)

Make it practical, actionable, and valuable for property managers."""
            }
        ],
        "temperature": 0.8,
        "max_tokens": 3000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Extract JSON from response (sometimes AI adds extra text)
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        blog_data = json.loads(content.strip())
        print("✅ Content generated successfully")
        return blog_data
        
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        return None

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
    
    # Select random topic
    topic = random.choice(TOPICS)
    print(f"\n📌 Selected topic: {topic}\n")
    
    # Generate blog content
    blog_data = generate_blog_content(topic)
    if not blog_data:
        print("❌ Failed to generate content. Exiting.")
        return
    
    # Get cover image
    image_data = get_unsplash_image(f"rental property {topic}")
    
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
