from pmanage.commands import start, stop, status
from tests.conftest import make_args


class TestStart:
    def test_start_creates_entry(self, tmp_db, capsys):
        args = make_args(project="testproj", note="")
        start.run(args)
        output = capsys.readouterr().out
        assert "Started tracking time for project 'testproj'" in output

        with tmp_db() as conn:
            row = conn.execute("SELECT * FROM entries").fetchone()
            assert row["project"] == "testproj"
            assert row["ended_at"] is None

    def test_start_with_note(self, tmp_db, capsys):
        args = make_args(project="proj", note="my note")
        start.run(args)

        with tmp_db() as conn:
            row = conn.execute("SELECT * FROM entries").fetchone()
            assert row["note"] == "my note"

    def test_start_blocks_when_timer_running(self, tmp_db, capsys):
        start.run(make_args(project="proj1", note=""))
        capsys.readouterr()

        start.run(make_args(project="proj2", note=""))
        output = capsys.readouterr().out
        assert "Timer already running" in output
        assert "proj1" in output

        with tmp_db() as conn:
            count = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
            assert count == 1


class TestStop:
    def test_stop_no_timer(self, tmp_db, capsys):
        stop.run(make_args(note=""))
        output = capsys.readouterr().out
        assert "No timer running." in output

    def test_stop_running_timer(self, tmp_db, capsys):
        start.run(make_args(project="proj", note=""))
        capsys.readouterr()

        stop.run(make_args(note=""))
        output = capsys.readouterr().out
        assert "Stopped 'proj'" in output
        assert "logged" in output

        with tmp_db() as conn:
            row = conn.execute("SELECT * FROM entries").fetchone()
            assert row["ended_at"] is not None

    def test_stop_with_note_updates(self, tmp_db, capsys):
        start.run(make_args(project="proj", note="original"))
        capsys.readouterr()

        stop.run(make_args(note="updated"))
        with tmp_db() as conn:
            row = conn.execute("SELECT * FROM entries").fetchone()
            assert row["note"] == "updated"

    def test_stop_without_note_preserves_original(self, tmp_db, capsys):
        start.run(make_args(project="proj", note="keep me"))
        capsys.readouterr()

        stop.run(make_args(note=""))
        with tmp_db() as conn:
            row = conn.execute("SELECT * FROM entries").fetchone()
            assert row["note"] == "keep me"


class TestStatus:
    def test_status_no_timer(self, tmp_db, capsys):
        status.run(make_args())
        output = capsys.readouterr().out
        assert "No timer running." in output

    def test_status_running_timer(self, tmp_db, capsys):
        start.run(make_args(project="proj", note=""))
        capsys.readouterr()

        status.run(make_args())
        output = capsys.readouterr().out
        assert "Running: 'proj'" in output

    def test_status_shows_note(self, tmp_db, capsys):
        start.run(make_args(project="proj", note="doing stuff"))
        capsys.readouterr()

        status.run(make_args())
        output = capsys.readouterr().out
        assert "doing stuff" in output
