from pathlib import Path
import sys, os
sys.path.insert(0, os.path.abspath(Path(__file__).resolve().parents[3]))
from codegen.scaffolder import render_template

def test_layout_template_snapshot():
    context = {"title": "Test", "description": "Desc"}
    rendered = render_template("_layout.tsx.j2", context)
    snapshot = (Path(__file__).parent / "layout_snapshot.tsx").read_text()
    assert rendered.strip() == snapshot.strip()

def test_scatter_template_snapshot():
    context = {"x": "a", "y": "b", "category": "c", "name": "MyScatter"}
    rendered = render_template("ScatterChart.tsx.j2", context)
    snapshot = (Path(__file__).parent / "scatter_snapshot.tsx").read_text()
    assert rendered.strip() == snapshot.strip()

def test_api_route_snapshot():
    rendered = render_template("api_route.ts.j2", {})
    snapshot = (Path(__file__).parent / "api_route_snapshot.ts").read_text()
    assert rendered.strip() == snapshot.strip()
