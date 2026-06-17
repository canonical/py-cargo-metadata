import json
from pathlib import Path

import pytest
from pydantic.json_schema import GenerateJsonSchema

from cargo_metadata import Metadata


class GenerateJsonSchemaNoTitles(GenerateJsonSchema):
    def field_title_should_be_set(self, _) -> bool: # pyright: ignore[reportIncompatibleMethodOverride]
        return False


SNAPSHOT_PATH = Path(__file__).parent / "snapshots" / "metadata.schema.json"


def test_metadata_json_schema_snapshot(pytestconfig: pytest.Config) -> None:
    schema = Metadata.model_json_schema(schema_generator=GenerateJsonSchemaNoTitles)
    snapshot_text = json.dumps(schema, indent=2, sort_keys=True) + "\n"

    if pytestconfig.getoption("--snapshot-update") or not SNAPSHOT_PATH.exists():
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_PATH.write_text(snapshot_text, encoding="utf-8")

    assert SNAPSHOT_PATH.read_text(encoding="utf-8") == snapshot_text
