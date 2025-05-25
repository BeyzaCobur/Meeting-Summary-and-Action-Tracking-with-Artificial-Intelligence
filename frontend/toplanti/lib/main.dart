import 'package:flutter/material.dart';
import 'package:toplanti/screens/meeting_list_screen.dart';
import 'package:toplanti/widgets/record.dart';
import 'package:provider/provider.dart';
import 'providers/meeting_provider.dart';

import 'package:toplanti/styles/sizes.dart';
import 'package:toplanti/styles/theme.dart';
import 'package:toplanti/widgets/transcript_list.dart';
import 'package:toplanti/services/websocket.dart';


void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => MeetingProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: const MeetingListScreen(),
    );
  }
}


class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final GlobalKey<TranscriptListState> _transcriptListKey = GlobalKey<TranscriptListState>();


   late WebSocketService webSocketService;


  @override
void initState() {
  super.initState();

  webSocketService = WebSocketService(url: 'ws://127.0.0.1:8000/ws');
  webSocketService.connect();

  webSocketService.stream.listen((message) {
    debugPrint("WebSocket mesajı: $message");
    _transcriptListKey.currentState?.refresh();
  });
}


  @override
  void dispose() {
    webSocketService.disconnect();
    super.dispose();
  }






  // int _counter = 0;

  // void _incrementCounter() {
  //   setState(() {
  //     // This call to setState tells the Flutter framework that something has
  //     // changed in this State, which causes it to rerun the build method below
  //     // so that the display can reflect the updated values. If we changed
  //     // _counter without calling setState(), then the build method would not be
  //     // called again, and so nothing would appear to happen.
  //     _counter++;
  //   });
  // }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Stack(
      children: [
        Row(
          children: [
            Column(
              children: [
                RecordWidget()

              ],
            ),
            Column(
              children: [
                SizedBox(
                  height: context.screenHeight*0.9,
                  width: context.screenWidth*0.33,
                  child: TranscriptList(key: _transcriptListKey),
                )
              ],
            )
          ],
        )
      ],
    );

  }
}
