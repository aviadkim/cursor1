import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_connection():
    """בדיקת חיבור ל-OpenAI וזמינות מודלים"""
    try:
        load_dotenv()
        client = OpenAI()
        
        # בדיקת חיבור בסיסית
        print("בודק חיבור ל-OpenAI...")
        models = client.models.list()
        print("\nמודלים זמינים:")
        for model in models.data:
            if "gpt" in model.id:
                print(f"- {model.id}")
        
        # בדיקת שליחת הודעה
        print("\nבודק שליחת הודעת טסט...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Test successful' in Hebrew"}]
        )
        print(f"תשובה מהשרת: {response.choices[0].message.content}")
        
        return True
    except Exception as e:
        print(f"\nשגיאה בבדיקה: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection() 