import 'dart:io';

import 'package:analyzer/dart/analysis/utilities.dart';
import 'package:analyzer/dart/ast/ast.dart';

import 'target.dart';

Target? findMain({
  String? inFile,
  String? inSource,
}) {
  final fileContent =
      inFile != null ? File(inFile).readAsStringSync() : inSource;
  if (fileContent == null) return null;

  final ast = parseString(content: fileContent);

  try {
    final main = ast.unit.declarations
        .whereType<FunctionDeclaration>()
        .firstWhere((declaration) => declaration.name.name == 'main');

    return Target(
      file: inFile,
      offset: main.beginToken.offset,
      name: 'main',
      type: TargetType.method,
    );
  } catch (_) {
    return null;
  }
}
