# MieHexTemplate

[![powered by hexdoc](https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc?label=1)](https://github.com/hexdoc-dev/hexdoc)

A [Copier](https://copier.readthedocs.io) template for **multiloader (Fabric + Forge), Kotlin-based** [Hex Casting](https://github.com/FallingColors/HexMod) addons on **Minecraft 1.20.1** with Architectury, targeting **Hex Casting 0.11.4**.

MieHexTemplate is a fork of [HexDummy v2](https://github.com/FallingColors/hexdummy) by artynova and Falling Colors (MIT). Everything HexDummy does is kept: hexdoc, the CI and release workflows, and the Registrar helpers. On top of that it adds:

- **Hex Casting 0.11.4** and the toolchain it needs: Kotlin 2.2.21, fabric-language-kotlin 1.13.7, KotlinForForge 4.12.0, Architectury Loom 1.9, Gradle 8.11.1.
- An extra example pattern, `Squaring Purification` (`<modid>:square`), to show a minimal `ConstMediaAction`.
- An optional **[MieLib](https://github.com/xm1221/MieLib) + HexCLI** development loop (the `use_mielib` question, default **yes**):
  - MieLib as a Jar-in-Jar dependency on both loaders. Fabric comes from MieLib's GitHub release; Forge is vendored in `libs/`.
  - [hexParse](https://modrinth.com/mod/hexparse) as a **dev-runtime-only** dependency, never shipped.
  - `./gradlew runHexCli -PacceptEula=true`, a headless Fabric dev server with `-Dmielib.hexcli=true`.
  - `scripts/hexcli-check.sh`, which runs `hexcli/examples.tsv` through `hexcli-client -e`. It compares stacks and messages, and reports parse errors (`hexParse: Unknown symbol`) separately from mishaps.
  - `skills/hexcasting/SKILL.md`, a HexCLI / hexParse cheat sheet for humans and AI agents.

  If you answer **no**, none of these files or dependencies are generated.

> [!TIP]
> Don't want to install Copier? A pre-rendered copy with the default answers lives in the GitHub template repo
> [xm1221/MieHexTemplate-Starter](https://github.com/xm1221/MieHexTemplate-Starter). Click *Use this template*, then run
> `python3 rename-mod.py --modid yourmod --package com.example.yourmod --name "Your Mod"`.
> Copier is still the recommended way, because it can later `copier update` your project when this template changes.

> [!TIP]
> If you're writing a Fabric-only or Forge-only mod, you probably don't need this template. Consider using the [Fabric template mod generator](https://fabricmc.net/develop/template/) or [Forge MDK](https://docs.minecraftforge.net/en/1.20.1/gettingstarted/) instead.

## Usage

1. Install the prerequisites:
   - [Git](https://github.com/git-guides/install-git)
   - [uv](https://docs.astral.sh/uv/getting-started/installation/)
   - Any IDE with Java and Kotlin support (recommended: [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/download/?section=windows))
2. Create, clone, and enter a **new** GitHub repo. You don't need to use any other project templates (e.g. IntelliJ's Minecraft mod template) with MieHexTemplate.
> [!CAUTION]
> **Do not** fork/clone/copy this repo directly.
3. From the repo root, run this command to copy the template, then follow the prompts to set it up:
   ```sh
   uvx copier copy gh:xm1221/MieHexTemplate .
   ```
4. Set up your Python environment and lockfile:
   ```sh
   uv sync

   .\.venv\Scripts\activate   # Windows
   . .venv/bin/activate.fish  # fish
   source .venv/bin/activate  # everything else
   ```
5. Look through the generated project to make sure everything looks good, then add, commit, and push the generated files (including `uv.lock`):
   ```
   git add .
   git update-index --chmod=+x gradlew
   git commit -m "Set up mod template"
   git push
   ```
6. Follow the [hexdoc setup instructions](https://hexdoc.hexxy.media/docs/guides/deployment/github-pages) for GitHub Pages.
7. Set up the release workflow:
   1. In your GitHub repository settings, create two new environments called `pypi` and `curseforge-modrinth`.
   2. Add the following environment secrets (**not** environment variables) to the `curseforge-modrinth` environment:
      - `CURSEFORGE_TOKEN`: Generate a new [CurseForge API token](https://authors-old.curseforge.com/account/api-tokens).
      - `MODRINTH_TOKEN`: Generate a new [Modrinth PAT](https://modrinth.com/settings/pats) with the `Create versions` scope.
   3. [Create a PyPI pending publisher](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) with the following settings:
      - PyPI Project Name: The `project.name` value in your `pyproject.toml` (eg. `hexdoc-hexcasting`)
      - Owner: Your GitHub username
      - Repository name: Your GitHub repository name
      - Workflow name: `release.yml`
      - Environment name: `pypi`
   4. If you'd like to publish your mod to https://maven.hexxy.media, [follow these instructions](https://gist.github.com/object-Object/f9988135bec5cef653c668712954f429) to set it up.
   5. When your mod is ready, [manually trigger a release](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow) through the Actions tab on GitHub.

Further instructions TODO - look at [HexDebug](https://github.com/object-Object/HexDebug) or [IoticBlocks](https://github.com/object-Object/IoticBlocks) for examples, since this template is based heavily on those mods.

## HexCLI development loop (`use_mielib = yes`)

```sh
./gradlew runHexCli -PacceptEula=true           # headless Fabric server, fabric/run/hexcli (you accept the Minecraft EULA)
./scripts/hexcli-check.sh --accept-eula         # starts the server if needed, runs hexcli/examples.tsv, stops the server
./scripts/hexcli-check.sh -f hexcli/examples-broken.tsv   # intentionally failing cases: one parse error, one mishap
```

`hexcli-check.sh` downloads `hexcli-client.jar` from MieLib's `hexcli-v1.0.0` release and checks it against `SHA256SUMS`. Each row of `hexcli/examples.tsv` is `name<TAB>code<TAB>outcome<TAB>stack<TAB>message-regex`, where the outcome is one of `OK`, `PARSE_ERROR`, `MISHAP` or `HEXCLI_ERROR`.

## Starter repo and the publish workflow

[`.github/workflows/publish-starter.yml`](.github/workflows/publish-starter.yml) renders this template with the default answers (`modid = miehexaddon`), builds it, and tests [`starter/rename-mod.py`](starter/rename-mod.py) on a copy. It then pushes the result as a single commit to the template repo `xm1221/MieHexTemplate-Starter`. That push replaces the starter's history.

- Triggers: tags `v*`, or a manual run from the Actions tab. A manual run takes the inputs `target_repo`, `target_branch` and `dry_run`.
- Required secret: **`STARTER_REPO_TOKEN`**. This is a fine-grained PAT with *Contents: read and write* on the starter repo. The secret name lives in the workflow's `TOKEN_SECRET_NAME` env.

## Resources

Upstream HexDummy example projects (without the MieHexTemplate changes):

- [example/v2/mojmap](https://github.com/FallingColors/hexdummy/tree/example/v2/mojmap)
- [example/v2/yarn](https://github.com/FallingColors/hexdummy/tree/example/v2/yarn)

The following repository contains an example of a project generated using HexDummy, including GitHub Actions workflow runs and a hexdoc web book:

- https://github.com/object-Object/HexDummyExample

## FAQ

### Why isn't this a template repository / why shouldn't I fork this repo to set up my mod?

MieHexTemplate (like HexDummy) uses [Copier](https://copier.readthedocs.io), a Python app for generating projects from *parameterized* templates. When you run `uvx copier copy`, Copier clones this repository, prompts you for some values, then fills those values into many placeholders in the template, making a customized project with no placeholder values for you to have to replace by hand.

As a consequence, this repository by itself is *not* a working Minecraft mod - if you look in the [template](./template) directory, you'll see a lot of `.jinja` files with placeholders that still need to be filled in.

### How do I add dependencies?

- Maven repositories: `buildSrc/src/main/kotlin/java.gradle.kts`
- Dependency definitions: `gradle/libs.versions.toml` ([Gradle docs](https://docs.gradle.org/current/userguide/version_catalogs.html#sec::toml-dependencies-format))
- Gradle dependency configurations: `{common,fabric,forge}/build.gradle.kts` (depending which platform you need it on)
- hexdoc dependencies: `pyproject.toml` and `doc/hexdoc.toml` (remember to run `uv sync` to update `uv.lock` after changing)
- Local JAR dependency files: `libs/`
- Maven repositories for Gradle plugins: `settings.gradle.kts`
- Maven repositories and Gradle dependency configurations specifically for Gradle plugins used by the convention plugins in `buildSrc`: `buildSrc/build.gradle.kts`

### Why is the release workflow triggered manually?

Minecraft mod releases tend to be brittle. HexDummy's release workflow includes separate inputs for each platform your mod is released to, so if some of them fail but others succeed, you can manually fix and re-release just the failing parts, rather than having to push a new tag or commit and release everything again.

### What's a (ModName)Registrar? Why can't I use Architectury's DeferredRegister?

Architectury's DeferredRegister [does not work with modded registries](https://github.com/architectury/architectury-api/issues/513). It's also somewhat unergonomic to use in Kotlin (in my opinion). So, HexDummy generates a Registrar base class that you can use to register things in all registries, vanilla or modded.

To add a registrar for a registry, [create an `object` subclassing the registrar](https://github.com/object-Object/HexDummyExample/blob/a7d8d5b58bd018a62456e4653fe46ba3eb22bc69/common/src/main/kotlin/io/github/objectobject/hexdummyexample/registry/HexdummyexampleActions.kt#L11-L14), and pass  the ResourceKey of the registry and a callback that returns the actual registry to the superclass. (A callback is used to avoid initializing the registry too early on Forge.) Add the subclass to the [initRegistries call](https://github.com/object-Object/HexDummyExample/blob/a7d8d5b58bd018a62456e4653fe46ba3eb22bc69/common/src/main/kotlin/io/github/objectobject/hexdummyexample/Hexdummyexample.kt#L21) in your common mod initializer.

Registering things with a HexDummy Registrar generally looks like this:

```kt
val REGISTERED_THING = register("registered_thing") { ThingConstructor("parameters") }
```

`register` takes a callback for the same reason as the registry object: to avoid constructing the instance too early on Forge. The string is used as the path for a ResourceLocation, with your mod id as the namespace.

The value returned by `register` is an [`Entry<V>`](https://github.com/object-Object/HexDummyExample/blob/a7d8d5b58bd018a62456e4653fe46ba3eb22bc69/common/src/main/kotlin/io/github/objectobject/hexdummyexample/registry/HexdummyexampleRegistrar.kt#L50). You can use this to access the registered thing's id (`.id`) or ResourceKey (`.key`), and when you're sure registration has finished, the actual registered instance (`.value`).

For a more concrete example, the template comes with an [example for registering patterns](https://github.com/object-Object/HexDummyExample/blob/a7d8d5b58bd018a62456e4653fe46ba3eb22bc69/common/src/main/kotlin/io/github/objectobject/hexdummyexample/registry/HexdummyexampleActions.kt), and HexDebug has [several more examples](https://github.com/object-Object/HexDebug/tree/5db5f78f5489863e2c20a3df472571a984877b7d/Common/src/main/kotlin/gay/object/hexdebug/registry) for various types of registries.

## TODO

- Finish adding Yarn support.
- See if there's a better way to download dependencies for CI tests than just manually listing Modrinth URLs.
- Improve documentation.
- Investigate https://github.com/headlesshq/mc-server-test more. From the logs, it seems like the Fabric server test might not actually be loading any mods?
- Fix the CI tests in this repository.
- Figure out how to publish to CurseForge/Modrinth/GitHub without having to build the mod again.

## Credits and license

- [HexDummy v2](https://github.com/FallingColors/hexdummy), Copyright (c) 2025 artynova, Falling Colors. MIT. This repository is a fork of it.
- [MieLib](https://github.com/xm1221/MieLib) (MIT): HexCLI, the vendored Forge jar and `skills/hexcasting/SKILL.md`.
- MieHexTemplate changes: Copyright (c) 2026 xm1221. MIT. See [LICENSE](LICENSE).
