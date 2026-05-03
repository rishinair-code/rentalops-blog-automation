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
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": """You are an expert blog writer specializing in rental property management. 
You MUST respond with ONLY valid JSON. No markdown, no code blocks, no explanations.
Just pure JSON that can be directly parsed."""
            },
            {
                "role": "user",
                "content": f"""Write a blog post about: {topic}

Return ONLY this JSON structure (no other text, no markdown):
{{
  "title": "SEO-optimized title here",
  "metaDescription": "Compelling 140-150 character description",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "content": "Full article in markdown with ## headers and bullet points (900-1200 words)"
}}

Make the content practical and valuable for property managers."""
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
        
        # Clean the response - remove common formatting issues
        cleaned_response = ai_response.strip()
        
        # Remove markdown code blocks if present
        if cleaned_response.startswith('```'):
            # Extract content between code blocks
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
        
        # Find JSON object in the response
        # Look for the first { and last }
        start_idx = cleaned_response.find('{')
        end_idx = cleaned_response.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            print(f"❌ No JSON object found in response")
            print(f"Full response: {ai_response}")
            return None
        
        json_str = cleaned_response[start_idx:end_idx + 1]
        
        print(f"🔍 Extracted JSON (first 200 chars): {json_str[:200]}...")
        
        # Parse JSON
        blog_data = json.loads(json_str)
        
        # Validate required fields
        required_fields = ['title', 'metaDescription', 'tags', 'content']
        missing_fields = [field for field in required_fields if field not in blog_data]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return None
        
        # Ensure tags is a list
        if not isinstance(blog_data['tags'], list):
            blog_data['tags'] = []
        
        # Limit tags to 5
        blog_data['tags'] = blog_data['tags'][:5]
        
        print("✅ Content generated and validated successfully")
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
        print(f"Attempted to parse: {json_str[:500]}...")
        print(f"\nFull AI response:\n{ai_response}")
        return None
    except KeyError as e:
        print(f"❌ Error accessing response data: {e}")
        print(f"Response structure: {result}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error generating content: {e}")
        import traceback
        print(traceback.format_exc())
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
