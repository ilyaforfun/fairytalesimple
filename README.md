# Magical Story Generator

A personalized fairytale generator that creates unique stories for children using AI. The application combines Claude AI for story generation and Leonardo AI for creating custom illustrations, making each story special and personalized.

## Features

- Personalized story generation based on child's name and age
- Multiple story types:
  - Fairy Tales
  - Adventure Stories
  - Educational Stories
  - Bedtime Stories
- Age-appropriate content filtering
- Custom AI-generated illustrations for each story
- Responsive web interface with dark theme
- Story caching for improved performance

## Technologies Used

- **Backend**: Python 3.x with Flask
- **Frontend**: Bootstrap 5 with dark theme
- **Database**: SQLite with SQLAlchemy ORM
- **AI Services**:
  - Claude AI (Anthropic) for story generation
  - Leonardo AI for image generation
- **Additional Libraries**:
  - Flask-SQLAlchemy for database management
  - Flask-Caching for performance optimization

## Setup Instructions

1. Create a new Replit project
2. Clone this repository or copy the files into your Replit project
3. Set up the required environment variables in Replit's Secrets tab:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude AI
   - `LEONARDO_API_KEY`: Your Leonardo AI API key
   - `FLASK_SECRET_KEY`: A secret key for Flask sessions (optional)

## Usage

1. Access the web interface through your Replit project URL
2. Enter the child's name and age (1-12 years)
3. Select a story type:
   - Fairy Tale (age 3+)
   - Adventure (age 5+)
   - Educational (all ages)
   - Bedtime Story (all ages)
4. Click "Generate Story" and wait for the magic to happen
5. The application will create a personalized story with an AI-generated illustration

## Project Structure

```
├── app.py              # Flask application configuration
├── main.py            # Application entry point
├── models.py          # Database models
├── routes.py          # Route handlers
├── utils.py           # Utility functions for AI integration
├── static/
│   ├── css/          # Custom styling
│   ├── images/       # Default images
│   └── js/           # Client-side JavaScript
└── templates/         # HTML templates
    ├── base.html     # Base template
    ├── index.html    # Story generation form
    └── story.html    # Story display page
```

## Key Features

1. **Personalization**
   - Stories incorporate the child's name multiple times
   - Age-appropriate content filtering
   - Different story types for various interests

2. **AI Integration**
   - Claude AI ensures high-quality, contextual storytelling
   - Leonardo AI creates unique illustrations for each story

3. **Performance**
   - Story caching to reduce API calls
   - Asynchronous image generation
   - Loading indicators for better user experience

4. **Safety**
   - Input validation for names and age
   - NSFW content filtering for images
   - Age-appropriate story type restrictions

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## Requirements

- Python 3.x
- Flask and its dependencies (requirements managed through Replit)
- Anthropic API key
- Leonardo AI API key

## Error Handling

The application includes comprehensive error handling for:
- API failures
- Invalid user input
- Database errors
- Image generation timeouts

## Note

This project is designed to run on Replit and uses Replit's environment for deployment. The dark theme is optimized for Replit's interface.
