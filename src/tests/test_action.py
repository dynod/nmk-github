from dataclasses import dataclass
from pathlib import Path

import nmk.utils as nmk_utils
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

    def test_label(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubIssuesLabelSuffix"])
        self.check_logs('Config dump: { "githubIssuesLabelSuffix": "+label%3Afoo%3Abar" }')

    def test_user(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubUser"])
        self.check_logs('Config dump: { "githubUser": "dynod" }')

    def test_repo(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubRepo"])
        self.check_logs('Config dump: { "githubRepo": "nmk-github" }')

    def test_fake_git_remote(self, monkeypatch):
        @dataclass
        class FakeCompletedProcess:
            stdout: str

        # Fake git remote returned URL
        monkeypatch.setattr(nmk_utils, "run_with_logs", lambda args: FakeCompletedProcess("foo"))
        self.nmk(
            self.prepare_project("ref_github.yml"),
            extra_args=["--print", "githubRepo"],
            expected_rc=1,
            expected_error="Error occurred while resolving config githubRepo: Failed to parse git fetch remote URL",
        )

    def test_action_no_python_version(self):
        self.nmk(self.prepare_project("ref_github_no_version.yml"), extra_args=["gh.actions"])
        assert not self.build_file.is_file()

    def test_action_no_python(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["gh.actions"])
        assert self.build_file.is_file()
        with self.build_file.open() as f:
            build_file = f.read()
            assert "# Publish to Pypi" not in build_file
            assert "# Upload coverage" not in build_file

    def test_action_with_python(self):
        self.nmk(self.prepare_project("ref_github_python.yml"), extra_args=["gh.actions"])
        assert self.build_file.is_file()
        with self.build_file.open() as f:
            build_file = f.read()
            assert "# Publish to Pypi" in build_file
            assert "# Upload coverage" in build_file
