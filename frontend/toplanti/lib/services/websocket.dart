import 'package:flutter/material.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  final String url;
  late WebSocketChannel _channel;

  WebSocketService({required this.url});

  void connect() {
    _channel = IOWebSocketChannel.connect(Uri.parse(url));
    debugPrint('WebSocket bağlandı: $url');
  }

  Stream get stream => _channel.stream;

  void sendMessage(String message) {
    _channel.sink.add(message);
    debugPrint('Gönderilen mesaj: $message');
  }

  void disconnect() {
    _channel.sink.close();
    debugPrint('WebSocket bağlantısı kapandı.');
  }
}
