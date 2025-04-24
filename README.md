# Kubernetes MCP Server

A Model Context Protocol (MCP) server for Kubernetes that enables Cursor to interact with Kubernetes clusters through natural language.

## Features

- Natural language interaction with Kubernetes clusters
- Real-time cluster state monitoring
- Modern web UI for visualization
- WebSocket-based MCP protocol implementation

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your Kubernetes configuration:

- Make sure you have a valid kubeconfig file
- The server will use your default Kubernetes context

3. Start the server:

```bash
python -m src.main
```

4. Access the UI:
   Open `http://localhost:8000` in your browser

## Project Structure

```
.
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── k8s/                 # Kubernetes client implementation
│   ├── mcp/                 # MCP protocol implementation
│   └── api/                 # API routes
├── ui/                      # React frontend
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Development

- Backend: FastAPI + Kubernetes Python Client
- Frontend: React + TypeScript
- Protocol: WebSocket-based MCP implementation
