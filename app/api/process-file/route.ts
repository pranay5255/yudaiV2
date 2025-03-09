import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import { join } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as File;
        let tempFilePath: string;
        
        if (!file) {
            // Use sample data if no file uploaded
            tempFilePath = join(process.cwd(), 'codegen', 'app', 'sample_data.csv');
        } else {
            // Create a temporary file path
            const bytes = await file.arrayBuffer();
            const buffer = Buffer.from(bytes);
            
            // Save the file temporarily
            tempFilePath = join(process.cwd(), 'tmp', file.name);
            await writeFile(tempFilePath, buffer);
        }

        // Execute the Python script
        const scriptPath = join(process.cwd(), 'codegen/app/base_eda.py');
        const command = `python3 "${scriptPath}" "${tempFilePath}"`;
        
        const { stdout } = await execAsync(command);
        const results = JSON.parse(stdout);

        // Clean up the temporary file if it was uploaded
        if (file) {
            await execAsync(`rm "${tempFilePath}"`);
        }

        return NextResponse.json(results);
        
    } catch (error) {
        console.error('Error processing file:', error);
        return NextResponse.json(
            { error: 'Error processing file' },
            { status: 500 }
        );
    }
}