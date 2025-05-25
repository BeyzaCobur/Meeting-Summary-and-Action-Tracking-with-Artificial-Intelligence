import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:toplanti/widgets/record.dart';
import '../providers/meeting_provider.dart';
import '../screens/meeting_detail_screen.dart';
import '../models/meeting.dart';

class MeetingListScreen extends StatelessWidget {
  const MeetingListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final meetings = context.watch<MeetingProvider>().meetings;

    return Scaffold(
      appBar: AppBar(title: const Text("Toplantılar")),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            // 🎙 Kayıt alanı
            const RecordWidget(),

            const SizedBox(height: 20),

            // 📋 Toplantı listesi
            Expanded(
              child: meetings.isEmpty
                  ? const Center(child: Text("Henüz toplantı yok."))
                  : ListView.builder(
                      itemCount: meetings.length,
                      itemBuilder: (context, index) {
                        final Meeting meeting = meetings[index];

                        return Card(
                          margin: const EdgeInsets.symmetric(vertical: 8),
                          child: ListTile(
                            title: Text(meeting.title),
                            subtitle: Text(
                              "📅 ${meeting.date.toLocal()}   ⏱ ${meeting.duration.inMinutes} dk",
                            ),
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => MeetingDetailScreen(meeting: meeting),
                                ),
                              );
                            },
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
