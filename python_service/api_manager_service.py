import os
import openai
import keyring
from aiohttp import web
import json

class APIManagerService:
    def __init__(self):
        """Initialize service and load API key"""
        print("Initializing API Manager Service...")
        self.api_key = None
        self.load_api_key()

    def load_api_key(self):
        """Load OpenAI API key from keyring"""
        try:
            print("Attempting to load OpenAI API key...")
            self.api_key = keyring.get_password("APIAutomationTool", "OpenAI API Key")
            
            if self.api_key:
                print(f"Found API key (starts with: {self.api_key[:7]}...)")
                # Set it both ways to be sure
                openai.api_key = self.api_key
                os.environ["OPENAI_API_KEY"] = self.api_key
                print("API key has been set")
            else:
                print("❌ No API key found in keyring!")
                raise ValueError("No API key found in keyring. Please set it using API_Manager.py")
            
        except Exception as e:
            print(f"❌ Error loading API key: {str(e)}")
            raise

    def get_ai_response(self, question: str) -> str:
        """Get AI response for a question"""
        try:
            print("\nGetting AI response...")
            print(f"Current API key starts with: {self.api_key[:7] if self.api_key else 'None'}")
            
            # Double-check key is set
            if not self.api_key:
                return "Error: API key not loaded"

            # Create client with explicit key
            client = openai.OpenAI(
                api_key=self.api_key
            )
            print("OpenAI client created")

            prompt = f"""
            Help me with this technical question or API requirement:
            {question}

            Please provide:
            1. Detailed explanation or solution
            2. Code examples if relevant
            3. API endpoints and implementation details if requested
            4. Best practices and recommendations

            Format the response in a clear, structured way.
            """

            print("Sending request to OpenAI...")
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            print("Got response from OpenAI")
            
            # Add these debug prints
            ai_response = response.choices[0].message.content
            print("Response content:", ai_response[:100], "...") # Print first 100 chars
            return ai_response
            

        except Exception as e:
            error_msg = f"Error in get_ai_response: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    async def handle_ai_query(self, request):
        """Handle incoming AI queries"""
        try:
            print("\nReceived new AI query request")
            data = await request.json()
            question = data.get('question')
            
            if not question:
                return web.Response(
                    text=json.dumps({
                        'status': 'error', 
                        'error': 'No question provided'
                    }),
                    content_type='application/json'
                )

            print(f"Processing question: {question[:50]}...")
            response = self.get_ai_response(question)
            
            return web.Response(
                text=json.dumps({
                    'status': 'success', 
                    'response': response
                }),
                content_type='application/json'
            )
        
        
            
        except Exception as e:
            error_msg = f"Error handling query: {str(e)}"
            print(f"❌ {error_msg}")
            return web.Response(
                text=json.dumps({
                    'status': 'error', 
                    'error': error_msg
                }),
                content_type='application/json'
            )

# Create and run the web application
print("\nStarting API Manager Service...")
app = web.Application()
service = APIManagerService()

# Add routes
app.router.add_post('/ai-query', service.handle_ai_query)

if __name__ == '__main__':
    import os  # Add this at the top with other imports
    print("\nStarting web server...")
    web.run_app(app, port=3000)