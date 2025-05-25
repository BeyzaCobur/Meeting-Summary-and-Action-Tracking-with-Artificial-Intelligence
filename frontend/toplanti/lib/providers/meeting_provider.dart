import 'package:flutter/material.dart';
import '../models/meeting.dart';
import '../services/task_service.dart';
import '../models/task_model.dart';

class MeetingProvider with ChangeNotifier {
  final List<Meeting> _meetings = [];


  List<Meeting> get meetings => _meetings;

  void addMeeting(Meeting meeting) {
    _meetings.add(meeting);
    notifyListeners();
  }

  Meeting? getById(String id) {
    try {
      return _meetings.firstWhere((m) => m.id == id);
    } catch (_) {
      return null;
    }
  }

  void updateSummary(String id, String summary) {
    final meeting = getById(id);
    if (meeting != null) {
      meeting.summary = summary;
      notifyListeners();
    }
  }

  void updateTasks(String id, List<Map<String, dynamic>> tasks) {
  final meeting = getById(id);
  if (meeting != null) {
    meeting.tasks = tasks;
    notifyListeners();
  }
}

}
