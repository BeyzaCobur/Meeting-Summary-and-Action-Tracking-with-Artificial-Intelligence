import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:uuid/uuid.dart'; // ✅ UUID üretmek için
import '../models/meeting.dart';
import '../providers/meeting_provider.dart';
import '../services/transcript_service.dart';
import '../services/meeting_service.dart';

class RecordWidget extends StatefulWidget {
  const RecordWidget({super.key});

  @override
  State<RecordWidget> createState() => _RecordWidgetState();
}

class _RecordWidgetState extends State<RecordWidget> {
  bool isRecording = false;
  Process? _ffmpegProcess;
  String? recordingPath;
  DateTime? _startTime;

  Future<String> getRecordingPath() async {
    final now = DateTime.now();
    final formatted = '${now.year}-${now.month}-${now.day}_${now.hour}-${now.minute}-${now.second}';
    final dir = Directory(".");
    return '${dir.path}/kayit_$formatted.wav';
  }

  Future<void> startRecording() async {
    _startTime = DateTime.now();
    final path = await getRecordingPath();

    _ffmpegProcess = await Process.start(
      'ffmpeg',
      ['-y', '-f', 'alsa', '-i', 'hw:1,0', path],
      mode: ProcessStartMode.detachedWithStdio,
    );

    setState(() {
      isRecording = true;
      recordingPath = path;
    });
  }

  Future<void> stopRecording() async {
    if (_ffmpegProcess != null) {
      _ffmpegProcess!.kill(ProcessSignal.sigterm);
    }

    final endTime = DateTime.now();
    final duration = endTime.difference(_startTime!);

    final title = await _askMeetingTitle(context);
    if (title != null && title.isNotEmpty) {
      final newMeeting = Meeting(
        id: const Uuid().v4(),// ✅ ID Flutter'da oluşturuluyor
        title: title,
        date: _startTime!,
        duration: duration,
        transcript: [],
      );

      try {
        // ✅ Backend'e toplantı kaydet
        final createdMeeting = await MeetingService.saveToDatabase(newMeeting);

        // ✅ State'e ekle
        Provider.of<MeetingProvider>(context, listen: false).addMeeting(createdMeeting);

        // ✅ Transcribe gönder
        await TranscriptService.transcribeAudio(File(recordingPath!), createdMeeting.id);

        print("📤 Transcribe gönderiliyor:");
        print("Meeting ID: ${createdMeeting.id}");
        print("Dosya: $recordingPath");

      } catch (e) {
        print("❌ Kayıt veya transcribe hatası: $e");
      }
    }

    if (mounted) {
      setState(() {
        isRecording = false;
      });
    }
  }

  Future<String?> _askMeetingTitle(BuildContext context) async {
    final controller = TextEditingController();

    return showDialog<String>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Toplantı Başlığı'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(hintText: 'Örn: Haftalık Planlama'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("İptal")),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, controller.text.trim()),
            child: const Text("Kaydet"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey[850],
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          ElevatedButton.icon(
            onPressed: isRecording ? null : startRecording,
            icon: const Icon(Icons.mic),
            label: const Text("Toplantıya Başla"),
          ),
          ElevatedButton.icon(
            onPressed: isRecording ? stopRecording : null,
            icon: const Icon(Icons.stop),
            label: const Text("Kaydı Bitir"),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
          ),
        ],
      ),
    );
  }
}
