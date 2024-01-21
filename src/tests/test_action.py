from dataclasses import dataclass
from pathlib import Path

from nmk.tests.tester import NmkBaseTester


@dataclass
class FakeCompletedProcess:
    stdout: str


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

    def test_default_remote(self):
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubUser", "--print", "githubRepo"])
        self.check_logs('Config dump: { "githubUser": "dynod", "githubRepo": "nmk-github" }')

    def test_http_remote(self, monkeypatch):
        monkeypatch.setattr("nmk_github.info.run_with_logs", lambda args: FakeCompletedProcess("origin	https://github.com/dynod/nmk-github (fetch)"))
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubUser", "--print", "githubRepo"])
        self.check_logs('Config dump: { "githubUser": "dynod", "githubRepo": "nmk-github" }')

    def test_git_remote(self, monkeypatch):
        monkeypatch.setattr("nmk_github.info.run_with_logs", lambda args: FakeCompletedProcess("origin	git@github.com:dynod/nmk-github.git (fetch)"))
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubUser", "--print", "githubRepo"])
        self.check_logs('Config dump: { "githubUser": "dynod", "githubRepo": "nmk-github" }')

    def test_bad_remote(self, monkeypatch):
        # Fake git remote returned URL
        monkeypatch.setattr("nmk_github.info.run_with_logs", lambda args: FakeCompletedProcess("foo"))
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
            assert '- "3.8"' in build_file
            assert '- "3.11"' not in build_file

    def test_action_with_python(self):
        self.nmk(self.prepare_project("ref_github_python.yml"), extra_args=["gh.actions"])
        assert self.build_file.is_file()
        with self.build_file.open() as f:
            build_file = f.read()
            assert '- "3.8"' in build_file
            assert '- "3.11"' in build_file

    def test_action_with_extra_steps(self):
        self.nmk(self.prepare_project("ref_github_extra_build.yml"), extra_args=["gh.actions"])
        assert self.build_file.is_file()
        with self.build_file.open() as f:
            build_file = f.read()

            # included __if__ step
            assert " name: Some extra step" in build_file
            assert " uses: foo/bar@v1.2.3" in build_file
            assert "__if__:" not in build_file

            # filtered __if__ step
            assert " name: Filtered step" not in build_file

            # __unless__ included step
            assert " name: Another extra step" in build_file
            assert "__unless__:" not in build_file

            # __unless__ filtered step
            assert " name: Another filtered step" not in build_file
