class Task {
  final String assignee;
  final String description;

  Task({required this.assignee, required this.description});

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      assignee: json['assignee'],
      description: json['description'],
    );
  }
}
