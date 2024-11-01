import os
import requests
import anthropic
import json
import time
import logging
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from app import cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_age_appropriate(age, story_type):
    """Validate if the story type is appropriate for the child's age."""
    age_restrictions = {
        'fairy': 3,
        'adventure': 5,
        'educational': 0,
        'bedtime': 0
    }
    return age >= age_restrictions.get(story_type, 0)

def count_name_occurrences(text, name):
    """Count how many times a name appears in the text."""
    return text.lower().count(name.lower())

def generate_story(child_name, age, story_type, max_retries=3):
    """Generate a story using Claude AI with name consistency check."""
    logger.info(f"Generating story for {child_name}, age {age}, type {story_type}")
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY not found in environment variables")
        raise ValueError("ANTHROPIC_API_KEY is required")
        
    anthropic_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    prompt = f"""Write a {story_type} story for a {age}-year-old child named {child_name}. 
    IMPORTANT: Use the name "{child_name}" at least 3 times naturally throughout the story.
    The story should be age-appropriate, engaging, and educational. 
    It should be around 300-400 words long.
    For fairy tales, include magical elements and make {child_name} the main character.
    For adventure stories, include exciting but safe challenges that {child_name} overcomes.
    For educational stories, include learning moments about science or values that {child_name} discovers.
    For bedtime stories, include calming elements and a peaceful ending with {child_name} feeling safe and sleepy."""

    for attempt in range(max_retries):
        try:
            logger.info(f"Making API call to Claude AI (attempt {attempt + 1}/{max_retries})")
            response = anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            story = response.content[0].text
            
            # Check name occurrence
            name_count = count_name_occurrences(story, child_name)
            logger.info(f"Name '{child_name}' appears {name_count} times in the story")
            
            if name_count >= 3:
                logger.info("Story generated successfully with sufficient name occurrences")
                return story
            else:
                logger.warning(f"Story generated but only contains {name_count} occurrences of the name")
                if attempt < max_retries - 1:
                    continue
                
        except anthropic.APIError as e:
            logger.error(f"Claude AI API error: {str(e)}")
            if attempt == max_retries - 1:
                raise
        except Exception as e:
            logger.error(f"Unexpected error in generate_story: {str(e)}")
            if attempt == max_retries - 1:
                raise
    
    raise ValueError(f"Failed to generate story with sufficient name occurrences after {max_retries} attempts")

@cache.memoize(timeout=3600)  # Cache for 1 hour
def generate_image(story_content):
    """Generate an illustration using Leonardo AI with caching."""
    logger.info("Starting image generation process")
    
    if not os.environ.get("LEONARDO_API_KEY"):
        logger.error("LEONARDO_API_KEY not found in environment variables")
        raise ValueError("LEONARDO_API_KEY is required")
    
    try:
        # First, create a prompt for the image based on the story content
        prompt = f"A child-friendly, colorful illustration for a children's story: {story_content[:200]}..."
        logger.info(f"Generated image prompt: {prompt[:100]}...")
        
        headers = {
            "Authorization": f"Bearer {os.environ['LEONARDO_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "modelId": "ac614f96-1082-45bf-be9d-757f2d31c174",  # DreamShaper v8
            "num_images": 1,
            "width": 512,  # Reduced size for faster generation
            "height": 512,  # Reduced size for faster generation
            "promptMagic": True,
            "nsfw": False
        }
        
        # Initialize image generation
        logger.info("Making initial API call to Leonardo AI")
        response = requests.post(
            "https://cloud.leonardo.ai/api/rest/v1/generations",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            logger.error(f"Leonardo AI API error: {response.status_code} - {response.text}")
            raise Exception(f"Leonardo AI API returned status code {response.status_code}")
            
        generation_id = response.json()["sdGenerationJob"]["generationId"]
        logger.info(f"Successfully initiated image generation with ID: {generation_id}")
        
        # Poll for the generated image
        for attempt in range(30):  # Try for 30 seconds
            logger.info(f"Polling attempt {attempt + 1}/30 for generation ID: {generation_id}")
            time.sleep(1)
            
            status_response = requests.get(
                f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
                headers=headers
            )
            
            if status_response.status_code == 200:
                generated_images = status_response.json()["generations_by_pk"]["generated_images"]
                if generated_images:
                    image_url = generated_images[0]["url"]
                    logger.info(f"Successfully generated image: {image_url}")
                    return image_url
            
        logger.warning("Image generation timed out after 30 seconds")
        return "/static/images/default_story.svg"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error in generate_image: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_image: {str(e)}")
        raise
