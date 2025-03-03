from typing import Dict, Any

def create_api_template() -> str:
    """Returns the base API route template"""
    return '''
import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

{%- if method_imports %}
{{ method_imports }}
{%- endif %}

{%- for method in methods %}
export async function {{ method }}({% if method_params %}{{ method_params }}{% endif %}) {
  try {
    {%- if method == 'GET' %}
    const filePath = path.join(process.cwd(), {{ file_path }});
    const fileContents = await fs.readFile(filePath, 'utf8');
    return new NextResponse(fileContents, {
      headers: {
        'Content-Type': {{ content_type|default("'text/plain'") }},
      },
    });
    {%- elif method == 'POST' %}
    const data = await request.json();
    // Process the data here
    return new NextResponse(JSON.stringify({ success: true }), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    {%- elif method == 'PUT' %}
    const data = await request.json();
    // Update the data here
    return new NextResponse(JSON.stringify({ success: true }), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    {%- elif method == 'DELETE' %}
    // Delete the resource here
    return new NextResponse(JSON.stringify({ success: true }), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    {%- endif %}
  } catch (error) {
    console.error('Error in {{ method }} request:', error);
    return new NextResponse('Error processing request', { status: 500 });
  }
}
{%- endfor %}
'''

def generate_api_route(config: Dict[str, Any]) -> str:
    """Generate an API route based on configuration"""
    from jinja2 import Template
    template = Template(create_api_template())
    return template.render(**config)

def example_usage():
    """Example of how to use the template generator"""
    config = {
        'methods': ['GET'],
        'file_path': "'codegen/app/sample_data.csv'",
        'content_type': "'text/csv'",
        'method_imports': '',
        'method_params': ''
    }
    return generate_api_route(config)

if __name__ == "__main__":
    print(example_usage())
