import logging
from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Story
from utils import generate_story, generate_image, validate_age_appropriate

# Configure logging
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    logger.info("Story generation request received")
    
    try:
        # Get form data
        child_name = request.form.get('child_name', '').strip()
        child_age = request.form.get('child_age', '')
        story_type = request.form.get('story_type', '')

        # Validate form data
        if not all([child_name, child_age, story_type]):
            logger.warning("Missing required fields in form submission")
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('index'))

        try:
            child_age = int(child_age)
            if child_age < 1 or child_age > 12:
                raise ValueError("Age out of range")
        except ValueError:
            logger.warning(f"Invalid age value: {child_age}")
            flash('Age must be between 1 and 12', 'danger')
            return redirect(url_for('index'))

        if not validate_age_appropriate(child_age, story_type):
            logger.warning(f"Story type {story_type} not appropriate for age {child_age}")
            flash('Selected story type is not appropriate for this age', 'danger')
            return redirect(url_for('index'))

        # Generate story
        logger.info(f"Generating story for {child_name}, age {child_age}, type {story_type}")
        try:
            story_content = generate_story(child_name, child_age, story_type)
        except Exception as e:
            logger.error(f"Story generation failed: {str(e)}")
            flash('Failed to generate story. Please try again.', 'danger')
            return redirect(url_for('index'))

        # Generate image
        logger.info("Generating illustration for the story")
        try:
            image_url = generate_image(story_content)
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            image_url = "/static/images/default_story.svg"
            flash('Story created but could not generate a custom illustration.', 'warning')

        # Save to database
        try:
            story = Story(
                child_name=child_name,
                child_age=child_age,
                story_type=story_type,
                content=story_content,
                image_url=image_url
            )
            db.session.add(story)
            db.session.commit()
            logger.info("Story saved to database successfully")
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            db.session.rollback()
            flash('Story generated but could not be saved.', 'warning')

        return render_template('story.html', story=story)

    except Exception as e:
        logger.error(f"Unexpected error in generate route: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'danger')
        return redirect(url_for('index'))
