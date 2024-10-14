const express = require('express');
const cors = require('cors');
const axios = require('axios');  // Add axios import here
const { Pool } = require('pg');
require('dotenv').config(); // Load environment variables from .env

// Create an instance of express
const app = express();
const port = process.env.PORT || 3000; // Use PORT from .env or default to 3000

// Use CORS to allow requests from the frontend
app.use(cors());
app.use(express.json());

// Setup PostgreSQL connection using environment variables
const pool = new Pool({
  user: process.env.PGUSER,
  host: process.env.PGHOST,
  database: process.env.PGDATABASE,
  password: process.env.PGPASSWORD,
  port: process.env.PGPORT,
});

// API endpoint for the chatbot
app.post('/api/chatbot', async (req, res) => {
  const { message } = req.body;

  try {
    // Call the chatbot function and get a response
    const chatbotResponse = await getChatbotResponse(message);

    // Optionally, store the user query and response in PostgreSQL
    await pool.query(
      'INSERT INTO chatlogs (user_message, bot_response) VALUES ($1, $2)',
      [message, chatbotResponse]
    );

    res.json({ response: chatbotResponse });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to get response from chatbot' });
  }
});

// Function to call the Flask RAG API
async function getChatbotResponse(message) {
    try {
      // Call the Flask RAG API
      const response = await axios.post('http://localhost:5001/api/rag', {
        message: message,
      });
  
      // Return the response from the Flask API
      return response.data.response;
    } catch (error) {
      console.error('Error calling RAG API:', error);
      throw new Error('Failed to fetch response from RAG API');
    }
  }

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

