from typer.testing import CliRunner

from app.cli import app


def test_cli_version_ok():
    runner = CliRunner()
    res = runner.invoke(app, ["version"])
    assert res.exit_code == 0
    assert "cc " in res.stdout


def test_cli_check_json_ok():
    runner = CliRunner()
    res = runner.invoke(app, ["check", "--json"])
    assert res.exit_code == 0
    assert res.stdout.strip().startswith("{") and res.stdout.strip().endswith("}")

