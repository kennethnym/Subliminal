/// Describes the location of a target in a project.
class Target {
  /// The path to the file that the target is in.
  final String file;

  /// Number of offset from the first character of the file this target has.
  final int offset;

  /// The name of this target.
  /// Can be name of a method, or name of a test block.
  final String name;

  const Target({
    required this.file,
    required this.offset,
    required this.name,
  });

  Map<String, dynamic> toJson() => {
        'file': file,
        'offset': offset,
        'name': name,
      };
}
