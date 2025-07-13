import subprocess
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

    def setup_remote(self, remote: str):
        # Set test folder as a git repository, and setup remote
        subprocess.run(["git", "init"], cwd=self.test_folder, check=True)
        subprocess.run(["git", "remote", "add", "origin", remote], cwd=self.test_folder, check=True)

    def test_http_remote(self):
        self.setup_remote("https://github.com/foo/bar")
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubUser", "--print", "githubRepo"])
        self.check_logs('Config dump: { "githubUser": "foo", "githubRepo": "bar" }')

    def test_git_remote(self):
        self.setup_remote("git@github.com:bar/foo.git")
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubUser", "--print", "githubRepo"])
        self.check_logs('Config dump: { "githubUser": "bar", "githubRepo": "foo" }')

    def test_bad_remote(self):
        # Fake git remote returned URL
        self.setup_remote("foo")
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
            assert '- "3.9"' in build_file
            assert '- "3.13"' in build_file

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

    def test_unknown_license(self):
        # By default: unknown license
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubLicense"])
        self.check_logs('Config dump: { "githubLicense": "Unknown" }')

    def test_parsed_license(self):
        # Dump a dummy license type
        license_title = "some dummy license"
        license_file = self.test_folder / "LICENSE"
        with license_file.open("w") as f:
            f.write(license_title)
        self.nmk(self.prepare_project("ref_github.yml"), extra_args=["--print", "githubLicense"])
        self.check_logs(f'Config dump: {{ "githubLicense": "{license_title}" }}')
