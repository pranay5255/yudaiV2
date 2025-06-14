from fastapi.testclient import TestClient
from pathlib import Path
import sys, os
sys.path.insert(0, os.path.abspath(Path(__file__).resolve().parents[1]))
import subprocess
import pandas as pd
from sklearn.datasets import load_iris

from codegen.api.chat import app

client = TestClient(app)

def create_iris_csv(path: Path):
    data = load_iris(as_frame=True).frame
    data.columns = [c.replace(" (cm)", "_cm").replace(" ", "_") for c in data.columns]
    data.to_csv(path, index=False)


def test_generate_scatter_project(tmp_path):
    csv_path = tmp_path / "iris.csv"
    create_iris_csv(csv_path)

    spec = {
        "project_name": "iris_dash",
        "layout": {"title": "Iris", "description": "Iris dataset"},
        "charts": [
            {"type": "scatter", "name": "ScatterChart", "x": "sepal_length_cm", "y": "sepal_width_cm", "category": "target"}
        ],
    }

    resp = client.post("/generate", json={"spec": spec})
    assert resp.status_code == 200
    project_dir = Path(resp.json()["path"])
    assert (project_dir / "app" / "components" / "ScatterChart.tsx").exists()
    subprocess.run(["pnpm", "install"], cwd=project_dir, capture_output=True)
    result = subprocess.run(["pnpm", "build"], cwd=project_dir, capture_output=True)
    assert result.returncode == 0
