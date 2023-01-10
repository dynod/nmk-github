from pathlib import Path

from nmk.tests.tester import NmkBaseTester


class TestGithubPlugin(NmkBaseTester):
    @property
    def templates_root(self) -> Path:
        return Path(__file__).parent / "templates"

    @property
    def build_file(self) -> Path:
        return self.test_folder / ".github" / "workflows" / "build.yml"

    def test_version(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["version"])

    def test_action_no_python_version(self):
        self.nmk(self.prepare_project("ref_github_no_version.yml"), extra_args=["gh.actions"])
        assert not self.build_file.is_file()

    def test_action_no_python(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["gh.actions"])
        assert self.build_file.is_file()
        with self.build_file.open() as f:
            assert "# Publish to Pypi" not in f.read()

    def test_action_with_python(self):
        self.nmk(self.prepare_project("ref_github_python.yml"), extra_args=["gh.actions"])
        assert self.build_file.is_file()
        with self.build_file.open() as f:
            assert "# Publish to Pypi" in f.read()
