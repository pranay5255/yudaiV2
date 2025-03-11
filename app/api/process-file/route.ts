import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import { join } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { File } from 'buffer';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as string;
        console.log(file);
        
        if (!file) {
            return NextResponse.json(
                { error: 'No file provided' },
                { status: 400 }
            );
        }

        let filePath: string;

        // Check if we're using the sample data
        if (file === 'sample_data.csv') {
            filePath = join(process.cwd(), 'codegen', 'app', 'sample_data.csv');
        } else {
            // Handle uploaded file
            const uploadedFile = formData.get('file') as unknown as File;
            const uploadPath = join(process.cwd(), 'codegen', 'app', 'data', 'uploads', uploadedFile.name);
            const bytes = await uploadedFile.arrayBuffer();
            const buffer = Buffer.from(bytes);
            await writeFile(uploadPath, buffer);
            filePath = uploadPath;
        }

        try {
            // Execute the Python script
            const scriptPath = join(process.cwd(), 'codegen/app/base_eda.py');
            const { stdout } = await execAsync(`python3 "${scriptPath}" "${filePath}"`);
            
            // Parse and return the results
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