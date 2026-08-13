from heartlight.corpus import append_lesson, build_profile, ingest_artifact, init_project


def test_family_archive_pipeline(tmp_path):
    vault_path = tmp_path / "lantern"
    init_project(vault_path, "Test Lantern")

    story = tmp_path / "story.txt"
    story.write_text("She always sang while cooking.", encoding="utf-8")
    record = ingest_artifact(vault_path, story, kind="text", source="family note")
    assert len(record.sha256) == 64

    append_lesson(
        vault_path,
        prompt="What did cooking sound like?",
        response="Singing and pans clattering.",
        teacher="Family",
    )
    profile = build_profile(vault_path)
    assert profile["display_name"] == "Test Lantern"
    assert profile["text_corpus"][0]["text"] == "She always sang while cooking."
    assert profile["family_teaching"][0]["teacher"] == "Family"
    assert "not the deceased person" in profile["disclosure"]
