# צ'אטבוט שירות לקוחות Movne Global

צ'אטבוט AI מתקדם המשלב LangChain עם RAG לטיפול בשאלות לקוחות ומכירות מוצרים מובנים.

## תכונות עיקריות
- ✅ מענה לשאלות על מוצרים מובנים
- ✅ אימות משקיעים מוסמכים
- ✅ זיכרון שיחות קודמות
- ✅ תיעוד שיחות לצרכי רגולציה
- ✅ תמיכה בעברית ואנגלית
- ✅ אינטגרציה עם Firebase לאחסון נתונים

## דרישות מערכת
- Python 3.8 ומעלה
- חשבון OpenAI API
- חשבון Firebase

## התקנה

1. צור סביבת Python וירטואלית:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
venv\Scripts\activate.bat     # Windows CMD
```

2. התקן את החבילות הנדרשות:
```bash
pip install -r requirements.txt
```

3. הגדר את קובץ `.env`:
- הוסף את מפתח ה-API של OpenAI
- הגדר את נתיב קובץ האישורים של Firebase

4. הוסף את קובץ האישורים של Firebase (`firebase_creds.json`)

5. הוסף את קבצי התוכן הרגולטורי:
- `regulation.pdf`
- `regulation.docx`

## הפעלה

הפעל את השרת:
```bash
python chatbot.py
```

השרת יפעל בכתובת `http://localhost:5000`

## שימוש ב-API

שלח בקשת POST ל-`/chat` עם JSON בפורמט הבא:
```json
{
    "user_id": "unique_user_id",
    "query": "שאלת המשתמש כאן"
}
```

דוגמה לתשובה:
```json
{
    "response": "תשובת הצ'אטבוט כאן"
}
```

## אבטחה ורגולציה
- כל השיחות מתועדות ב-Firebase
- בדיקת הסמכת משקיעים לפני חשיפת מידע רגיש
- תמיכה בדרישות רגולטוריות

## תמיכה
לשאלות ותמיכה, צור קשר עם צוות הפיתוח. 