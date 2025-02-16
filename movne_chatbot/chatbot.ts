export class MovneChatbot {
  async processQuery(userId: string, query: string, productId?: string): Promise<string> {
    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        query: query,
        product_id: productId,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'שגיאה בעיבוד השאילתה');
    }

    return data.response;
  }
} 