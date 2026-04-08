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

    def test_no_subcommand_has_no_func(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert not hasattr(args, "func")
