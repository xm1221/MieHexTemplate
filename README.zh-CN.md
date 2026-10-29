# MieHexTemplate

[English](README.md) | **简体中文**

[![powered by hexdoc](https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc?label=1)](https://github.com/hexdoc-dev/hexdoc)

这是一个 [Copier](https://copier.readthedocs.io) 模板，用来开 [Hex Casting](https://github.com/FallingColors/HexMod) 附属模组的新项目：**Minecraft 1.20.1**、Architectury **双端（Fabric + Forge）**、**Kotlin**，对应 **Hex Casting 0.11.4**。

MieHexTemplate 是从 [HexDummy v2](https://github.com/FallingColors/hexdummy)（作者 artynova、Falling Colors，MIT 协议）fork 来的。HexDummy 原有的东西都还在：hexdoc 文档、CI 和发布工作流、Registrar 注册工具。在此基础上，我们又加了几样：

- **升级到 Hex Casting 0.11.4**，相应的工具链也一起升了：Kotlin 2.2.21、fabric-language-kotlin 1.13.7、KotlinForForge 4.12.0、Architectury Loom 1.9、Gradle 8.11.1。
- 多一个示例图案：「平方之馏化」（`<modid>:square`），演示最简单的 `ConstMediaAction` 怎么写。
- 可选的 **[MieLib](https://github.com/xm1221/MieLib) + HexCLI 开发流程**。生成项目时会问你 `use_mielib`，默认是“是”。选了以后会多出这些：
  - MieLib，两端都以 Jar-in-Jar 方式打包进你的模组。Fabric 版直接从 MieLib 的 GitHub Release 下载，Forge 版目前没有公开下载，所以放在 `libs/` 里随模板分发。
  - [hexParse](https://modrinth.com/mod/hexparse)，**只在开发环境运行时加载**，不会成为你发布出去的模组的依赖。
  - HexDebug 和 IoticBlocks 也只用于开发环境，补齐 hexParse 1.12.0 的运行时依赖；模板会把 HexDebug 的核心 Jar-in-Jar 展开给 Loom 开发运行使用。
  - `./gradlew :fabric:runHexCli -PacceptEula=true` 和 `./gradlew :forge:runHexCli -PacceptEula=true`，分别启动开启了 `-Dmielib.hexcli=true` 的无头 Fabric / Forge 开发服务器。
  - `scripts/hexcli-check.sh`：把 `hexcli/examples.tsv` 里的例子逐条交给 `hexcli-client -e` 执行，核对栈和消息，并且能区分「解析错误」（`hexParse: Unknown symbol`）和「事故」（mishap）。
  - `skills/hexcasting/SKILL.md`：HexCLI / hexParse 速查手册，人和 AI 都能看。

  如果选“否”，上面这些文件和依赖一个都不会生成。

> [!TIP]
> 不想装 Copier？我们在 GitHub 模板仓库 [xm1221/MieHexTemplate-Starter](https://github.com/xm1221/MieHexTemplate-Starter)
> 里放了一份按默认答案渲染好的项目。点 **Use this template** 建好自己的仓库，再运行：
> `python3 rename-mod.py --modid yourmod --package com.example.yourmod --name "Your Mod"` 改成你自己的模组名就行。
> 不过还是更推荐用 Copier：以后模板有更新，可以直接 `copier update` 同步到你的项目里。

> [!TIP]
> 如果你只做 Fabric 或只做 Forge，大概用不着这个模板，[Fabric 模板生成器](https://fabricmc.net/develop/template/) 或 [Forge MDK](https://docs.minecraftforge.net/en/1.20.1/gettingstarted/) 会更合适。

## 使用方法

1. 先装好这些：
   - [Git](https://github.com/git-guides/install-git)
   - [uv](https://docs.astral.sh/uv/getting-started/installation/)
   - 支持 Java 和 Kotlin 的 IDE（推荐 [IntelliJ IDEA 社区版](https://www.jetbrains.com/idea/download/)）
2. 在 GitHub 上新建一个**空**仓库，clone 下来并进入目录。不需要再套别的项目模板（比如 IntelliJ 自带的 Minecraft 模组模板）。
> [!CAUTION]
> **不要**直接 fork、clone 或复制本仓库。本仓库只是模板源码，本身不是能编译的模组。
3. 在仓库根目录运行下面的命令，按提示回答问题：
   ```sh
   uvx copier copy gh:xm1221/MieHexTemplate .
   ```
4. 配置 Python 环境并生成 lock 文件：
   ```sh
   uv sync

   .\.venv\Scripts\activate   # Windows
   . .venv/bin/activate.fish  # fish
   source .venv/bin/activate  # 其他 shell
   ```
5. 把生成的项目检查一遍，没问题就把所有文件（包括 `uv.lock`）提交并推送：
   ```sh
   git add .
   git update-index --chmod=+x gradlew
   git commit -m "Set up mod template"
   git push
   ```
6. 按照 [hexdoc 的说明](https://hexdoc.hexxy.media/docs/guides/deployment/github-pages) 配置 GitHub Pages。
7. 配置发布工作流：
   1. 在仓库设置里新建两个 environment：`pypi` 和 `curseforge-modrinth`。
   2. 在 `curseforge-modrinth` 里添加下面两个 environment **secret**（注意不是 variable）：
      - `CURSEFORGE_TOKEN`：新建一个 [CurseForge API token](https://authors-old.curseforge.com/account/api-tokens)。
      - `MODRINTH_TOKEN`：新建一个带 `Create versions` 权限的 [Modrinth PAT](https://modrinth.com/settings/pats)。
   3. [在 PyPI 创建一个 pending publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)，填写：
      - PyPI Project Name：`pyproject.toml` 里的 `project.name`（例如 `hexdoc-hexcasting`）
      - Owner：你的 GitHub 用户名
      - Repository name：你的仓库名
      - Workflow name：`release.yml`
      - Environment name：`pypi`
   4. 如果想发布到 https://maven.hexxy.media，参考[这篇说明](https://gist.github.com/object-Object/f9988135bec5cef653c668712954f429)。
   5. 模组准备好之后，到 Actions 页面[手动触发 release 工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)。

更详细的写法可以参考 [HexDebug](https://github.com/object-Object/HexDebug) 和 [IoticBlocks](https://github.com/object-Object/IoticBlocks)，HexDummy 很大程度上就是照着这两个模组搭的。

## HexCLI 开发流程（`use_mielib` 选“是”时）

```sh
./gradlew :fabric:runHexCli -PacceptEula=true    # 启动无头 Fabric 服务器，目录 fabric/run/hexcli（加这个参数即表示你同意 Minecraft EULA）
./gradlew :forge:runHexCli -PacceptEula=true     # Forge 版，目录 forge/run/hexcli
./scripts/hexcli-check.sh --accept-eula          # 没有服务器时自动启动，跑完 hexcli/examples.tsv 再自动关掉
./scripts/hexcli-check.sh --platform forge --accept-eula   # 同上，换成 Forge 服务器
./scripts/hexcli-check.sh -f hexcli/examples-broken.tsv    # 故意写错的例子：一个解析错误、一个事故，用来看报错长什么样
```

注意要写 `:fabric:` 或 `:forge:` 前缀。直接写 `./gradlew runHexCli` 会让 Gradle 依次启动两个服务器，而第一个服务器不关，第二个就永远不会启动。

Forge 版的 `runHexCli` 额外加了 `-Djava.net.preferIPv4Stack=true`。原因是 Forge 启动时带着 `-Djava.net.preferIPv6Addresses=system`，MieLib 的 HexCLI 端口（用 `InetAddress.getLoopbackAddress()` 绑定）会监听在 `[::1]` 上，可 `hexcli/client.json` 里写的是 `127.0.0.1`，客户端就会报 `Connection refused`。

`hexcli-check.sh` 会从 MieLib 的 `hexcli-v1.0.0` Release 下载 `hexcli-client.jar`，并用 `SHA256SUMS` 校验。`hexcli/examples.tsv` 每行的格式是
`名称<TAB>代码<TAB>预期结果<TAB>预期栈<TAB>消息正则`，预期结果可以是 `OK`、`PARSE_ERROR`、`MISHAP` 或 `HEXCLI_ERROR`。

## Starter 模板仓库和自动同步

[`.github/workflows/publish-starter.yml`](.github/workflows/publish-starter.yml) 会做这几件事：

1. 用默认答案（`modid = miehexaddon`）渲染本模板，并编译一遍。
2. 复制一份，用 [`starter/rename-mod.py`](starter/rename-mod.py) 改名，确认改完还能编译。
3. 把结果作为一个单独的提交推送到模板仓库 `xm1221/MieHexTemplate-Starter`。这一步是强制推送，Starter 仓库原有的历史会被替换掉。

- 触发方式：推送 `v*` 标签，或者在 Actions 页面手动运行。手动运行时可以填 `target_repo`、`target_branch`、`dry_run`。
- 需要的 secret：**`STARTER_REPO_TOKEN`**。用一个 fine-grained PAT，给 Starter 仓库开 *Contents: read and write* 权限即可。secret 的名字写在工作流的 `TOKEN_SECRET_NAME` 环境变量里，想改名的话改那里。

### 改名脚本 `rename-mod.py`

Starter 仓库根目录自带这个脚本，只用 Python 标准库。它会一次性替换 mod id、包名、类名前缀、显示名称和 GitHub 用户名/仓库名，也会移动包目录、重命名相关文件：

```sh
python3 rename-mod.py --modid mymod --package io.github.me.mymod --name "My Mod" --github-user me
# 可选：--classname MyMod --github-repo mymod --dry-run（只打印要改什么，不实际修改）
./gradlew build
```

## 参考项目

HexDummy 上游的示例项目（不含 MieHexTemplate 的改动）：

- [example/v2/mojmap](https://github.com/FallingColors/hexdummy/tree/example/v2/mojmap)
- [example/v2/yarn](https://github.com/FallingColors/hexdummy/tree/example/v2/yarn)
- https://github.com/object-Object/HexDummyExample（含 Actions 运行记录和 hexdoc 网页）

## 常见问题

### 为什么不做成 GitHub 模板仓库，为什么不能直接 fork？

MieHexTemplate 和 HexDummy 一样用 [Copier](https://copier.readthedocs.io) 生成项目。运行 `uvx copier copy` 时，Copier 会拉取本仓库，问你几个问题，然后把答案填进模板里的占位符，生成一个已经定制好的项目，你不用再手动替换任何东西。

所以本仓库本身**不是**一个能用的模组。看看 [template](./template) 目录就知道，里面全是还没填值的 `.jinja` 文件。真要用 GitHub 模板仓库的话，请用上面提到的 [MieHexTemplate-Starter](https://github.com/xm1221/MieHexTemplate-Starter)。

### 依赖要加在哪里？

- Maven 仓库：`buildSrc/src/main/kotlin/<modid>/java.gradle.kts`
- 依赖的版本和坐标：`gradle/libs.versions.toml`（[Gradle 文档](https://docs.gradle.org/current/userguide/version_catalogs.html#sec::toml-dependencies-format)）
- Gradle 依赖配置：`{common,fabric,forge}/build.gradle.kts`，看你需要在哪个平台上用
- hexdoc 依赖：`pyproject.toml` 和 `doc/hexdoc.toml`（改完记得 `uv sync` 更新 `uv.lock`）
- 本地 JAR 依赖：`libs/`
- Gradle 插件的 Maven 仓库：`settings.gradle.kts`
- `buildSrc` 里约定插件用到的 Gradle 插件，它们的仓库和依赖：`buildSrc/build.gradle.kts`

### 为什么发布工作流要手动触发？

Minecraft 模组发布很容易出岔子。发布工作流给每个发布平台都单独设了开关，某个平台失败了，修好后只重新发那一个就行，不用再推新标签、整个重新发一遍。

### `(ModName)Registrar` 是什么？为什么不用 Architectury 的 DeferredRegister？

Architectury 的 DeferredRegister [不支持模组自己的注册表](https://github.com/architectury/architectury-api/issues/513)，在 Kotlin 里用起来也不太顺手。所以模板会生成一个 Registrar 基类，原版注册表和模组注册表都能用它注册。

要给某个注册表加一个 registrar，就写一个继承它的 `object`，把注册表的 ResourceKey 和一个返回注册表本体的回调传给父类（用回调是为了避免在 Forge 上过早初始化注册表），再把它加进通用初始化里的 `initRegistries` 调用。示例见 [HexDummyExample](https://github.com/object-Object/HexDummyExample/blob/a7d8d5b58bd018a62456e4653fe46ba3eb22bc69/common/src/main/kotlin/io/github/objectobject/hexdummyexample/registry/HexdummyexampleActions.kt#L11-L14)。

注册一般长这样：

```kt
val REGISTERED_THING = register("registered_thing") { ThingConstructor("parameters") }
```

`register` 收一个回调，原因同上：避免在 Forge 上过早构造实例。字符串是 ResourceLocation 的路径部分，命名空间是你的 mod id。返回值是一个 `Entry<V>`，可以用 `.id` 取 id、`.key` 取 ResourceKey，确定注册完成后可以用 `.value` 取到注册的对象。模板里自带了注册图案的例子，HexDebug 里还有[更多注册表的例子](https://github.com/object-Object/HexDebug/tree/5db5f78f5489863e2c20a3df472571a984877b7d/Common/src/main/kotlin/gay/object/hexdebug/registry)。

### 支持 Yarn 映射吗？

上游 HexDummy 的 Yarn 支持还没做完，示例代码用的是 Mojmap 的类名，所以选 Yarn 时目前编译不过。请使用默认的 Mojmap。

## 致谢与协议

- [HexDummy v2](https://github.com/FallingColors/hexdummy)，Copyright (c) 2025 artynova, Falling Colors，MIT 协议。本仓库是它的 fork。
- [MieLib](https://github.com/xm1221/MieLib)（MIT 协议）：提供 HexCLI、`libs/` 里的 Forge jar 和 `skills/hexcasting/SKILL.md`。
- MieHexTemplate 的改动：Copyright (c) 2026 xm1221，MIT 协议，见 [LICENSE](LICENSE)。
