from nyafetch.mood import compute_mood


def test_low_load_is_zen():
    mood = compute_mood(cpu_percent=5, memory_percent=10, disk_percent=20)
    assert mood.name == "zen"


def test_high_load_is_overloaded():
    mood = compute_mood(cpu_percent=95, memory_percent=10, disk_percent=10)
    assert mood.name == "overloaded"


def test_uses_the_worst_metric():
    mood = compute_mood(cpu_percent=5, memory_percent=85, disk_percent=10)
    assert mood.name == "stressed"


def test_boundary_at_40_is_chill_not_zen():
    mood = compute_mood(cpu_percent=40, memory_percent=0, disk_percent=0)
    assert mood.name == "chill"


def test_every_mood_has_face_and_caption():
    for cpu in (10, 45, 65, 85, 99):
        mood = compute_mood(cpu, 0, 0)
        assert mood.face
        assert mood.caption
        assert mood.color
