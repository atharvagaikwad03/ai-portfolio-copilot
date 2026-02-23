/**
 * Node.js Express server for AI Portfolio Copilot
 * Acts as a gateway between frontend and Python backend
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.NODE_API_PORT || 3000;
const PYTHON_API_URL = `http://localhost:${process.env.PYTHON_API_PORT || 8000}`;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve frontend (chat UI) - path from backend/nodejs to project root then frontend
const frontendPath = path.join(__dirname, '..', '..', 'frontend');
app.use('/app', express.static(frontendPath));
app.get('/app', (req, res) => {
  res.sendFile(path.join(frontendPath, 'example.html'));
});
app.get('/', (req, res, next) => {
  // If they want HTML, redirect to chat app; otherwise return API info
  const acceptsHtml = req.accepts('html');
  if (acceptsHtml && req.get('sec-fetch-dest') !== 'empty') {
    return res.redirect(302, '/app/example.html');
  }
  next();
});

// Request logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    // Check Python backend health
    const pythonHealth = await axios.get(`${PYTHON_API_URL}/health`).catch(() => null);
    
    res.json({
      status: 'healthy',
      nodejs: 'running',
      python_backend: pythonHealth ? 'connected' : 'disconnected',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      error: error.message
    });
  }
});

// Chat endpoint - proxy to Python backend
app.post('/api/chat', async (req, res) => {
  try {
    const { message, session_id, enable_evaluation } = req.body;
    
    if (!message) {
      return res.status(400).json({
        error: 'Message is required'
      });
    }
    
    // Forward request to Python backend
    const response = await axios.post(`${PYTHON_API_URL}/api/chat`, {
      message,
      session_id,
      enable_evaluation
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error in chat endpoint:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json({
        error: error.response.data.detail || error.message
      });
    } else {
      res.status(500).json({
        error: 'Internal server error',
        message: error.message
      });
    }
  }
});

// Documents endpoint - proxy to Python backend
app.post('/api/documents', async (req, res) => {
  try {
    const response = await axios.post(
      `${PYTHON_API_URL}/api/documents`,
      req.body
    );
    
    res.json(response.data);
  } catch (error) {
    console.error('Error in documents endpoint:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.detail || error.message
    });
  }
});

// Stats endpoint - proxy to Python backend
app.get('/api/stats', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/api/stats`);
    res.json(response.data);
  } catch (error) {
    console.error('Error in stats endpoint:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.detail || error.message
    });
  }
});

// Clear documents endpoint
app.delete('/api/documents', async (req, res) => {
  try {
    const response = await axios.delete(`${PYTHON_API_URL}/api/documents`);
    res.json(response.data);
  } catch (error) {
    console.error('Error clearing documents:', error.message);
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.detail || error.message
    });
  }
});

// Root endpoint (API info when requested as JSON or by tools)
app.get('/', (req, res) => {
  res.json({
    message: 'AI Portfolio Copilot - Node.js Gateway',
    version: '1.0.0',
    chatApp: 'http://localhost:' + PORT + '/app/example.html',
    endpoints: {
      health: '/health',
      chat: 'POST /api/chat',
      documents: 'POST /api/documents',
      stats: 'GET /api/stats'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Node.js server running on port ${PORT}`);
  console.log(`📡 Python backend expected at ${PYTHON_API_URL}`);
  console.log(`🌐 Health check: http://localhost:${PORT}/health`);
});

module.exports = app;
