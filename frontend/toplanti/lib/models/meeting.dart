import 'package:uuid/uuid.dart';

class Meeting {
  final String id;
  final String title;
  final DateTime date;
  final Duration duration;
  final List transcript;
  String? summary;

  List<Map<String, dynamic>>? tasks;

  // 🧱 Constructor
  Meeting({
    String? id, // Flutter'da üretilebilir ama fromJson'da da kullanılabilir
    required this.title,
    required this.date,
    required this.duration,
    required this.transcript,
    this.summary,
    this.tasks,
  }) : id = id ?? const Uuid().v4(); // 🎯 ID Flutter'da otomatik oluşturulur

  // 🔁 JSON'dan oluşturmak için
  factory Meeting.fromJson(Map<String, dynamic> json) {
    return Meeting(
      id: json['id'], // Backend'den gelen ID'yi al
      title: json['title'],
      date: DateTime.parse(json['start_time']),
      duration: Duration(minutes: (json['duration'] as num).toInt()),
      transcript: [],
      summary: json['summary'],
      tasks: json['tasks'] != null ? List<Map<String, dynamic>>.from(json['tasks']) : null,
    );
  }

  // 🔁 JSON'a çevirmek için (saveToDatabase için)
  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "title": title,
      "start_time": date.toIso8601String(),
      "duration": duration.inMinutes,
      "summary": summary,
      "tasks": tasks,
    };
  }
}
