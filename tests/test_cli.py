from pmanage.cli import build_parser


class TestBuildParser:
    def test_parser_has_subcommands(self):
        parser = build_parser()
        # Should not raise
        args = parser.parse_args(["start", "myproject"])
        assert args.project == "myproject"
        assert hasattr(args, "func")

    def test_start_with_note(self):
        parser = build_parser()
        args = parser.parse_args(["start", "proj", "--note", "hello"])
        assert args.project == "proj"
        assert args.note == "hello"

    def test_stop_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["stop"])
        assert args.note == ""
        assert hasattr(args, "func")

    def test_log_project_filter(self):
        parser = build_parser()
        args = parser.parse_args(["log", "-p", "myproj"])
        assert args.project == "myproj"

    def test_log_days_filter(self):
        parser = build_parser()
        args = parser.parse_args(["log", "-d", "30"])
        assert args.days == 30

    def test_add_entry(self):
        parser = build_parser()
        args = parser.parse_args(["add", "proj", "09:00", "17:00", "--note", "work"])
        assert args.project == "proj"
        assert args.start_time == "09:00"
        assert args.end_time == "17:00"
        assert args.note == "work"

    def test_delete_entry(self):
        parser = build_parser()
        args = parser.parse_args(["delete", "42"])
        assert args.id == 42

    def test_edit_entry(self):
        parser = build_parser()
        args = parser.parse_args(["edit", "42", "--project", "newproj", "--start-time", "10:00", "--end-time", "18:00", "--note", "updated"])
        assert args.id == 42
        assert args.project == "newproj"
        assert args.start_time == "10:00"
        assert args.end_time == "18:00"
        assert args.note == "updated"

    def test_no_subcommand_has_no_func(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert not hasattr(args, "func")
