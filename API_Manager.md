# AI Manager Tool

A desktop application that combines AI assistance with API testing capabilities. Get AI-powered answers to technical questions, API endpoints, and programming challenges, with integrated API testing functionality.

## Setup & Installation

### Requirements
- Python 3.8+
- Internet connection for AI features

### Quick Start
1. Clone or download this repository
2. Run the application:
```bash
python API_Manager.py
```

The application automatically installs required dependencies on first run:
- PyQt6: GUI framework
- requests: API handling
- openai: AI integration
- keyring: Secure key storage

### Manual Installation
If needed, install dependencies manually:
```bash
pip install -r requirements.txt
```

## Core Features

### AI Support
- Get instant answers to technical questions
- Find API endpoints and implementation details
- Receive coding guidance and solutions
- Access AI-powered technical documentation

### API Testing
- Configure and test API requests
- Save frequently used configurations
- Track request history
- Support for multiple data formats

## Usage Guide

### Initial Setup
1. Click "Configure API Keys"
2. Enter your OpenAI API key
3. Optionally add custom API keys for specific services

### Getting AI Support
1. Click "Get AI Support"
2. Enter your question or describe your need
   - Example: "I need the Microsoft Graph API endpoint for user profiles"
   - Example: "How do I implement OAuth2 authentication?"
   - Example: "What's the best way to handle rate limiting?"
3. View AI response with detailed explanations

### API Testing
1. Configure Request:
   - Select HTTP method
   - Enter API URL
   - Set headers (JSON format)
   - Choose body format (JSON/x-www-form-urlencoded)
   - Enter request body

2. Send and View:
   - Click "Send Request"
   - View response data
   - Check status codes
   - Save responses if needed

### Managing Configurations
- Save configurations using "New" button
- Double-click saved items to load
- Right-click for edit/delete options
- Configurations stored in `saved_requests.json`

## Components

### Main Interface
- Left Panel: Saved configurations
- Center: Request builder and tester
- Right: Response display
- Bottom: Request history

### Support Dialog
- Question/Issue input
- AI-powered response display
- Context-aware suggestions
- Code examples when relevant

### History Tab
- Complete request logs
- Response tracking
- Error history
- Status code monitoring

## Best Practices

### Getting Good AI Responses
- Be specific in your questions
- Include context when relevant
- Mention specific technologies/versions
- Ask follow-up questions for clarity

### API Testing
- Start with GET requests for testing
- Validate JSON before sending
- Check response headers
- Save working configurations

### Security
- Store sensitive keys securely
- Don't share API keys
- Review API responses before using
- Keep configurations backed up

## File Structure
- `API_Manager.py`: Main application
- `requirements.txt`: Dependencies
- `saved_requests.json`: Saved configurations
- `api_response.json`: Latest saved response

## Troubleshooting

### Common Issues
- API Key issues: Reconfigure keys
- Network errors: Check connection
- JSON errors: Validate format
- Missing dependencies: Run manual install

### Error Messages
- Invalid JSON: Check syntax
- API errors: Verify endpoint/auth
- Connection failed: Check network
- Rate limits: Space out requests

## Updates & Maintenance
- Dependencies auto-update on launch
- Configurations persist between sessions
- Regular backups recommended
- Check for new versions

Need help? The AI assistant can guide you through any feature or issue within the application.