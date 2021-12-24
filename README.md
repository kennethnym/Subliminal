# Subliminal [Work in progress!]

A Sublime Text 4 plugin that adds support for Dart/Flutter projects. This plugin adds commands for working with Dart/Flutter projects,
and **does not** provide syntax/autocompletion support.

## Installation

1. If you haven't already, please install [LSP](https://lsp.sublimetext.io/language_servers/) and [LSP-Dart](https://github.com/sublimelsp/LSP-Dart) first. They will provide autocompletion for your Dart code.
2. This plugin will try to detect the path to the Flutter and Dart SDK. To define the path manually, define `FLUTTER_ROOT` (for Flutter projects) and/or `DART_SDK` (for Dart projects) in the settings file for `LSP-Dart`, under the `"env"` key.
    - `FLUTTER_ROOT` should be the path to the Flutter SDK
    - `DART_SDK` should be the path to the Dart SDK
    - If you have per-project settings, define them in the project settings file instead.
3. Install this plugin through Package Control.

## Integration with Sublime Text's build system.

This plugin allows Dart/Flutter projects to be run through Sublime Text's build system.

### Running Dart projects

To create a build system for running Dart projects, go to `Tools -> Build system -> New build system...`. A new file will be created. Name it `dart.sublime-build`, then add the following:

```json
{
    "name": "<a name for this build system>",
    "selector": "source.dart",
    "target": "dart_run",
    "cancel": {
        "kill": true,
    },
    // additional arguments passed to 'flutter run' as a list of strings
    "args": ["--arg1", "--arg2"],
}
```

### Running Flutter projects

To create a build system for running Flutter projects, go to `Tools -> Build system -> New build system...`. A new file will be created. Name it `flutter.sublime-build`, then add the following:

```json
{
    "name": "<a name for this build system>"
    "selector": "source.dart"
    "target": "flutter_run",
    "cancel": {
        "kill": true,
    },
    // additional arguments passed to 'flutter run' as a list of strings
    "args": ["--arg1", "--arg2"],
}
```

### Per-project build system

To have different build systems for different Sublime projects, instead of making a new build system through the menu, add the above JSON objects
to the list under the `"build_systems"` key, in the `<project-name>.sublime-project` file:

```json
{
    "folders": [/*...*/],
    "build_systems":
    [
        /* Add build system JSON config here */
        {
            "name": "Run my project"
            "selector": "source.dart"
            "target": "flutter_run",
            "cancel": {
                "kill": true,
            },
            // additional arguments passed to 'flutter run' as a list of strings
            "args": ["--no-sound-null-safety"],
        }
    ]
}
```

## To-do

- [ ] Dart/Flutter commands
    - [x] `pub get`
    - [x] `pub add`
    - [x] `fluter clean`
    - [x] `flutter run`
    - [x] `dart run`
- [x] Hot reload/Restart
- [x] Open ios/android folder in Xcode/Android Studio
- [x] Select device
- [x] Add dependency
