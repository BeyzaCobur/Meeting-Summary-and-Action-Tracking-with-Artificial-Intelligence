import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;

Future<void> uploadFile(String filePath) async {
  final file = File(filePath);
  final uri = Uri.parse('http://127.0.0.1:8000/uploads');

  final request = http.MultipartRequest('POST', uri);

  // Dosya verisini byte olarak oku
  final Uint8List fileBytes = await file.readAsBytes();

  // Dosyayı ByteStream üzerinden ekle
  request.files.add(
    http.MultipartFile.fromBytes(
      'file', // field name
      fileBytes,
      filename: file.uri.pathSegments.last, // dosya adı
    ),
  );

  try {
    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    print("HTTP response: ${response.statusCode} ${response.body}");
  } catch (e) {
    print("HTTP error: $e");
  }
}
