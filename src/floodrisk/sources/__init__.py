"""Source discovery utilities."""

from floodrisk.sources.reliefweb import (
    DEFAULT_RELIEFWEB_APPNAME,
    RELIEFWEB_REPORTS_ENDPOINT,
    ReliefWebDiscoveredReport,
    ReliefWebDiscoveryPlan,
    ReliefWebDiscoveryQuery,
    ReliefWebMetadataDiscoveryResult,
    build_reliefweb_discovery_plan,
    discover_reliefweb_metadata,
    fetch_reliefweb_query_metadata,
    load_reliefweb_discovery_queries,
    normalize_reliefweb_report,
    render_reliefweb_discovery_plan_report,
    render_reliefweb_metadata_discovery_report,
    write_reliefweb_discovery_plan_report,
    write_reliefweb_metadata_discovery_outputs,
)

__all__ = [
    "DEFAULT_RELIEFWEB_APPNAME",
    "RELIEFWEB_REPORTS_ENDPOINT",
    "ReliefWebDiscoveryPlan",
    "ReliefWebDiscoveryQuery",
    "build_reliefweb_discovery_plan",
    "load_reliefweb_discovery_queries",
    "render_reliefweb_discovery_plan_report",
    "write_reliefweb_discovery_plan_report",
    "ReliefWebDiscoveredReport",
    "ReliefWebMetadataDiscoveryResult",
    "discover_reliefweb_metadata",
    "fetch_reliefweb_query_metadata",
    "normalize_reliefweb_report",
    "render_reliefweb_metadata_discovery_report",
    "write_reliefweb_metadata_discovery_outputs",
]
