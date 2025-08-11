import builtins
import main


def test_main_uses_console_when_no_token(monkeypatch):
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    called = {}

    def fake_run_console():
        called["run"] = True

    monkeypatch.setattr(main, "run_console", fake_run_console)

    main.main()

    assert called.get("run") is True


def test_run_console_processes_image(monkeypatch, tmp_path, capsys):
    img = tmp_path / "img.png"
    img.touch()

    inputs = iter([str(img), "exit"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    called = {}

    def fake_classify(path):
        called["classify"] = path
        return "anime"

    class DummyTagger:
        def suggest_tags(self, path):
            called["tagger"] = path
            return ["tag1", "tag2"]

    def fake_get_tagger(image_type):
        called["get_tagger"] = image_type
        return DummyTagger()

    monkeypatch.setattr(main, "classify_image", fake_classify)
    monkeypatch.setattr(main, "get_tagger", fake_get_tagger)

    main.run_console()

    assert called["classify"] == str(img)
    assert called["get_tagger"] == "anime"
    assert called["tagger"] == str(img)
    output = capsys.readouterr().out
    assert "tag1" in output and "tag2" in output
