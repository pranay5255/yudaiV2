import { NextRequest, NextResponse } from 'next/server';
import { writeFile, mkdir, readFile } from 'fs/promises';
import { join } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { existsSync } from 'fs';
import { DatasetProfile } from '../../../codegen/app/models';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as File;
        
        if (!file) {
            return NextResponse.json(
                { error: 'No file provided' },
                { status: 400 }
            );
        }

        // Ensure upload directories exist
        const uploadDir = join(process.cwd(), 'codegen', 'app', 'uploads');
        
        if (!existsSync(uploadDir)) {
            await mkdir(uploadDir, { recursive: true });
        }

        // Save the uploaded file
        const uploadPath = join(uploadDir, file.name);
        const bytes = await file.arrayBuffer();
        const buffer = Buffer.from(bytes);
        await writeFile(uploadPath, buffer);

        try {
            // Execute the Python profiling script
            const scriptPath = join(process.cwd(), 'codegen/agents/base_eda.py');
            console.log(scriptPath);
            console.log(uploadPath);

            const { stdout, stderr } = await execAsync(`pnpm exec python3 "${scriptPath}" "${uploadPath}"`);
            
            // Only throw if stderr contains actual error messages (not INFO logs)
            if (stderr && !stderr.includes('INFO:')) {
                console.error('Python script error:', stderr);
                throw new Error(stderr);
            }

            // Get the profile JSON file path from Python output
            const profilePath = stderr.includes('Profile saved to:') 
                ? stderr.split('Profile saved to:')[1].trim()
                : stdout.trim();
            
            // Read and parse the profile JSON file
            const profileContent = await readFile(profilePath, 'utf-8');
            const profileData = JSON.parse(profileContent) as DatasetProfile;

            // Validate the profile data structure
            if (!profileData.analysis || !profileData.table || !profileData.variables) {
                throw new Error('Invalid profile data structure');
            }

            // Initialize context with the new profile
            const initContextPath = join(process.cwd(), 'codegen/scripts/init_context.py');
            await execAsync(`pnpm exec python3 "${initContextPath}" "${profilePath}"`);

            return NextResponse.json({
                success: true,
                data: profileData
            });
            
        } catch (error) {
            console.error('Error processing dataset:', error);
            return NextResponse.json(
                { error: 'Error processing dataset' },
                { status: 500 }
            );
        }
        
    } catch (error) {
        console.error('Error handling file upload:', error);
        return NextResponse.json(
            { error: 'Error handling file upload' },
            { status: 500 }
        );
    }
}

export async function GET() {
    return NextResponse.json(
        { error: 'Method not allowed' },
        { status: 405 }
    );
}