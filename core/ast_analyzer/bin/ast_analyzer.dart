import 'dart:convert';
import 'dart:io';

import 'package:args/args.dart';
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
  final argParser = ArgParser()
    ..addOption('type', allowed: ['main', 'tests'])
    ..addOption('source', defaultsTo: null)
    ..addOption('file', defaultsTo: null);

  final args = argParser.parse(arguments);

  try {
    final targetType = _Target.values.byName(args['type']);
    final targets = <Target>[];
    switch (targetType) {
      case _Target.main:
        if (args['file'] != null) {
          final target = findMain(inFile: args['file']);
          if (target != null) {
            targets.add(target);
          }
        } else if (args['source'] != null) {
          final target = findMain(inSource: args['source']);
          if (target != null) {
            targets.add(target);
          }
        }

        break;

      case _Target.tests:
        if (args['file'] != null) {
          targets.addAll(findTests(inFile: args['file']));
        } else if (args['source'] != null) {
          targets.addAll(findTests(inSource: args['source']));
        }
        break;
    }

    stdout.writeln(jsonEncode(targets));
  } catch (ex) {
    print('ex $ex');
  }
}
