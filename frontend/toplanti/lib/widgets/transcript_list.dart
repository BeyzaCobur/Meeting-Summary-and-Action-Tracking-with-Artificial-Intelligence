import 'package:flutter/material.dart';
import '../models/transcripts.dart';
import '../services/transcript_service.dart';

class TranscriptList extends StatefulWidget {
  const TranscriptList({Key? key}) : super(key: key);

  @override
  State<TranscriptList> createState() => TranscriptListState();
}

class TranscriptListState extends State<TranscriptList> {
  late Future<List<Transcript>> _transcripts;

  @override
  void initState() {
    super.initState();
    _loadTranscripts();
  }

  void _loadTranscripts() {
    _transcripts = TranscriptService.fetchTranscripts();
  }

  void refresh() {
    setState(() {
      _loadTranscripts();
    });
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Transcript>>(
      future: _transcripts,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Text(
            "Hata: ${snapshot.error}",
            style: Theme.of(context).textTheme.bodyMedium,
          );
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Text(
            "Henüz transkript yok.",
            style: Theme.of(context).textTheme.bodyMedium,
          );
        }

        final transcripts = snapshot.data!;
        return ListView.builder(
          itemCount: transcripts.length,
          itemBuilder: (context, index) {
            final t = transcripts[index];
            final cleanedTitle = t.dosyaAdi.replaceAll('.wav', '');

            return GestureDetector(
              onTap: () {
                showDialog(
                  context: context,
                  builder: (_) => Dialog(
                    backgroundColor: Theme.of(context).cardTheme.color,
                    child: TranscriptDetay(transcript: t),
                  ),
                );
              },
              child: Card(
                elevation: 2,
                margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 8),
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                  child: Text(
                    cleanedTitle,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          decoration: TextDecoration.underline,
                        ),
                  ),
                ),
              ),
            );
          },
        );

      },
    );
  }
}

class TranscriptDetay extends StatelessWidget {
  const TranscriptDetay({super.key, required this.transcript});

  final Transcript transcript;

  @override
  Widget build(BuildContext context) {
    final cleanedTitle = transcript.dosyaAdi.replaceAll('.wav', '');

    return Padding(
      padding: const EdgeInsets.all(24),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              cleanedTitle,
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 12),
            Text(
              transcript.icerik,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
}
