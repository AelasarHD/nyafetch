from nyafetch.collectors.base import InfoSnapshot
from nyafetch.render import render


def make_snapshot() -> InfoSnapshot:
    return InfoSnapshot(
        os_name="macOS 15.0",
        host="mitchbook",
        kernel="24.0.0",
        uptime="2h 3m",
        shell="zsh",
        terminal="iTerm",
        cpu="Apple M2",
        gpu="Apple M2 GPU",
        ram="16.0 GB | 6400 MHz",
        disk="100.0 GiB / 500.0 GiB (20%)",
        python_version="3.12.0",
    )


def test_render_includes_requested_fields_no_color():
    output = render(make_snapshot(), logo_lines=["AAA", "BBB"], fields=["os", "cpu"], no_color=True)
    assert "OS: macOS 15.0" in output
    assert "CPU: Apple M2" in output
    assert "Host:" not in output  # not requested


def test_render_includes_host_header():
    output = render(make_snapshot(), logo_lines=["X"], fields=["os"], no_color=True)
    assert "mitchbook" in output


def test_render_no_color_has_no_ansi_codes():
    output = render(make_snapshot(), logo_lines=["X"], fields=["os"], no_color=True)
    assert "\x1b[" not in output


def test_render_color_adds_ansi_codes():
    output = render(make_snapshot(), logo_lines=["X"], fields=["os"], no_color=False)
    assert "\x1b[" in output


def test_render_unknown_field_is_ignored():
    output = render(make_snapshot(), logo_lines=["X"], fields=["not_a_real_field"], no_color=True)
    assert "not_a_real_field" not in output
