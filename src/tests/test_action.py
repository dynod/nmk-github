from pathlib import Path

from nmk.tests.tester import NmkBaseTester


class TestGithubPlugin(NmkBaseTester):
    @property
    def templates_root(self) -> Path:
        return Path(__file__).parent / "templates"

    def test_version(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["version"])

    def test_action_no_python(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["gh.actions"])
        build_file = self.test_folder / ".github" / "workflows" / "build.yml"
        assert build_file.is_file()
        with build_file.open() as f:
            assert "# Publish to Pypi" not in f.read()

    def test_action_with_python(self):
        self.nmk(self.prepare_project("ref_github_python.yml"), extra_args=["gh.actions"])
        build_file = self.test_folder / ".github" / "workflows" / "build.yml"
        assert build_file.is_file()
        with build_file.open() as f:
            assert "# Publish to Pypi" in f.read()
