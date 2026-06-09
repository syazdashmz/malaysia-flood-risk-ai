"""Planned geospatial artifact checks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class GeospatialArtifact:
    """Expected local geospatial artifact."""

    dataset_id: str
    relative_path: str
    required_for_mvp: bool
    description: str

    def as_dict(self) -> dict[str, str | bool]:
        """Return artifact metadata as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class GeospatialArtifactCheck:
    """Existence check for one planned geospatial artifact."""

    artifact: GeospatialArtifact
    exists: bool

    @property
    def status(self) -> str:
        """Return current artifact status."""

        return "available" if self.exists else "planned_missing"

    def as_dict(self) -> dict[str, str | bool | dict[str, str | bool]]:
        """Return check result as a dictionary."""

        return {
            "artifact": self.artifact.as_dict(),
            "exists": self.exists,
            "status": self.status,
        }


GEOSPATIAL_ARTIFACTS = [
    GeospatialArtifact(
        dataset_id="malaysia_admin_boundary",
        relative_path="data/external/geospatial/malaysia_admin_boundary.geojson",
        required_for_mvp=False,
        description=("Country-level or combined administrative boundary polygons for Malaysia."),
    ),
    GeospatialArtifact(
        dataset_id="malaysia_state_boundary",
        relative_path="data/external/geospatial/malaysia_state_boundary.geojson",
        required_for_mvp=False,
        description="State-level administrative boundary polygons for Malaysia.",
    ),
    GeospatialArtifact(
        dataset_id="malaysia_district_boundary",
        relative_path="data/external/geospatial/malaysia_district_boundary.geojson",
        required_for_mvp=False,
        description="District-level administrative boundary polygons for Malaysia.",
    ),
]


def list_geospatial_artifacts() -> list[GeospatialArtifact]:
    """Return planned geospatial artifacts."""

    return GEOSPATIAL_ARTIFACTS.copy()


def check_geospatial_artifacts(project_root: Path) -> list[GeospatialArtifactCheck]:
    """Check whether planned geospatial artifacts exist locally."""

    return [
        GeospatialArtifactCheck(
            artifact=artifact,
            exists=(project_root / artifact.relative_path).exists(),
        )
        for artifact in GEOSPATIAL_ARTIFACTS
    ]


def render_geospatial_artifact_report(
    checks: list[GeospatialArtifactCheck],
) -> str:
    """Render geospatial artifact checks as Markdown."""

    lines = [
        "# Geospatial Artifact Plan",
        "",
        "## Purpose",
        "",
        (
            "This report tracks expected local geospatial boundary artifacts "
            "for the v0.3.0 geospatial foundation milestone."
        ),
        "",
        "No boundary file is bundled until source reliability, licensing, and "
        "redistribution rules are verified.",
        "",
        "## Planned Artifacts",
        "",
        "| Dataset ID | Path | Required for MVP | Status |",
        "|---|---|---:|---|",
    ]

    for check in checks:
        artifact = check.artifact
        lines.append(
            "| "
            f"{artifact.dataset_id} | "
            f"{artifact.relative_path} | "
            f"{artifact.required_for_mvp} | "
            f"{check.status} |"
        )

    lines.extend(
        [
            "",
            "## Next Actions",
            "",
            "1. Verify authoritative boundary data sources.",
            "2. Confirm license and redistribution permissions.",
            "3. Download data manually only after verification.",
            "4. Store raw external files under data/external/geospatial/.",
            "5. Add geometry loading and validation checks.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_geospatial_artifact_report(
    checks: list[GeospatialArtifactCheck],
    output_path: Path,
) -> Path:
    """Write geospatial artifact report to Markdown."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_geospatial_artifact_report(checks),
        encoding="utf-8",
    )
    return output_path
