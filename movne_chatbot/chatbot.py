import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, ConversationChain
from flask import Flask, request, jsonify
import json
import logging

logger = logging.getLogger(__name__)

# טעינת משתני הסביבה
load_dotenv()

# יצירת אפליקציית Flask
app = Flask(__name__)

class MovneChatbot:
    def __init__(self):
        logger.info("אתחול הצ'אטבוט...")
        
        # הגדרת המודל של OpenAI
        self.llm = OpenAI(
            model="gpt-3.5-turbo-instruct",
            temperature=0.7,
            encoding="utf-8"
        )
        
        # הגדרת הזיכרון לשיחה
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output",
            human_prefix="Human",
            ai_prefix="AI"
        )
        
        # הגדרת שרשרת השיחה
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
        self.user_status: Dict[str, Dict[str, Any]] = {}
        self.product_knowledge: Dict[str, Any] = {}
        self.restricted_topics = ["תשואה", "קופון", "ריבית", "אחוז", "%"]
        self.marketing_responses = {
            "general_benefits": """
                המוצרים המובנים שלנו מציעים:
                - אפשרות להשקעה בשווקים הגלובליים
                - מנגנוני הגנה מובנים על ההשקעה
                - גמישות ונזילות - אפשרות למכור בכל יום מסחר
                - מעקב שוטף אחר ביצועי ההשקעה
                - ליווי מקצועי של מומחי השקעות
                האם תרצה לשמוע עוד על אחד מהיתרונות?
            """,
            "protection_info": """
                המוצרים שלנו כוללים מנגנוני הגנה מובנים שעוזרים לשמור על ההשקעה שלך.
                נשמח להסביר בפירוט על מנגנוני ההגנה בפגישה אישית.
            """,
            "ask_for_qualification": """
                כדי שנוכל להציג לך את כל הפרטים על המוצר והתנאים המדויקים,
                נשמח אם תמלא את שאלון ההתאמה הקצר שלנו.
                זה יעזור לנו להתאים עבורך את המוצר המתאים ביותר.
            """
        }
        self.setup_knowledge_base()
        
        logger.info("אתחול הצ'אטבוט הושלם בהצלחה")

    def setup_knowledge_base(self):
        """הגדרת בסיס הידע מקבצי PDF ו-Word"""
        # טעינת קבצי רגולציה
        pdf_path = os.path.join("data", "regulations", "regulation.pdf")
        docx_path = os.path.join("data", "regulations", "regulation.docx")
        
        all_docs = []
        
        if os.path.exists(pdf_path):
            pdf_loader = PyPDFLoader(pdf_path)
            all_docs.extend(pdf_loader.load())
            
        if os.path.exists(docx_path):
            word_loader = UnstructuredWordDocumentLoader(docx_path)
            all_docs.extend(word_loader.load())
        
        if all_docs:
            self.vectorstore = FAISS.from_documents(all_docs, self.embeddings)
            self.retriever = self.vectorstore.as_retriever()
            
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                self.llm,
                retriever=self.retriever,
                memory=self.memory
            )

    def load_product_knowledge(self, product_id: str):
        """טעינת מידע על מוצר ספציפי"""
        product_path = os.path.join("data", "products", f"{product_id}.pdf")
        if os.path.exists(product_path):
            loader = PyPDFLoader(product_path)
            docs = loader.load()
            self.product_knowledge[product_id] = FAISS.from_documents(docs, self.embeddings)
            return True
        return False

    def load_questionnaire(self) -> Dict:
        """טעינת שאלון מקובץ JSON"""
        questionnaire_path = os.path.join("data", "questionnaires", "questions.json")
        if os.path.exists(questionnaire_path):
            with open(questionnaire_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def check_accreditation(self, user_responses: Dict[str, bool]) -> bool:
        """בדיקת הסמכת המשקיע"""
        questionnaire = self.load_questionnaire()
        required_answers = questionnaire.get("required_answers", {
            "income": True,
            "assets": True,
            "investment_experience": True
        })
        return all(user_responses.get(k, False) for k in required_answers)

    def detect_language(self, text: str) -> str:
        """זיהוי שפת הטקסט"""
        if any(c in text for c in "אבגדהוזחטיכלמנסעפצקרשת"):
            return "he"
        return "en"

    def translate_response(self, response: str, target_lang: str) -> str:
        """תרגום התשובה לשפה הרצויה"""
        if target_lang == "he":
            return self.llm.invoke(f"Translate to Hebrew: {response}").content
        return response

    def is_user_qualified(self, user_id: str) -> bool:
        """בדיקה האם המשתמש כשיר ומילא את השאלון"""
        user_data = self.user_status.get(user_id, {})
        return user_data.get("questionnaire_completed", False) and user_data.get("is_qualified", False)

    def contains_restricted_info(self, response: str) -> bool:
        """בדיקה האם התשובה מכילה מידע מוגבל על תשואות וקופונים"""
        return any(topic in response.lower() for topic in self.restricted_topics)

    def process_query(self, user_id: str, query: str, product_id: str = None) -> str:
        """עיבוד שאילתת המשתמש"""
        user_data = self.user_status.get(user_id, {})
        lang = self.detect_language(query)
        
        # בדיקה אם השאלה מבקשת מידע על תשואות/קופונים
        if any(topic in query.lower() for topic in self.restricted_topics):
            if not self.is_user_qualified(user_id):
                return self.marketing_responses["ask_for_qualification"]
        
        # אם השאלה כללית על המוצר
        if any(term in query.lower() for term in ["איך עובד", "מה זה", "יתרונות", "הסבר על"]):
            return self.marketing_responses["general_benefits"]
        
        # אם השאלה על הגנה או סיכונים
        if any(term in query.lower() for term in ["הגנה", "סיכון", "בטוח"]):
            return self.marketing_responses["protection_info"]
        
        # קבלת תשובה מהמערכת
        try:
            if product_id and product_id in self.product_knowledge:
                response = self.product_knowledge[product_id].similarity_search(query)[0].page_content
            else:
                # אם אין מסמכים, נשתמש ב-LLM ישירות
                response = self.llm.invoke(query).content
            
            # בדיקה האם התשובה מכילה מידע מוגבל
            if self.contains_restricted_info(response) and not self.is_user_qualified(user_id):
                # החלפת המידע המוגבל בתשובה שיווקית
                return f"""
                    אנחנו מציעים מגוון מוצרים עם תנאים אטרקטיביים ומנגנוני הגנה מובנים.
                    כדי לקבל את כל הפרטים והתנאים המדויקים, נשמח אם תמלא את שאלון ההתאמה הקצר שלנו
                    או שתקבע פגישה עם אחד המומחים שלנו.
                """
            
            translated_response = self.translate_response(response, lang)
            return translated_response
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "מצטער, נתקלתי בבעיה בעיבוד השאלה. אנא נסה שוב או צור קשר עם התמיכה."

    def get_marketing_response(self, query_type: str) -> str:
        """קבלת תשובה שיווקית מותאמת לסוג השאלה"""
        return self.marketing_responses.get(query_type, self.marketing_responses["general_benefits"])

    def update_user_status(self, user_id: str, questionnaire_completed: bool, is_qualified: bool):
        """עדכון סטטוס המשתמש לאחר מילוי השאלון"""
        self.user_status[user_id] = {
            "questionnaire_completed": questionnaire_completed,
            "is_qualified": is_qualified,
            "last_update": None
        }

    def get_response(self, query: str) -> str:
        try:
            prompt = f"""
            אתה עוזר דיגיטלי של חברת מובנה גלובל, חברה המתמחה במוצרים פיננסיים מובנים.
            ענה בעברית על השאלה הבאה בצורה מקצועית ומנומסת:
            {query}
            """
            response = self.llm.predict(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"שגיאה בקבלת תשובה: {str(e)}")
            raise e

chatbot = MovneChatbot()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query")
    
    if not user_query:
        return jsonify({"error": "חסרה שאילתה"}), 400
    
    try:
        response = chatbot.get_response(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"שגיאה בעיבוד השאילתה: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000) 