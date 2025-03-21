# Data Analysis Agent System

## Architecture Overview

### Core Components
1. **Main Orchestrator** (`main.py`)
   - Central initialization point
   - Manages agent instances
   - Handles context management
   - Routes requests to appropriate agents

2. **Context Manager** (`context_manager.py`)
   - Maintains in-memory state
   - Tracks dataset profiles
   - Stores conversation history
   - Manages user inputs and agent outputs

3. **Agents**
   - Base EDA Agent: Initial data profiling
   - Dataset Profiler Agent: Detailed analysis
   - Insight Generator Agent: Pattern discovery
   - TB Agent: Code generation
   - Prompt Template Orchestrator: Conversation management

4. **API Layer** (`chat.py`)
   - REST endpoints for client communication
   - Request validation
   - Error handling and responses
   - Routes requests to main orchestrator

### Implementation Tasks

#### 1. Core Setup and Initialization
- [ ] Create agent factory in main.py
- [ ] Implement singleton pattern for agents
- [ ] Initialize context manager
- [ ] Set up error logging system
- [ ] Configure environment variables

#### 2. Context Management
- [ ] Implement in-memory state storage
- [ ] Create context update mechanisms
- [ ] Add conversation history tracking
- [ ] Implement context retrieval methods
- [ ] Add context validation

#### 3. Agent Integration
- [ ] Refactor agents for singleton pattern
- [ ] Add error handling in each agent
- [ ] Implement agent state management
- [ ] Create agent communication interfaces
- [ ] Add agent result validation

#### 4. API Development
- [ ] Create unified message handling
- [ ] Implement request validation
- [ ] Add error response formatting
- [ ] Create API documentation
- [ ] Add rate limiting

#### 5. Frontend Integration
- [ ] Implement message state management
- [ ] Add error handling UI
- [ ] Create loading states
- [ ] Implement retry mechanisms
- [ ] Add user feedback components

## Usage Guide

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration
```

### Starting the System
```bash
# Start the main application
python main.py

# In a separate terminal, start the API server
uvicorn codegen.api.chat:app --reload
```

### API Endpoints

#### POST /chat/message
Request:
```json
{
  "message": "string"
}
```

Response:
```json
{
  "message": "string",
  "code": "string (optional)"
}
```

### Error Handling

Each component implements its own error handling:

1. **Agents**
   - Input validation
   - Processing errors
   - Resource availability
   - API call failures

2. **Context Manager**
   - State corruption
   - Invalid updates
   - Missing data

3. **API Layer**
   - Request validation
   - Response formatting
   - HTTP error codes

## Development Guidelines

### 1. Error Handling
- Use custom exception classes
- Implement proper logging
- Provide meaningful error messages
- Add retry mechanisms where appropriate

### 2. State Management
- Use atomic operations
- Implement validation
- Maintain data consistency
- Handle concurrent access

### 3. Code Organization
- Follow single responsibility principle
- Use dependency injection
- Implement interface segregation
- Maintain clean architecture

### 4. Testing
- Unit tests for agents
- Integration tests for API
- Context manager tests
- End-to-end testing

## Directory Structure
```
codegen/
├── main.py              # Main orchestrator
├── agents/             # Agent implementations
│   ├── base_eda.py
│   ├── dataset_profiler_agent.py
│   ├── insight_gen_agent.py
│   ├── tb_agent.py
│   └── prompt_template_orchestrator.py
├── api/               # API endpoints
│   └── chat.py
├── app/              # Application core
│   ├── context_manager.py
│   └── models.py
├── uploads/          # Data storage
└── tests/            # Test suite
```

## Best Practices

1. **Code Quality**
   - Type hints
   - Documentation
   - Consistent formatting
   - Code reviews

2. **Performance**
   - Efficient data structures
   - Resource management
   - Caching when appropriate
   - Async operations

3. **Security**
   - Input validation
   - API key management
   - Rate limiting
   - Error message sanitization

4. **Maintainability**
   - Modular design
   - Clear documentation
   - Version control
   - Change logging