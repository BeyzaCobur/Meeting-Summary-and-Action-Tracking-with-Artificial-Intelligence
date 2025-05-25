import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/meeting.dart';

class MeetingService {
  static const String baseURL = 'http://127.0.0.1:8000'; // ya da IP

  static Future<Meeting> saveToDatabase(Meeting meeting) async {
    final response = await http.post(
      Uri.parse('$baseURL/meetings/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(meeting.toJson()),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      final Map<String, dynamic> json = jsonDecode(response.body);
      return Meeting.fromJson(json);
    } else {
      throw Exception('Toplantı veritabanına kaydedilemedi: ${response.body}');
    }
  }
}
