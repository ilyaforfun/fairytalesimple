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
    """Simulate Claude AI story generation."""
    # In a real implementation, this would make an API call to Claude AI
    return f"""Once upon a time, there was a brave child named {child_name} who loved to explore. 
    One day, they discovered a magical garden filled with talking flowers and friendly butterflies..."""

def generate_image(story_content):
    """Simulate Leonardo AI image generation."""
    # In a real implementation, this would make an API call to Leonardo AI
    return "/static/images/default_story.svg"
