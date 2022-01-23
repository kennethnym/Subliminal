import 'dart:io';

import 'package:analyzer/dart/analysis/utilities.dart';
import 'package:analyzer/dart/ast/ast.dart';

import 'target.dart';

Iterable<Target> findTests({String? inFile, String? inSource}) {
  final source = inFile != null ? File(inFile).readAsStringSync() : inSource;
  if (source == null) return [];

  final ast = parseString(content: source);

  final mainBlock = ast.unit.declarations
      .whereType<FunctionDeclaration>()
      .firstWhere((declaration) => declaration.name.name == 'main')
      .functionExpression
      .body
      .childEntities
      .firstWhere((child) => child is Block) as Block;

  return _findTestNodes(mainBlock, inFile);
}

Iterable<Target> _findTestNodes(Block block, String? file) {
  final nodes = block.statements
      .whereType<ExpressionStatement>()
      .map((statement) => statement.expression)
      .whereType<MethodInvocation>()
      .where(_isTestNode);

  return nodes
      .map((invocation) => Target(
            file: file,
            offset: invocation.beginToken.offset,
            name: (invocation.argumentList.arguments.first as StringLiteral)
                .stringValue!,
            type: TargetType.test,
          ))
      .followedBy(nodes.fold(<Target>[], (arr, node) {
        final testBody = node.argumentList.arguments[1] as FunctionExpression;
        final block = testBody.body.childEntities
            .firstWhere((child) => child is Block) as Block;
        return arr.followedBy(_findTestNodes(block, file));
      }));
}

bool _isTestNode(MethodInvocation invocation) {
  if (!(invocation.methodName.name == 'group' ||
      invocation.methodName.name == 'test')) {
    return false;
  }

  final args = invocation.argumentList.arguments;
  final firstArg = args[0];
  final secondArg = args[1];
  if (firstArg is! StringLiteral || secondArg is! FunctionExpression) {
    return false;
  }

  return firstArg.stringValue != null;
}
