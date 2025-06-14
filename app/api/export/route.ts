import { NextRequest } from 'next/server';
import archiver from 'archiver';
import { Readable } from 'stream';

export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const id = url.searchParams.get('id') || '0';

  const archive = archiver('zip', { zlib: { level: 9 } });

  const stream = new Readable({
    read() {}
  });

  const fileContent = `Config for dashboard ${id}`;
  archive.append(fileContent, { name: 'config.txt' });
  archive.finalize();

  archive.on('data', (data) => stream.push(data));
  archive.on('end', () => stream.push(null));

  return new Response(Readable.toWeb(stream) as unknown as ReadableStream, {
    headers: {
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="dashboard_${id}.zip"`,
    },
  });
}
