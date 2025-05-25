import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/transcripts.dart';

class TranscriptService {
  static const String baseURL = 'http://127.0.0.1:8000';

  static Future<List<Transcript>> fetchTranscripts() async {
    final response = await http.get(Uri.parse('$baseURL/transcripts'));

    if (response.statusCode == 200) {
      final decoded = json.decode(response.body);
      print('Sunucudan gelen JSON: $decoded');

      final List<dynamic> jsonList = decoded['transkript'];
      print('Çekilen transcript listesi: $jsonList');

      

      return jsonList.map((json) => Transcript.fromJson(json)).toList();
    } else {
      throw Exception('Transkriptler alınamadı: ${response.statusCode}');
    }
  }

static Future<bool> transcribeAudio(File file, String meetingId) async {
  final request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseURL/transcribe'),
  );

  request.fields['meeting_id'] = meetingId;
  request.files.add(await http.MultipartFile.fromPath('file', file.path));

  final streamedResponse = await request.send();
  final response = await http.Response.fromStream(streamedResponse);

  if (response.statusCode == 200) {
    final Map<String, dynamic> decoded = json.decode(response.body);
    return decoded['status'] == 'success';
  }
  return false;
}


}
