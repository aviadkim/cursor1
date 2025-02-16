import { NextApiRequest, NextApiResponse } from 'next';
import { MovneChatbot } from '../../chatbot';

const chatbot = new MovneChatbot();

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { user_id, query, product_id } = req.body;

    if (!user_id || !query) {
      return res.status(400).json({
        error: 'חסרים פרטי משתמש או שאילתה',
      });
    }

    const response = await chatbot.processQuery(user_id, query, product_id);
    
    return res.status(200).json({ response });
  } catch (error: any) {
    console.error('Error in chat handler:', error);
    return res.status(500).json({
      error: `שגיאה בעיבוד השאילתה: ${error?.message || 'שגיאה לא ידועה'}`,
    });
  }
} 