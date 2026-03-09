# pokemon_jsonl_builder.py
# 
# Creates JSONL from user input to structure data from posts on r/pokemontrade to prep for finetuning LLMs.
#
# Author: Levester Williams
# Date: 8 March 2026
# Platform info:
#   - Python 3.13.12


from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List


SYSTEM_PROMPT = (
    "Generate a JSON string that describes a Pokémon trade or giveaway, including "
    "sender's and receiver's Pokémon details such as the name, IV, gender, ability, "
    "hidden ability, region, language, and form of each Pokemon."
)

OUTPUT_FILENAME = "ft_llm_pkmntrades_reddit_posts.jsonl"

# Sentinel padding value to indicate "user did not specify this IV"
IV_PAD_VALUE = 32


def desktop_path(filename: str) -> Path:
    """
    Returns a best-effort Desktop path across macOS/Windows/Linux.
    Falls back to home directory if Desktop does not exist.
    """
    home = Path.home()
    desktop = home / "Desktop"
    return (desktop if desktop.exists() else home) / filename


def prompt_str(prompt: str) -> str:
    return input(prompt).strip()


def prompt_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in {"yes", "y"}:
            return True
        if ans in {"no", "n"}:
            return False
        print("Please type: yes, no, y, or n.")


def ensure_file_ready(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text("", encoding="utf-8")
        return

    if path.stat().st_size == 0:
        return

    with path.open("rb") as f:
        f.seek(-1, os.SEEK_END)
        last = f.read(1)

    if last != b"\n":
        with path.open("ab") as f:
            f.write(b"\n")


def parse_ivs_6_ints(raw: str, pad_value: int = IV_PAD_VALUE) -> List[int]:
    """
    Accepts comma, slash, or whitespace delimiters.
    Validates that provided IVs are integers in [0, 31].
    Pads missing values with `pad_value` up to 6, truncates extras.
    """
    raw = raw.strip()

    if raw == "":
        ivs: List[int] = []
    else:
        parts = [p for p in re.split(r"[\s,/]+", raw) if p]
        ivs = []
        for p in parts:
            iv = int(p)
            if not (0 <= iv <= 31):
                raise ValueError("IV out of range")
            ivs.append(iv)

    if len(ivs) < 6:
        ivs = ivs + [pad_value] * (6 - len(ivs))
        print(f"IVs padded to 6 values with {pad_value} (meaning: not provided).")
    elif len(ivs) > 6:
        ivs = ivs[:6]
        print("IVs truncated to first 6 values.")

    return ivs


def prompt_ivs_6() -> List[int]:
    while True:
        raw = prompt_str("Enter the Pokemon's IVs (comma/slash/space delimited, 0-31): ")
        try:
            return parse_ivs_6_ints(raw)
        except ValueError:
            print("Invalid IVs. Enter integers 0–31, separated by commas, slashes, or spaces.")


def prompt_one_pokemon() -> Dict[str, Any]:
    name = prompt_str("Enter the Pokemon's name: ")
    ivs = prompt_ivs_6()
    nature = prompt_str("Enter the Pokemon's nature: ")
    gender = prompt_str("Enter the Pokemon's gender: ")
    ability = prompt_str("Enter the Pokemon's ability: ")
    language = prompt_str("Enter the Pokemon's language: ")
    form = prompt_str("Enter the Pokemon's form: ")
    special = prompt_str("Enter the Pokemon's special: ")
    pokeball = prompt_str("Enter the Pokemon's pokeball: ")
    shiny = prompt_yes_no("Is the Pokemon shiny? YES or NO: ")

    return {
        "Pokemon": name,
        "IVs": ivs,
        "nature": nature,
        "gender": gender,
        "ability": ability,
        "language": language,
        "form": form,
        "special": special,
        "pokeball": pokeball,
        "shiny": shiny,
    }


def prompt_many_senders() -> List[Dict[str, Any]]:
    has_sender = prompt_yes_no("Does the post contains a Pokemon to send? YES or NO: ")
    if not has_sender:
        return []

    senders: List[Dict[str, Any]] = []
    while True:
        senders.append(prompt_one_pokemon())
        more = prompt_yes_no("Are there more sender's Pokemon? YES or NO: ")
        if not more:
            break
    return senders


def prompt_many_requested() -> List[Dict[str, Any]]:
    has_requested = prompt_yes_no("Does the post contains a requested Pokemon? YES or NO: ")
    if not has_requested:
        return []

    requested: List[Dict[str, Any]] = []
    while True:
        requested.append(prompt_one_pokemon())
        more = prompt_yes_no("Are there more requested Pokemon? YES or NO: ")
        if not more:
            break
    return requested


def build_jsonl_line(
    subreddit_post: str,
    senders: List[Dict[str, Any]],
    requested: List[Dict[str, Any]],
    version: str,
    action: str,
) -> Dict[str, Any]:
    assistant_payload = {
        "sender's Pokemon": senders,
        "requested Pokemon": requested,
        "version": version,
        "action": action,
    }

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": subreddit_post},
            {"role": "assistant", "content": json.dumps(assistant_payload, ensure_ascii=False)},
        ]
    }


def append_line(path: Path, obj: Dict[str, Any]) -> None:
    ensure_file_ready(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False))
        f.write("\n")


def main() -> None:
    out_path = desktop_path(OUTPUT_FILENAME)
    print(f"Output file: {out_path}")

    while True:
        subreddit_post = prompt_str("Type subreddit post here: ")

        senders = prompt_many_senders()
        requested = prompt_many_requested()

        version = prompt_str("Enter the game version: ")
        action = prompt_str("Enter the action: ")

        obj = build_jsonl_line(
            subreddit_post=subreddit_post,
            senders=senders,
            requested=requested,
            version=version,
            action=action,
        )

        append_line(out_path, obj)
        print(f"Wrote 1 line to: {out_path}")

        again = prompt_yes_no("Do you want to add another line? YES or NO: ")
        if not again:
            print("Done. File saved.")
            break


if __name__ == "__main__":
    main()