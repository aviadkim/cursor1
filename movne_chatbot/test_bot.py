from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from huggingface_hub import InferenceClient
import os

def test_chatbot():
    """בדיקת פונקציונליות בסיסית של הצ'אטבוט"""
    try:
        # טעינת משתני הסביבה
        load_dotenv()
        
        # יצירת מודל השיחה
        chat = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0)
        
        # שליחת שאלת בדיקה
        response = chat.invoke("תגיד 'הצ'אטבוט עובד!' בעברית")
        
        print(f"תשובה מהצ'אטבוט: {response.content}")
        return True
        
    except Exception as e:
        print(f"שגיאה בבדיקה: {str(e)}")
        return False

def test_huggingface():
    """בדיקת חיבור ל-Hugging Face"""
    try:
        # טעינת משתני הסביבה
        load_dotenv()
        
        # יצירת לקוח HuggingFace
        client = InferenceClient(token=os.getenv('HUGGINGFACE_API_TOKEN'))
        
        # שליחת שאלת בדיקה
        response = client.text_generation(
            "תגיד 'החיבור ל-Hugging Face עובד!' בעברית",
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_new_tokens=100
        )
        
        print(f"תשובה מ-Hugging Face: {response}")
        return True
        
    except Exception as e:
        print(f"שגיאה בבדיקת Hugging Face: {str(e)}")
        return False

if __name__ == "__main__":
    test_chatbot()
    test_huggingface() 