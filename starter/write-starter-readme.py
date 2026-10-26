#!/usr/bin/env python3
"""Prepend "how to use this starter" notes to the rendered starter READMEs (used by publish-starter.yml).

README.md gets an English note, README.zh-CN.md a Chinese one.
"""
import sys
from pathlib import Path

root, source_repo, commit = Path(sys.argv[1]), sys.argv[2], sys.argv[3]

notes = {
    "README.md": f"""> [!NOTE]
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

""",
    "README.zh-CN.md": f"""> [!NOTE]
> 这是一个 **GitHub 模板仓库**，由 [{source_repo}](https://github.com/{source_repo}) @ `{commit}`
> 按默认答案自动生成。点 **Use this template** 建好你自己的仓库，clone 下来，然后把模组改成你的名字：
>
> ```sh
> python3 rename-mod.py --modid mymod --package io.github.me.mymod --name "My Mod" --github-user me
> ./gradlew build
> ```
>
> 想自己回答生成时的问题（比如不要 MieLib/HexCLI），或者以后想用 `copier update` 跟进模板更新，
> 请改用 Copier：`uvx copier copy gh:{source_repo} .`。
> 这个仓库每次发布都会被整个覆盖，所以请不要往这里提 PR。

""",
}

for name, intro in notes.items():
    readme = root / name
    if readme.exists():
        readme.write_text(intro + readme.read_text(encoding="utf-8"), encoding="utf-8")
