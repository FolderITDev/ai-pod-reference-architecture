"""Deterministic, offline token counting.

tiktoken normally downloads its BPE merge-rank files over the network on
first use. That would violate this repo's no-network guarantee, so the
merge-rank file for each supported encoding is bundled locally under
data/*.tiktoken and loaded from disk instead. The bundled cl100k_base file
is the official OpenAI file (sha256 223921b7...865b2a7, matching the hash
tiktoken itself checks); only the download step is replaced, not the data.
"""

from __future__ import annotations

import os

import tiktoken
from tiktoken.load import load_tiktoken_bpe

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

_ENCODING_SPECS = {
    "cl100k_base": {
        "expected_hash": "223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7",
        "pat_str": (
            r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}++|\p{N}{1,3}+"""
            r"""| ?[^\s\p{L}\p{N}]++[\r\n]*+|\s++$|\s*[\r\n]|\s+(?!\S)|\s"""
        ),
        "special_tokens": {
            "<|endoftext|>": 100257,
            "<|fim_prefix|>": 100258,
            "<|fim_middle|>": 100259,
            "<|fim_suffix|>": 100260,
            "<|endofprompt|>": 100276,
        },
    },
}

_encoding_cache: dict[str, tiktoken.Encoding] = {}


def _load_encoding(encoding_name: str) -> tiktoken.Encoding:
    if encoding_name in _encoding_cache:
        return _encoding_cache[encoding_name]
    if encoding_name not in _ENCODING_SPECS:
        raise ValueError(
            f"No locally bundled encoding for {encoding_name!r}; "
            f"available offline: {sorted(_ENCODING_SPECS)}"
        )
    spec = _ENCODING_SPECS[encoding_name]
    bpe_path = os.path.join(_DATA_DIR, f"{encoding_name}.tiktoken")
    mergeable_ranks = load_tiktoken_bpe(bpe_path, expected_hash=spec["expected_hash"])
    encoding = tiktoken.Encoding(
        name=encoding_name,
        pat_str=spec["pat_str"],
        mergeable_ranks=mergeable_ranks,
        special_tokens=spec["special_tokens"],
    )
    _encoding_cache[encoding_name] = encoding
    return encoding


def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens in text with a locally bundled encoding. Deterministic, offline."""
    encoding = _load_encoding(encoding_name)
    return len(encoding.encode(text, disallowed_special=()))
