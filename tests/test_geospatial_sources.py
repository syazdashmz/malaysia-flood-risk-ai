from floodrisk.geospatial.sources import (
    get_geospatial_data_source,
    list_geospatial_data_source_dicts,
    list_geospatial_data_sources,
)


def test_list_geospatial_data_sources_returns_planned_sources():
    sources = list_geospatial_data_sources()

    assert len(sources) >= 3
    assert sources[0].dataset_id == "malaysia_admin_boundary"


def test_get_geospatial_data_source_returns_matching_source():
    source = get_geospatial_data_source("malaysia_state_boundary")

    assert source.name == "Malaysia State Boundary"
    assert source.status == "planned"


def test_get_geospatial_data_source_rejects_unknown_id():
    try:
        get_geospatial_data_source("unknown")
    except KeyError as exc:
        assert "Unknown geospatial dataset id" in str(exc)
    else:
        raise AssertionError("Expected KeyError for unknown dataset id")


def test_list_geospatial_data_source_dicts_is_serializable():
    sources = list_geospatial_data_source_dicts()

    assert isinstance(sources[0], dict)
    assert "dataset_id" in sources[0]
    assert "license_note" in sources[0]
