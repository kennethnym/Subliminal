import 'dart:convert';
import 'dart:io';

import 'package:ast_analyzer/ast_analyzer.dart';
import 'package:ast_analyzer/src/find_tests.dart';
import 'package:ast_analyzer/src/target.dart';

/// Defines targets the analyzer should find.
enum _Target {
  /// Find where the main method of the project is
  main,

  /// Find where all the tests of the projects are.
  tests,
}

/// Finds where targets are in the given file
/// Usage: ast_analyzer <target> <file-path>
///   - target: main | tests
///     - main: find where the main method is
///     - tests: find where all the tests are
///   - file-path: full path to the file being analyzedd
void main(List<String> arguments) {
  try {
    final targetType = _Target.values.byName(arguments.first);
    final targets = <Target>[];
    switch (targetType) {
      case _Target.main:
        final target = findMain(forFile: arguments[1]);
        if (target != null) {
          targets.add(target);
        }
        break;

      case _Target.tests:
        targets.addAll(findTests(forFile: arguments[1]));
        break;
    }

    stdout.writeln(jsonEncode(targets));
  } catch (ex) {}
}
