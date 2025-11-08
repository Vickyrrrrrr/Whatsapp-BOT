"""
Test script to verify Gemini integration works
Run this to test AI responses without WhatsApp
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
    print("\n📝 To get your API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Create an API key")
    print("3. Add to .env file: GEMINI_API_KEY=your_key_here")
    exit(1)

print("✅ Gemini API Key found!")
print("🧪 Testing Gemini AI...\n")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    test_question = "What is University of Lucknow known for? Answer in 2 sentences."
    print(f"Question: {test_question}\n")
    
    response = model.generate_content(test_question)
    print(f"Gemini Response:\n{response.text}\n")
    
    print("✅ Gemini AI integration working perfectly!")
    print("\n🎉 Your WhatsApp bot can now answer ANY student question!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nCheck:")
    print("- Is your API key valid?")
    print("- Do you have internet connection?")
    print("- Is google-generativeai package installed?")
