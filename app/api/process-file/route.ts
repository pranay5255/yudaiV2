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
        
        if (!file) {
            return NextResponse.json(
                { error: 'No file provided' },
                { status: 400 }
            );
        }

        // Save the uploaded file
        const uploadPath = join(process.cwd(), 'data', 'uploads', file.name);
        const bytes = await file.arrayBuffer();
        const buffer = Buffer.from(bytes);
        await writeFile(uploadPath, buffer);

        try {
            // Execute the Python script which will create output in data/tmp
            const scriptPath = join(process.cwd(), 'codegen/app/base_eda.py');
            const { stdout } = await execAsync(`python3 "${scriptPath}" "${uploadPath}"`);
            
            // base_eda.py outputs the results to stdout as JSON
            const results = JSON.parse(stdout);

            return NextResponse.json(results);
            
        } catch (error) {
            throw error;
        }
        
    } catch (error) {
        console.error('Error processing file:', error);
        return NextResponse.json(
            { error: 'Error processing file' },
            { status: 500 }
        );
    }
}