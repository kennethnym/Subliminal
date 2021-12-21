# Subliminal [Work in progress!]

A Sublime Text 4 plugin that adds support for Dart/Flutter projects. This plugin adds commands for working with Dart/Flutter projects,
and **does not** provide syntax/autocompletion support.

## Installation

1. If you haven't already, please install [LSP](https://lsp.sublimetext.io/language_servers/) and [LSP-Dart](https://github.com/sublimelsp/LSP-Dart) first. They will provide autocompletion for your Dart code.
2. Define `FLUTTER_ROOT` (for Flutter projects) and/or `DART_SDK` (for Dart projects) in the settings file for `LSP-Dart`, under the `"env"` key.
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
    "target": "flutter_run",
    "as": ""
}
```

## To-do

- [ ] Dart/Flutter commands
    - [x] `pub get`
    - [x] `pub add`
    - [x] `fluter clean`
    - [x] `flutter run`
- [ ] Hot reload/Restart
- [ ] Open ios/android folder in Xcode/Android Studio
- [ ] Select device
- [ ] Add dependency
