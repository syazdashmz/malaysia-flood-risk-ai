"""Feature table generation plan for future model training."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from floodrisk.ml.training_schema import TRAINING_TABLE_COLUMNS


@dataclass(frozen=True)
class FeatureTablePlanItem:
    """Planned source and derivation for one training table column."""

    column: str
    dtype: str
    role: str
    source_category: str
    planned_source: str
    derivation_note: str
    ready_now: bool

    def as_dict(self) -> dict[str, str | bool]:
        """Return plan item as a dictionary."""

        return asdict(self)


COLUMN_SOURCE_PLAN = {
    "observation_id": (
        "generated",
        "feature table builder",
        "Create stable unique ID from location and observation date.",
        False,
    ),
    "latitude": (
        "sample/geospatial",
        "sample locations or geocoded observations",
        "Use validated Malaysia latitude.",
        True,
    ),
    "longitude": (
        "sample/geospatial",
        "sample locations or geocoded observations",
        "Use validated Malaysia longitude.",
        True,
    ),
    "observation_date": (
        "temporal",
        "future observation/event table",
        "Attach date for time-aware split and weather joins.",
        False,
    ),
    "state": (
        "geospatial",
        "future administrative boundary file",
        "Derive by point-in-polygon lookup after boundary data is verified.",
        False,
    ),
    "district": (
        "geospatial",
        "future administrative boundary file",
        "Derive by point-in-polygon lookup after district data is verified.",
        False,
    ),
    "elevation_m": (
        "terrain",
        "current sample data or future DEM source",
        "Use sample value now; replace with DEM-derived value later.",
        True,
    ),
    "slope_deg": (
        "terrain",
        "current sample data or future DEM source",
        "Use sample value now; replace with DEM-derived slope later.",
        True,
    ),
    "river_distance_m": (
        "hydrology/geospatial",
        "current sample data or future river network",
        "Use sample value now; replace with nearest-river calculation later.",
        True,
    ),
    "historical_flood_distance_m": (
        "historical/geospatial",
        "current sample data or future historical flood polygons",
        "Use sample value now; replace with historical flood proximity later.",
        True,
    ),
    "rainfall_24h_mm": (
        "weather",
        "weather pipeline or future rainfall history",
        "Aggregate rainfall over previous 24 hours.",
        False,
    ),
    "rainfall_72h_mm": (
        "weather",
        "weather pipeline or future rainfall history",
        "Aggregate rainfall over previous 72 hours.",
        False,
    ),
    "water_level_status": (
        "hydrology",
        "future river/water-level source",
        "Join hydrology status by station, basin, or nearest valid proxy.",
        False,
    ),
    "weather_warning_status": (
        "weather",
        "weather warning pipeline",
        "Map warning text or category into normalized warning status.",
        True,
    ),
    "land_cover_class": (
        "exposure/geospatial",
        "current sample data or future land-cover raster/vector",
        "Use sample value now; replace with verified land-cover lookup later.",
        True,
    ),
    "population_density_per_km2": (
        "exposure",
        "current sample data or future population raster/table",
        "Use sample value now; replace with verified population density source.",
        True,
    ),
    "flood_occurred": (
        "target",
        "future verified historical flood label source",
        (
            "Preferred binary target label from a verified historical flood source. "
            "Must not come from rule-based risk score."
        ),
        False,
    ),
}


def build_feature_table_plan() -> list[FeatureTablePlanItem]:
    """Build planned source map for training table columns."""

    plan_items: list[FeatureTablePlanItem] = []

    for column in TRAINING_TABLE_COLUMNS:
        source_category, planned_source, derivation_note, ready_now = COLUMN_SOURCE_PLAN[
            column.name
        ]

        plan_items.append(
            FeatureTablePlanItem(
                column=column.name,
                dtype=column.dtype,
                role=column.role,
                source_category=source_category,
                planned_source=planned_source,
                derivation_note=derivation_note,
                ready_now=ready_now,
            )
        )

    return plan_items


def render_feature_table_plan_report(plan_items: list[FeatureTablePlanItem]) -> str:
    """Render feature table generation plan as Markdown."""

    ready_count = sum(1 for item in plan_items if item.ready_now)
    missing_count = len(plan_items) - ready_count
    target_items = [item for item in plan_items if item.role == "target"]
    target_ready = all(item.ready_now for item in target_items)

    lines = [
        "# Feature Table Generation Plan",
        "",
        "## Summary",
        "",
        f"- Planned columns: {len(plan_items)}",
        f"- Columns with usable current source/proxy: {ready_count}",
        f"- Columns still requiring future data work: {missing_count}",
        f"- Target label ready: {target_ready}",
        f"- Real ML training allowed now: {target_ready}",
        "",
        "## Planned Columns",
        "",
        "| Column | Type | Role | Source Category | Ready Now | Planned Source | Derivation Note |",
        "|---|---|---|---|---:|---|---|",
    ]

    for item in plan_items:
        lines.append(
            "| "
            f"{item.column} | "
            f"{item.dtype} | "
            f"{item.role} | "
            f"{item.source_category} | "
            f"{item.ready_now} | "
            f"{item.planned_source} | "
            f"{item.derivation_note} |"
        )

    lines.extend(
        [
            "",
            "## Training Guardrail",
            "",
            (
                "Do not create a real model-training table until the target label "
                "`flood_occurred` comes from a verified historical flood source."
            ),
            "",
            "The rule-based risk score may be used for demos or weak-supervision "
            "experiments only if clearly labeled as proxy or synthetic.",
            "",
            "## Next Practical Step",
            "",
            (
                "Create a feature-table builder skeleton that can inspect available "
                "sample columns, but refuses to mark output as training-ready when "
                "the verified target label is unavailable."
            ),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_feature_table_plan_report(
    plan_items: list[FeatureTablePlanItem],
    output_path: Path,
) -> Path:
    """Write feature table generation plan report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_feature_table_plan_report(plan_items),
        encoding="utf-8",
    )
    return output_path
