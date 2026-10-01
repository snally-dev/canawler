"""Public source and artifact provenance."""

from __future__ import annotations

from typing import Any

from canawler.dataset import (
    ACCESS_SOURCE_ID,
    AQUEDUCT_MILE_SOURCE_ID,
    AQUEDUCT_SOURCE_ID,
    CAMPSITE_SOURCE_ID,
    NPS_LOCK_SOURCE_ID,
    RECREATION_SOURCE_ID,
    TOWPATH_SOURCE_ID,
    TRUST_LOCK_SOURCE_ID,
    load_access_points,
    load_aqueducts,
    load_campsites,
    load_locks,
    load_recreation_guide,
)
from canawler.reference import FEATURESERVER_URL, ReferenceDataError

SOURCE_SCHEMA_VERSION = 2
SOURCE_CHECKED_AT = "2026-10-01"


def build_sources() -> dict[str, Any]:
    access = load_access_points()["source"]
    recreation = load_recreation_guide()["source"]
    campsite = load_campsites()["source"]
    aqueduct_sources = load_aqueducts()["sources"]
    lock_sources = load_locks()["sources"]
    lock_by_role = {source["role"]: source for source in lock_sources}
    try:
        nps_locks = lock_by_role["Lift-lock count and numbering authority"]
        trust_locks = lock_by_role["Primary practical lock mileposts and common names"]
    except KeyError as error:
        raise ReferenceDataError(
            "lock source roles do not match the expected schema"
        ) from error
    aqueduct_by_role = {source["role"]: source for source in aqueduct_sources}
    try:
        guide_aqueducts = aqueduct_by_role["Historical aqueduct construction table"]
        trust_aqueducts = aqueduct_by_role["Aqueduct names and mileposts"]
    except KeyError as error:
        raise ReferenceDataError(
            "aqueduct source roles do not match the expected schema"
        ) from error

    sources = sorted(
        [
            {
                "id": AQUEDUCT_MILE_SOURCE_ID,
                "name": trust_aqueducts["name"],
                "organization": "C&O Canal Trust",
                "url": trust_aqueducts["url"],
                "description": "Normalized aqueduct names and reference mileposts.",
                "published_at": None,
                "retrieved_at": None,
                "checked_at": SOURCE_CHECKED_AT,
            },
            {
                "id": AQUEDUCT_SOURCE_ID,
                "name": guide_aqueducts["name"],
                "organization": "Schreiber Publishing",
                "url": guide_aqueducts["url"],
                "description": (
                    "Historical guidebook aqueduct dimensions and masonry details, "
                    "transcribed from user-supplied page photographs."
                ),
                "published_at": None,
                "retrieved_at": "2026-09-30",
                "checked_at": SOURCE_CHECKED_AT,
            },
            {
                "id": CAMPSITE_SOURCE_ID,
                "name": campsite["name"],
                "organization": "National Park Service",
                "url": campsite["url"],
                "description": (
                    "Current official campground types and mileposts, approved "
                    f"{campsite['approved']}."
                ),
                "published_at": campsite["approved"],
                "retrieved_at": None,
                "checked_at": SOURCE_CHECKED_AT,
            },
            {
                "id": ACCESS_SOURCE_ID,
                "name": access["name"],
                "organization": "C&O Canal Association",
                "url": access["url"],
                "description": "Access-point names, mile ranges, and coordinates.",
                "published_at": None,
                "retrieved_at": None,
                "checked_at": SOURCE_CHECKED_AT,
            },
            {
                "id": RECREATION_SOURCE_ID,
                "name": recreation["name"],
                "organization": "National Park Service",
                "url": recreation["url"],
                "description": "Recreation locations and listed visitor amenities.",
                "published_at": None,
                "retrieved_at": None,
                "checked_at": SOURCE_CHECKED_AT,
            },
            {
                "id": NPS_LOCK_SOURCE_ID,
                "name": "National Park Service Lift Locks",
                "organization": "National Park Service",
                "url": nps_locks["url"],
                "description": "Authority for the lift-lock count and numbering.",
                "published_at": None,
                "retrieved_at": None,
                "checked_at": SOURCE_CHECKED_AT,
            },
            {
                "id": TRUST_LOCK_SOURCE_ID,
                "name": trust_locks["name"],
                "organization": "C&O Canal Trust",
                "url": trust_locks["url"],
                "description": "Practical lift-lock mileposts and common names.",
                "published_at": None,
                "retrieved_at": None,
                "checked_at": SOURCE_CHECKED_AT,
            },
            {
                "id": TOWPATH_SOURCE_ID,
                "name": "National Park Service Public Trails dataset",
                "organization": "National Park Service",
                "url": FEATURESERVER_URL,
                "description": (
                    "Underlying geometry for the canonical C&O Canal towpath."
                ),
                "published_at": None,
                "retrieved_at": "2026-08-31",
                "checked_at": SOURCE_CHECKED_AT,
            },
        ],
        key=lambda source: source["id"],
    )
    artifacts = {
        "access-points": [ACCESS_SOURCE_ID, RECREATION_SOURCE_ID],
        "aqueducts": [
            AQUEDUCT_MILE_SOURCE_ID,
            AQUEDUCT_SOURCE_ID,
            TOWPATH_SOURCE_ID,
        ],
        "campsites": [CAMPSITE_SOURCE_ID, TOWPATH_SOURCE_ID],
        "features": [
            ACCESS_SOURCE_ID,
            AQUEDUCT_MILE_SOURCE_ID,
            AQUEDUCT_SOURCE_ID,
            CAMPSITE_SOURCE_ID,
            NPS_LOCK_SOURCE_ID,
            RECREATION_SOURCE_ID,
            TOWPATH_SOURCE_ID,
            TRUST_LOCK_SOURCE_ID,
        ],
        "locks": [NPS_LOCK_SOURCE_ID, TRUST_LOCK_SOURCE_ID, TOWPATH_SOURCE_ID],
        "relationships": [
            ACCESS_SOURCE_ID,
            AQUEDUCT_MILE_SOURCE_ID,
            CAMPSITE_SOURCE_ID,
            NPS_LOCK_SOURCE_ID,
            RECREATION_SOURCE_ID,
            TRUST_LOCK_SOURCE_ID,
        ],
        "towpath.geojson": [TOWPATH_SOURCE_ID],
    }
    return {
        "schema_version": SOURCE_SCHEMA_VERSION,
        "sources": sources,
        "artifacts": artifacts,
    }


__all__ = ["build_sources"]
