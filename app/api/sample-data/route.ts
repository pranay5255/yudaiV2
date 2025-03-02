import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

export async function GET() {
  try {
    const filePath = path.join(process.cwd(), 'codegen', 'app', 'sample_data.csv');
    const fileContents = await fs.readFile(filePath, 'utf8');
    return new NextResponse(fileContents, {
      headers: {
        'Content-Type': 'text/csv',
      },
    });
  } catch {
    return new NextResponse('Error reading file', { status: 500 });
  }
} 