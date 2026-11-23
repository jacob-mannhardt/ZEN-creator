"""Unit tests for MetaData."""

from __future__ import annotations

import pytest

from zen_creator.datasets.datasets.metadata import MetaData


def _metadata(doi: str | None, url: str | None = None) -> MetaData:
    return MetaData(
        name="x",
        title="T",
        author=["A"],
        publication="P",
        publication_year=2020,
        url=url,
        doi=doi,
    )


@pytest.mark.parametrize(
    "doi",
    [
        "10.1016/j.x.2020.1",
        "https://doi.org/10.1016/j.x.2020.1",
        "http://dx.doi.org/10.1016/j.x.2020.1",
        "doi:10.1016/j.x.2020.1",
        " HTTPS://DOI.ORG/10.1016/j.x.2020.1 ",
    ],
)
def test_doi_is_stored_bare(doi: str) -> None:
    """Every accepted DOI form is stored bare and cited as one doi.org link."""
    metadata = _metadata(doi)
    assert metadata.doi == "10.1016/j.x.2020.1"
    assert metadata.to_str().endswith(" https://doi.org/10.1016/j.x.2020.1")


def test_missing_doi_stays_none() -> None:
    assert _metadata(None, url="https://example.org").doi is None


@pytest.mark.parametrize("url", [None, ""])
def test_url_or_doi_is_required(url: str | None) -> None:
    """A source without url and doi cannot be traced and is rejected."""
    with pytest.raises(ValueError, match="needs a url or a doi"):
        _metadata(None, url=url)
