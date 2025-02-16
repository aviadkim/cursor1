import type { NextPage } from 'next';
import Head from 'next/head';
import { ChatInterface } from '../components/ChatInterface';

const Home: NextPage = () => {
  return (
    <div>
      <Head>
        <title>Movne Global Assistant</title>
        <meta name="description" content="Movne Global Structured Products Assistant" />
        <link rel="icon" href="/favicon.ico" />
        <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;500;600&display=swap" rel="stylesheet" />
      </Head>

      <main style={{ 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0f0f1f 0%, #1a1a2e 100%)'
      }}>
        <ChatInterface />
      </main>
    </div>
  );
};

export default Home; 