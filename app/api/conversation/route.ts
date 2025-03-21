import { NextRequest, NextResponse } from 'next/server';
import { PythonShell, Options } from 'python-shell';
import path from 'path';

interface OrchestratorResponse {
    text: string;
    done?: boolean;
}

interface ConversationState {
    pyshell: PythonShell;
    turnCount: number;
}

// Store orchestrator instances in memory (consider using a proper session store in production)
const orchestrators: Map<string, ConversationState> = new Map();

export async function POST(req: NextRequest) {
    try {
        const data = await req.json();
        
        // Generate a session ID if not provided
        const sessionId = req.headers.get('X-Session-ID') || crypto.randomUUID();
        
        // Initialize Python shell options
        const options: Options = {
            mode: 'json' as const,
            pythonPath: 'python3',
            scriptPath: path.join(process.cwd(), 'codegen/agents')
        };

        // Handle conversation initialization
        if (data.type === 'initialize' && data.profile) {
            const pyshell = new PythonShell('prompt_template_orchestrator.py', options);
            
            return new Promise((resolve, reject) => {
                pyshell.send({ action: 'initialize', profile: data.profile });
                
                pyshell.on('message', (message: OrchestratorResponse) => {
                    // Store the Python process reference
                    orchestrators.set(sessionId, { 
                        pyshell,
                        turnCount: 0
                    });
                    
                    resolve(NextResponse.json({
                        message: message.text,
                        sessionId: sessionId
                    }, { 
                        status: 200,
                        headers: { 'X-Session-ID': sessionId }
                    }));
                });
                
                pyshell.on('error', (error: Error) => {
                    reject(NextResponse.json({ error: error.message }, { status: 500 }));
                });
            });
        }
        
        // Handle user messages
        if (data.type === 'message' && data.message) {
            const state = orchestrators.get(sessionId);
            
            if (!state) {
                return NextResponse.json(
                    { error: 'Conversation not initialized' },
                    { status: 400 }
                );
            }
            
            return new Promise((resolve, reject) => {
                state.pyshell.send({ action: 'process', message: data.message });
                
                state.pyshell.on('message', (message: OrchestratorResponse) => {
                    state.turnCount += 1;
                    resolve(NextResponse.json({
                        message: message.text,
                        done: message.done || state.turnCount >= 3,
                        sessionId: sessionId
                    }));
                });
                
                state.pyshell.on('error', (error: Error) => {
                    reject(NextResponse.json({ error: error.message }, { status: 500 }));
                });
            });
        }
        
        return NextResponse.json(
            { error: 'Invalid request format' },
            { status: 400 }
        );
        
    } catch (error) {
        console.error('Conversation API error:', error);
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        );
    }
}
