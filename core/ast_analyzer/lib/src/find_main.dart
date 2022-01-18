import 'dart:io';

import 'package:analyzer/dart/analysis/utilities.dart';
import 'package:analyzer/dart/ast/ast.dart';

import 'target.dart';

Target? findMain({required String forFile}) {
  final fileContent = File(forFile).readAsLinesSync();

  final ast = parseString(content: fileContent.join('\n'));

  try {
    final main = ast.unit.declarations
        .whereType<FunctionDeclaration>()
        .firstWhere((declaration) => declaration.name.name == "main");

    return Target(
      file: forFile,
      offset: main.beginToken.charOffset,
      name: 'main',
    );
  } catch (_) {
    return null;
  }
}
