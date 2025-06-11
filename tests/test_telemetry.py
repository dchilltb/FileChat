from telemetry.collector import record_event
import json, pathlib, tempfile

def test_event_is_json(tmp_path: pathlib.Path, capsys):
    record_event("demo", foo=1)
    out, _ = capsys.readouterr()
    obj = json.loads(out)
    assert obj["event"] == "demo" and obj["foo"] == 1