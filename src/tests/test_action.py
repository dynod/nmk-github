from pathlib import Path

from nmk.tests.tester import NmkBaseTester


class TestGithubPlugin(NmkBaseTester):
    @property
    def templates_root(self) -> Path:
        return Path(__file__).parent / "templates"

    def test_version(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["version"])

    def test_action(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["gh.actions"])
        assert (self.test_folder / ".github" / "workflows" / "build.yml").is_file()
