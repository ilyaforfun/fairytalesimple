from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Story
from utils import generate_story, generate_image, validate_age_appropriate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        child_name = request.form.get('child_name')
        child_age = int(request.form.get('child_age'))
        story_type = request.form.get('story_type')

        if not all([child_name, child_age, story_type]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('index'))

        if not validate_age_appropriate(child_age, story_type):
            flash('Selected story type is not appropriate for this age', 'error')
            return redirect(url_for('index'))

        # Generate story and image
        story_content = generate_story(child_name, child_age, story_type)
        image_url = generate_image(story_content)

        # Save to database
        story = Story(
            child_name=child_name,
            child_age=child_age,
            story_type=story_type,
            content=story_content,
            image_url=image_url
        )
        db.session.add(story)
        db.session.commit()

        return render_template('story.html', story=story)

    except Exception as e:
        flash('An error occurred while generating the story', 'error')
        return redirect(url_for('index'))
