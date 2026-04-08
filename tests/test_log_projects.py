from datetime import datetime, timezone, timedelta
from pmanage.commands import log, projects, start, stop
from tests.conftest import make_args


class TestLog:
    def test_log_no_entries(self, tmp_db, capsys):
        log.run(make_args(project=None, days=7))
        output = capsys.readouterr().out
        assert "No entries found" in output

    def test_log_shows_completed_entry(self, tmp_db, capsys):
        start.run(make_args(project="proj", note=""))
        stop.run(make_args(note=""))
        capsys.readouterr()

        log.run(make_args(project=None, days=7))
        output = capsys.readouterr().out
        assert "proj" in output
        assert "Total:" in output

    def test_log_shows_running_entry(self, tmp_db, capsys):
        start.run(make_args(project="proj", note=""))
        capsys.readouterr()

        log.run(make_args(project=None, days=7))
        output = capsys.readouterr().out
        assert "running" in output

    def test_log_filters_by_project(self, tmp_db, capsys):
        # Create two completed entries for different projects
        start.run(make_args(project="alpha", note=""))
        stop.run(make_args(note=""))
        start.run(make_args(project="beta", note=""))
        stop.run(make_args(note=""))
        capsys.readouterr()

        log.run(make_args(project="alpha", days=7))
        output = capsys.readouterr().out
        assert "alpha" in output
        assert "beta" not in output

    def test_log_shows_notes(self, tmp_db, capsys):
        start.run(make_args(project="proj", note="important work"))
        stop.run(make_args(note=""))
        capsys.readouterr()

        log.run(make_args(project=None, days=7))
        output = capsys.readouterr().out
        assert "important work" in output


class TestProjects:
    def test_projects_no_entries(self, tmp_db, capsys):
        projects.run(make_args())
        output = capsys.readouterr().out
        assert "No projects logged yet." in output

    def test_projects_lists_projects(self, tmp_db, capsys):
        start.run(make_args(project="alpha", note=""))
        stop.run(make_args(note=""))
        start.run(make_args(project="beta", note=""))
        stop.run(make_args(note=""))
        capsys.readouterr()

        projects.run(make_args())
        output = capsys.readouterr().out
        assert "alpha" in output
        assert "beta" in output
        assert "Sessions" in output
