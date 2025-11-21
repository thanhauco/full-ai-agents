# API Documentation

## Overview

The AI Agent System provides a RESTful API for interacting with the agent.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

Check if the service is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-agent-system"
}
```

### Get Capabilities

Get information about agent capabilities.

**Endpoint:** `GET /capabilities`

**Response:**
```json
{
  "capabilities": [
    "text_generation",
    "multi_step_reasoning",
    "tool_execution",
    "memory_management"
  ],
  "models": ["gpt-4", "claude-3"],
  "features": {
    "multimodal": false,
    "streaming": true,
    "safety_filter": true
  }
}
```

### Chat

Send a message to the agent.

**Endpoint:** `POST /chat`

**Request Body:**
```json
{
  "message": "Hello, how can you help me?",
  "session_id": "session_123",
  "user_id": "user_456"
}
```

**Response:**
```json
{
  "message": "I can help you with various tasks...",
  "session_id": "session_123"
}
```

### Get Session

Get information about a session.

**Endpoint:** `GET /sessions/{session_id}`

**Response:**
```json
{
  "session_id": "session_123",
  "status": "active",
  "message_count": 5
}
```

### Delete Session

Delete a session and its history.

**Endpoint:** `DELETE /sessions/{session_id}`

**Response:**
```json
{
  "session_id": "session_123",
  "deleted": true
}
```

## Authentication

API endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Rate Limiting

- 60 requests per minute per user
- 1000 requests per hour per user

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request format"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing authentication token"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
