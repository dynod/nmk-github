from pathlib import Path

from nmk_base._buildenv.template import NmkBaseProjectTemplate, NmkReference


class NmkGithubProjectTemplate(NmkBaseProjectTemplate):
    """
    Template for **nmk-github** plugin project
    """

    @property
    def weight(self) -> int:
        # Not a main template
        return 0

    @property
    def auto_extra(self) -> bool:
        # Default extra
        return True

    @property
    def references(self) -> list[NmkReference]:
        return super().references + [NmkReference("nmk-github!plugin.yml", ["nmk-base!plugin.yml"])]

    @property
    def description(self) -> str:
        return "add Github support, including actions file generation"

    @property
    def generated_files(self) -> set[Path]:
        github_path = Path(".github") / "workflows"
        return super().generated_files | set(
            [
                github_path / "build.yml",
            ]
        )

    @property
    def post_generation_tasks(self) -> list[str]:
        return super().post_generation_tasks + ["gh.actions"]
