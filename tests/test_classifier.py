import shutil
import types
from pathlib import Path

import classifier


def test_classify_image_extension_fallback(monkeypatch, tmp_path):
    dummy = tmp_path / "image.png"
    dummy.touch()
    monkeypatch.setattr(classifier, "_load_classifier", lambda: (None, None, None))

    result = classifier.classify_image(str(dummy))
    assert result == "anime"


def test_move_to_category_moves_file(tmp_path, monkeypatch):
    src = tmp_path / "pic.jpg"
    src.write_text("data")
    monkeypatch.chdir(tmp_path)

    moved = {}

    def fake_move(src_path, dst_path):
        moved["src"] = src_path
        moved["dst"] = dst_path

    monkeypatch.setattr(shutil, "move", fake_move)

    dest = classifier.move_to_category(str(src), "photo")
    expected = str(Path("data/photos/pic.jpg"))
    assert dest == expected
    assert moved["src"] == str(src)
    assert str(moved["dst"]) == expected


def test_prepare_image_calls_classify_and_move(monkeypatch):
    calls = {}

    def fake_classify(path):
        calls["classify"] = path
        return "anime"

    def fake_move(path, image_type):
        calls["move"] = (path, image_type)
        return f"/new/{path}"

    class DummyTagger:
        pass

    def fake_get_tagger(image_type):
        calls["tagger"] = image_type
        return DummyTagger()

    monkeypatch.setattr(classifier, "classify_image", fake_classify)
    monkeypatch.setattr(classifier, "move_to_category", fake_move)
    monkeypatch.setattr(classifier, "get_tagger", fake_get_tagger)

    new_path, tagger = classifier.prepare_image("old/file.png")

    assert new_path == "/new/old/file.png"
    assert isinstance(tagger, DummyTagger)
    assert calls["classify"] == "old/file.png"
    assert calls["move"] == ("old/file.png", "anime")
    assert calls["tagger"] == "anime"


def test_load_classifier_handles_three_outputs(monkeypatch):
    dummy_model = object()
    dummy_preprocess_val = object()

    def fake_create_model_and_transforms(name, pretrained=None):
        return dummy_model, object(), dummy_preprocess_val

    def fake_get_tokenizer(name):
        return "tok"

    dummy_module = types.SimpleNamespace(
        create_model_and_transforms=fake_create_model_and_transforms,
        get_tokenizer=fake_get_tokenizer,
    )
    monkeypatch.setattr(classifier, "open_clip", dummy_module)
    monkeypatch.setattr(classifier, "torch", object())
    monkeypatch.setattr(classifier, "Image", object())
    monkeypatch.setattr(classifier, "_model", None)
    monkeypatch.setattr(classifier, "_preprocess", None)
    monkeypatch.setattr(classifier, "_tokenizer", None)

    model, preprocess, tokenizer = classifier._load_classifier()

    assert model is dummy_model
    assert preprocess is dummy_preprocess_val
    assert tokenizer == "tok"

