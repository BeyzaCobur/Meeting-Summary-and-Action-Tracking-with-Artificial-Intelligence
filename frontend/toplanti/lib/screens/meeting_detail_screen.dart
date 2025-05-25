import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:toplanti/services/ozet.dart';
import 'package:toplanti/services/task_service.dart';
import '../models/meeting.dart';
import '../providers/meeting_provider.dart';

class MeetingDetailScreen extends StatelessWidget {
  final Meeting meeting;

  const MeetingDetailScreen({super.key, required this.meeting});

  @override
  Widget build(BuildContext context) {
    final updatedMeeting = context.watch<MeetingProvider>().getById(meeting.id);

    return Scaffold(
      appBar: AppBar(title: Text(updatedMeeting?.title ?? "Toplantı")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 📅 Tarih ve süre
              Text("📅 Tarih: ${updatedMeeting?.date.toLocal().toString().split('.')[0] ?? '-'}"),
              Text("⏱ Süre: ${updatedMeeting?.duration.inMinutes ?? 0} dakika"),
              const SizedBox(height: 24),

              // 🎤 Transkript
              Text("🎤 Transkript", style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 8),
              (updatedMeeting?.transcript.isEmpty ?? true)
                  ? const Text("Henüz transkript yok.")
                  : Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: updatedMeeting!.transcript
                          .map((line) => Text("• $line"))
                          .toList(),
                    ),

              const SizedBox(height: 32),

              // 🧠 Özet
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text("🧠 Toplantı Özeti", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  ElevatedButton(
                    onPressed: () => generateSummary(context, meeting),
                    child: const Text("Oluştur"),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(updatedMeeting?.summary ?? "Henüz oluşturulmadı."),

              const SizedBox(height: 32),

              // ✅ Görevler
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text("✅ Görev Listesi", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  ElevatedButton(
                    onPressed: () async {
                      await generateTasks(context, updatedMeeting!);
                    },
                    child: const Text("Görevleri Oluştur"),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              (updatedMeeting?.tasks == null || updatedMeeting!.tasks!.isEmpty)
                  ? const Text("Henüz oluşturulmadı.")
                  : Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: updatedMeeting.tasks!
                          .map((task) => Row(
                                children: [
                                  const Icon(Icons.check_box_outline_blank, size: 18),
                                  const SizedBox(width: 6),
                                  Expanded(
                                    child: Text("${task['assignee']}: ${task['description']}"),
                                  ),
                                ],
                              ))
                          .toList(),
                    ),
            ],
          ),
        ),
      ),
    );
  }
}
