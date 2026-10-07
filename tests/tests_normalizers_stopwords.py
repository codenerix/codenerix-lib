"""The stopwords corpus is loaded lazily and never downloaded."""

import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import nltk
import pytest

from codenerix_lib import normalizers


class _MissingCorpus:
    # Stand-in for nltk's LazyCorpusLoader when the corpus is not installed
    def words(self, language: str) -> list[str]:
        raise LookupError("Resource stopwords not found.")


class _TinyCorpus:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def words(self, language: str) -> list[str]:
        self.calls.append(language)
        return ["the"]


@pytest.fixture(autouse=True)
def fresh_cache() -> Iterator[None]:
    # Each test decides what the corpus loader sees
    normalizers._stop_words.cache_clear()
    yield
    normalizers._stop_words.cache_clear()


def _no_download(*args: object, **kwargs: object) -> bool:
    raise AssertionError("nltk.download must never be called")


def test_import_never_downloads(tmp_path: Path) -> None:
    # Fresh interpreter, empty HOME: a download would land in HOME/nltk_data
    env = {
        **os.environ,
        "HOME": str(tmp_path),
        "NLTK_DATA": str(tmp_path / "empty"),
        "NLTK_ALLOW_PROXIED_URLOPEN": "1",
    }
    subprocess.run(
        [sys.executable, "-c", "import codenerix_lib.normalizers"],
        env=env,
        check=True,
    )
    assert not (tmp_path / "nltk_data").exists()


def test_missing_corpus_raises_with_install_hint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(normalizers, "stopwords", _MissingCorpus())
    monkeypatch.setattr(nltk, "download", _no_download)
    with pytest.raises(normalizers.MissingStopwordsError) as excinfo:
        normalizers.strong_normalizer("The quick brown fox")
    assert "python -m nltk.downloader stopwords" in str(excinfo.value)
    # Callers catching nltk's LookupError keep working
    assert isinstance(excinfo.value, LookupError)


def test_corpus_is_loaded_once(monkeypatch: pytest.MonkeyPatch) -> None:
    corpus = _TinyCorpus()
    monkeypatch.setattr(normalizers, "stopwords", corpus)
    assert normalizers.strong_normalizer("The quick fox") == "quick fox"
    assert normalizers.strong_normalizer("The lazy dog") == "lazy dog"
    assert corpus.calls == ["english"]
