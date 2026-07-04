import pytest
from buildenv.__main__ import buildenv
from pytest_multilog import TestHelper


class TestTemplate(TestHelper):
    def test_template(self, monkeypatch: pytest.MonkeyPatch):
        # Fake a "no CI" environment
        monkeypatch.delenv("CI", raising=False)

        # Prepare a project with uvx backend
        assert (
            buildenv(
                [
                    "install",
                    "--template",
                    "nmk.python",
                    "--extra-template",
                    "nmk.github",
                    "-p",
                    str(self.test_folder),
                ]
            )
            == 0
        )

        # Check github actions file is generated
        assert (self.test_folder / ".github" / "workflows" / "build.yml").is_file()
