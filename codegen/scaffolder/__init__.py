from pathlib import Path
from typing import Dict, Any
import shutil
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "tasksv1" / "templates"

env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

def render_template(name: str, context: Dict[str, Any]) -> str:
    template = env.get_template(name)
    return template.render(**context)

def generate_project(spec: Dict[str, Any], base_dir: Path) -> Path:
    project_dir = base_dir / spec.get("project_name", "dashboard")
    app_dir = project_dir / "app"
    components_dir = app_dir / "components"
    api_dir = app_dir / "api" / "sample"

    components_dir.mkdir(parents=True, exist_ok=True)
    api_dir.mkdir(parents=True, exist_ok=True)

    # layout
    layout_content = render_template("_layout.tsx.j2", spec.get("layout", {}))
    (app_dir / "layout.tsx").write_text(layout_content)
    page_content = render_template("page.tsx.j2", {})
    (app_dir / "page.tsx").write_text(page_content)

    # chart components
    for chart in spec.get("charts", []):
        if chart.get("type") == "scatter":
            chart_content = render_template("ScatterChart.tsx.j2", chart)
            (components_dir / f"{chart.get('name','ScatterChart')}.tsx").write_text(chart_content)

    # api route sample
    api_content = render_template("api_route.ts.j2", {})
    (api_dir / "route.ts").write_text(api_content)

    # copy configuration files for standalone build
    root = Path(__file__).resolve().parents[2]
    for fname in ["package.json", "tsconfig.json", "pnpm-lock.yaml"]:
        shutil.copy(root / fname, project_dir / fname)

    # create Next.js config that disables lint and type checks
    config_content = """import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: true },
};

export default nextConfig;
"""
    (project_dir / "next.config.ts").write_text(config_content)

    # minimal globals.css
    (app_dir / "globals.css").write_text("body{font-family:sans-serif;}")

    return project_dir
