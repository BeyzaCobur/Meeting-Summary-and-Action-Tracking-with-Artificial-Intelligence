import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import '../models/meeting.dart';
import '../providers/meeting_provider.dart';

Future<void> generateSummary(BuildContext context, Meeting meeting) async {
  final text = meeting.transcript.join(" ");

  final response = await http.post(
    Uri.parse("http://127.0.0.1:8000/summarize"),
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({"text": text}),
  );

  if (response.statusCode == 200) {
    final decodedUtf8 = utf8.decode(response.bodyBytes);
    final data = jsonDecode(decodedUtf8);

    final summary = data["summary"]?.toString();
    if (summary != null && summary.isNotEmpty) {
      Provider.of<MeetingProvider>(context, listen: false)
          .updateSummary(meeting.id, summary);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("⚠️ Özet boş döndü.")),
      );
    }
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Hata: ${response.statusCode}")),
    );
  }
}
