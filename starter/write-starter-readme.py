#!/usr/bin/env python3
"""Prepend "how to use this starter" instructions to the rendered starter README (used by publish-starter.yml)."""
import sys
from pathlib import Path

root, source_repo, commit = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
readme = root / "README.md"
intro = f"""> [!NOTE]
> This repository is a **GitHub template** generated automatically from
> [{source_repo}](https://github.com/{source_repo}) @ `{commit}` with the default answers.
> Click **Use this template**, clone your new repo, then rename the mod:
>
> ```sh
> python3 rename-mod.py --modid mymod --package io.github.me.mymod --name "My Mod" --github-user me
> ./gradlew build
> ```
>
> Prefer Copier (`uvx copier copy gh:{source_repo} .`) if you want to answer the questions yourself
> (e.g. a project without MieLib/HexCLI) or `copier update` later. Don't open pull requests here:
> this repo is overwritten on every publish.

"""
readme.write_text(intro + readme.read_text(encoding="utf-8"), encoding="utf-8")
