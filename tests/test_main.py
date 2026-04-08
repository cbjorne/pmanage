from unittest.mock import patch
from pmanage.main import main


class TestMain:
    def test_no_args_prints_help(self, tmp_db, capsys):
        with patch("sys.argv", ["pmanage"]):
            main()
        output = capsys.readouterr().out
        assert "usage:" in output.lower() or "pmanage" in output

    def test_start_via_main(self, tmp_db, capsys):
        with patch("sys.argv", ["pmanage", "start", "myproj"]):
            main()
        output = capsys.readouterr().out
        assert "Started tracking" in output
