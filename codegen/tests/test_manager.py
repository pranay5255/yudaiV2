from codegen.agents.manager import ManagerAgent


def test_manager_pattern(tmp_path):
    csv_path = tmp_path / 'data.csv'
    csv_path.write_text('a,b\n1,2\n3,4')
    manager = ManagerAgent()
    result = manager.handle(str(csv_path), 'Generate dashboard', {'goal': 'demo'})
    assert result.endswith('.zip') or result.startswith('http')
