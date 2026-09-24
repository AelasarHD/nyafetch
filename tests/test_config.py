from nyafetch.config import NyafetchConfig


def test_load_missing_file_returns_defaults(tmp_path):
    cfg = NyafetchConfig.load(tmp_path / "missing.toml")
    assert cfg.fields[0] == "os"
    assert cfg.no_color is False
    assert cfg.accent_color is None


def test_save_then_load_roundtrip(tmp_path):
    path = tmp_path / "config.toml"
    original = NyafetchConfig(fields=["os", "cpu"], accent_color="green", no_color=True, classic=True)
    original.save(path)
    loaded = NyafetchConfig.load(path)
    assert loaded.fields == ["os", "cpu"]
    assert loaded.accent_color == "green"
    assert loaded.no_color is True
    assert loaded.classic is True


def test_load_corrupt_file_falls_back_to_defaults(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text("this is not valid = = toml", encoding="utf-8")
    cfg = NyafetchConfig.load(path)
    assert cfg.fields[0] == "os"
