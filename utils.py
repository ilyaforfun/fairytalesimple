import os
import requests
import anthropic
import json
import time
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

def validate_age_appropriate(age, story_type):
    """Validate if the story type is appropriate for the child's age."""
    age_restrictions = {
        'fairy': 3,
        'adventure': 5,
        'educational': 0,
        'bedtime': 0
    }
    return age >= age_restrictions.get(story_type, 0)

def generate_story(child_name, age, story_type):
    """Generate a story using Claude AI."""
    anthropic_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    prompt = f"""Write a {story_type} story for a {age}-year-old child named {child_name}. 
    The story should be age-appropriate, engaging, and educational. 
    It should be around 300-400 words long.
    For fairy tales, include magical elements.
    For adventure stories, include exciting but safe challenges.
    For educational stories, include learning moments about science or values.
    For bedtime stories, include calming elements and a peaceful ending."""

    try:
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error generating story: {e}")
        return f"""Once upon a time, there was a brave child named {child_name} who loved to explore. 
        One day, they discovered a magical garden filled with talking flowers and friendly butterflies..."""

def generate_image(story_content):
    """Generate an illustration using Leonardo AI."""
    try:
        # First, create a prompt for the image based on the story content
        prompt = f"A child-friendly, colorful illustration for a children's story: {story_content[:200]}..."
        
        # Create the image generation request
        headers = {
            "Authorization": f"Bearer {os.environ['LEONARDO_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "modelId": "ac614f96-1082-45bf-be9d-757f2d31c174",  # DreamShaper v8
            "num_images": 1,
            "width": 768,
            "height": 768,
            "promptMagic": True,
            "nsfw": False
        }
        
        # Initialize image generation
        response = requests.post(
            "https://cloud.leonardo.ai/api/rest/v1/generations",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            return "/static/images/default_story.svg"
            
        generation_id = response.json()["sdGenerationJob"]["generationId"]
        
        # Poll for the generated image
        for _ in range(30):  # Try for 30 seconds
            time.sleep(1)
            status_response = requests.get(
                f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
                headers=headers
            )
            
            if status_response.status_code == 200:
                generated_images = status_response.json()["generations_by_pk"]["generated_images"]
                if generated_images:
                    return generated_images[0]["url"]
            
        return "/static/images/default_story.svg"
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return "/static/images/default_story.svg"
