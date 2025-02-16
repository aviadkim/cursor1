import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  console.log('Received request:', {
    method: req.method,
    body: req.body,
    headers: req.headers
  });

  if (req.method !== 'POST') {
    console.error(`Invalid method: ${req.method}`);
    return res.status(405).json({ 
      error: 'Method not allowed',
      details: `Expected POST, got ${req.method}`
    });
  }

  try {
    const { query, user_id } = req.body;

    if (!query || !user_id) {
      console.error('Missing required fields:', { query, user_id });
      return res.status(400).json({
        error: 'חסרים שדות חובה',
        details: {
          query: !query ? 'missing query' : 'ok',
          user_id: !user_id ? 'missing user_id' : 'ok'
        }
      });
    }

    console.log('Sending request to Python server:', {
      query,
      user_id
    });

    const response = await axios.post('http://localhost:5000/chat', {
      query,
      user_id
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json; charset=utf-8'
      },
      responseType: 'json'
    });

    console.log('Received response from Python server:', response.data);

    return res.status(200).json({
      response: response.data.response
    });
  } catch (error: any) {
    console.error('Chat error:', {
      message: error.message,
      stack: error.stack,
      response: error.response?.data
    });

    return res.status(500).json({ 
      error: 'Internal server error',
      details: error.message,
      pythonError: error.response?.data
    });
  }
} 