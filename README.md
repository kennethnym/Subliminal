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

### Flutter projects

To create a build system for Flutter projects, Go to `Tools -> Build system -> New build system...`. A new file will be created. Name it `flutter.sublime-build`, then add the following:

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

## To-do

- [ ] Dart/Flutter commands
    - [x] `pub get`
    - [x] `pub add`
    - [x] `fluter clean`
    - [x] `flutter run`
- [x] Hot reload/Restart
- [ ] Open ios/android folder in Xcode/Android Studio
- [x] Select device
- [x] Add dependency
