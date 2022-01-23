enum TargetType {
  method,
  test,
}

/// Describes the location of a target in a project.
class Target {
  /// The path to the file that the target is in.
  /// If this target is not found in a file but rather in a source string, this will be null.
  final String? file;

  /// Number of offset from the first character of the file this target has.
  final int offset;

  /// The name of this target.
  /// Can be name of a method, or name of a test block.
  final String name;

  /// The type of this target
  final TargetType type;

  const Target({
    this.file,
    required this.offset,
    required this.name,
    required this.type,
  });

  Map<String, dynamic> toJson() => {
        'file': file,
        'offset': offset,
        'name': name,
        'type': type.toString().split('.').last,
      };
}
