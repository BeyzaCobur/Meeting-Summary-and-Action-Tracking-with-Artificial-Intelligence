import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import '../models/meeting.dart';
import '../providers/meeting_provider.dart';

Future<void> generateTasks(BuildContext context, Meeting meeting) async {
  final text = meeting.transcript.join(" ");

  final response = await http.post(
    Uri.parse("http://127.0.0.1:8000/extract_tasks"),
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"text": text}),
  );

  if (response.statusCode == 200) {
    final decodedUtf8 = utf8.decode(response.bodyBytes);
    final data = jsonDecode(decodedUtf8);

    final tasks = data["tasks"];
    if (tasks is List) {
      Provider.of<MeetingProvider>(context, listen: false)
          .updateTasks(meeting.id, tasks.cast<Map<String, dynamic>>());
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Görev verisi okunamadı.")),
      );
    }
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Görevler alınamadı: ${response.statusCode}")),
    );
  }
}


