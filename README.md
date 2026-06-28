# Klyx Plugin Registry

Community plugin registry for [Klyx](https://klyx-dev.github.io) - a modern code editor for Android.

## For Plugin Authors

### Prerequisites

1. A `plugin.json` at the root of your project (see [sample]())
2. The `io.github.klyx-dev.plugin` Gradle plugin applied

### Build

```bash
./gradlew klyxBundle
# -> build/klyx/my-plugin.klyx
```

### Publish

**Via web UI (recommended):** Go to https://klyx-dev.github.io/publish and drag your `.klyx` file.

**Via GitHub PR:**
1. [Fork](https://github.com/klyx-dev/plugins/fork) the registry repo
2. Add your `.klyx` file to the `incoming/` directory
3. Create a pull request
4. CI validates the bundle and auto-merges

### Bundle format

A `.klyx` file is a gzipped tarball containing:

| Entry | Required | Description |
|-------|----------|-------------|
| `plugin.json` | ✅ | Plugin metadata (id, version, name, etc.) |
| `plugin.apk` | ✅ | The compiled APK |
| `icon.png` | ❌ | Store icon (512×512 recommended) |
| `readme.md` | ❌ | Plugin description / docs |
| `changelog.md` | ❌ | Version changelog |

## Structure

```
plugins/
  index.json        <- Auto-generated registry
  {plugin-id}/
    metadata.json   <- Extracted plugin.json
    icon.png        <- Extracted plugin icon
    readme.md       <- Extracted readme
    changelog.md    <- Extracted changelog
    {version}.klyx  <- Bundle files
incoming/           <- Drop .klyx files here (via PR)
```

## License

GPL-3.0
