"""
Google Gemini AI Assistant for SaarthiAI
Provides intelligent tutoring, explanations, quizzes, and flashcards
"""

import os
from datetime import datetime

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. AI features will be disabled.")

class GeminiAssistant:
    """AI Learning Assistant powered by Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini AI with API key from environment"""
        if not GEMINI_AVAILABLE:
            self.model = None
            self.chat_session = None
            return
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY', 'your_api_key_here')
        
        if api_key == 'your_api_key_here' or not api_key:
            print("⚠️  Warning: GEMINI_API_KEY not set in .env file")
            print("   AI features will use demo mode")
            self.model = None
            self.chat_session = None
            return
        
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Initialize model
            self.model = genai.GenerativeModel('gemini-pro')
            
            # Start chat session
            self.chat_session = self.model.start_chat(history=[])
            
            print("✅ Gemini AI initialized successfully")
            
        except Exception as e:
            print(f"⚠️  Error initializing Gemini AI: {e}")
            self.model = None
            self.chat_session = None
    
    def is_available(self):
        """Check if Gemini AI is available"""
        return self.model is not None and self.chat_session is not None
    
    def chat(self, message):
        """
        General chat with AI assistant
        
        Args:
            message: User's question or message
        
        Returns:
            AI response as string
        """
        if not self.is_available():
            return self._demo_response(message)
        
        try:
            # Add educational context
            prompt = f"""You are SaarthiAI, a friendly and helpful educational assistant for Indian students. 
You help students learn concepts in a simple, engaging way using examples relevant to Indian students.
Always be encouraging and supportive.

Student's question: {message}

Please provide a helpful, clear response:"""
            
            response = self.chat_session.send_message(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return f"I'm having trouble processing your request right now. Please try again later."
    
    def explain_topic(self, topic):
        """
        Explain a topic in simple language
        
        Args:
            topic: Topic to explain
        
        Returns:
            Detailed explanation
        """
        if not self.is_available():
            return self._demo_explain(topic)
        
        try:
            prompt = f"""As SaarthiAI, explain the following topic to an Indian high school or college student 
in simple, easy-to-understand language. Use relevant examples and analogies from everyday life.

Topic: {topic}

Please provide:
1. A brief introduction (2-3 sentences)
2. Key concepts explained simply
3. Real-world examples (preferably relevant to Indian context)
4. A simple summary

Explanation:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error explaining topic: {e}")
            return "I'm having trouble explaining this topic right now. Please try again later."
    
    def generate_quiz(self, topic, num_questions=5):
        """
        Generate a quiz on given topic
        
        Args:
            topic: Topic for quiz
            num_questions: Number of questions (default 5)
        
        Returns:
            Quiz in formatted text
        """
        if not self.is_available():
            return self._demo_quiz(topic)
        
        try:
            prompt = f"""Create a quiz for Indian students on the topic: {topic}

Generate {num_questions} multiple-choice questions with:
- 4 options (A, B, C, D)
- Clear question text
- One correct answer
- Brief explanation for the correct answer

Format each question as:
Question X: [Question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [Letter]
Explanation: [Brief explanation]

Quiz:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return "I'm having trouble generating a quiz right now. Please try again later."
    
    def create_flashcards(self, topic, num_cards=5):
        """
        Create flashcards for studying
        
        Args:
            topic: Topic for flashcards
            num_cards: Number of flashcards (default 5)
        
        Returns:
            Flashcards in formatted text
        """
        if not self.is_available():
            return self._demo_flashcards(topic)
        
        try:
            prompt = f"""Create {num_cards} study flashcards on the topic: {topic}

For each flashcard, provide:
- Front: A key concept, term, or question
- Back: Definition, explanation, or answer (keep it concise)

Format:
Flashcard X
Front: [Question/Term]
Back: [Answer/Definition]

Flashcards:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error creating flashcards: {e}")
            return "I'm having trouble creating flashcards right now. Please try again later."
    
    # Demo responses when API key not configured
    def _demo_response(self, message):
        """Demo response when Gemini not available"""
        return f"""**Demo Mode - AI Assistant**

I received your message: "{message}"

To enable full AI features:
1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
2. Add it to your .env file: GEMINI_API_KEY=your_key_here
3. Restart the application

For now, here's a helpful response:
I'm here to help you learn! Ask me about any topic in:
- Mathematics
- Science (Physics, Chemistry, Biology)
- Computer Science
- Languages
- History and Geography

I can:
✓ Explain topics in simple language
✓ Generate practice quizzes
✓ Create study flashcards
✓ Answer your questions

What would you like to learn today?"""
    
    def _demo_explain(self, topic):
        """Demo explanation when Gemini not available"""
        return f"""**Demo Mode - Topic Explanation**

Topic: {topic}

To get a detailed AI-powered explanation:
1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
2. Add it to your .env file
3. Restart the application

Meanwhile, here's a general approach:
- Break down the topic into key concepts
- Understand the fundamentals first
- Practice with examples
- Connect to real-world applications

Try searching for "{topic}" online or ask your teacher for help!"""
    
    def _demo_quiz(self, topic):
        """Demo quiz when Gemini not available"""
        return f"""**Demo Mode - Quiz**

Topic: {topic}

To generate an AI-powered quiz:
1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
2. Add it to your .env file
3. Restart the application

Sample Quiz Format:
Question 1: What is {topic}?
A) Option A
B) Option B
C) Option C
D) Option D
Correct Answer: (Configure API key to see answers)"""
    
    def _demo_flashcards(self, topic):
        """Demo flashcards when Gemini not available"""
        return f"""**Demo Mode - Flashcards**

Topic: {topic}

To generate AI-powered flashcards:
1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
2. Add it to your .env file
3. Restart the application

Sample Flashcard Format:
Flashcard 1
Front: Key Concept
Back: Definition/Explanation

Configure your API key to generate custom flashcards!"""

# Test the assistant
if __name__ == '__main__':
    print("=" * 50)
    print("Testing Gemini AI Assistant")
    print("=" * 50)
    
    assistant = GeminiAssistant()
    
    if assistant.is_available():
        print("\n✅ Gemini AI is available")
        
        # Test chat
        print("\n--- Testing Chat ---")
        response = assistant.chat("Hello! Can you help me with math?")
        print(response)
        
    else:
        print("\n⚠️  Gemini AI not available (API key not configured)")
        print("Running in demo mode...")