import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:file_picker/file_picker.dart';

import 'bottom.dart';

class Trans extends StatefulWidget {
  const Trans({Key? key}) : super(key: key);

  @override
  _TransState createState() => _TransState();
}

class _TransState extends State<Trans> {
  late WebViewController _webViewController;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        title: const Text(
          'Translate',
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: const Color.fromARGB(255, 0, 0, 0),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: WebView(
              initialUrl: 'translate url',
              javascriptMode: JavascriptMode.unrestricted,
              onWebViewCreated: (WebViewController webViewController) {
                _webViewController = webViewController;
              },
              javascriptChannels: <JavascriptChannel>{
                JavascriptChannel(
                  name: 'FilePicker',
                  onMessageReceived: (JavascriptMessage message) async {
                    FilePickerResult? result = await FilePicker.platform.pickFiles();
                    
                    if (result != null) {
                      PlatformFile file = result.files.first;
                      print('File selected: ${file.name}');
                    }
                  },
                ),
              },
              onPageStarted: (String url) {},
              onPageFinished: (String url) {},
              onWebResourceError: (WebResourceError error) {
                print("Web resource error: $error");
              },
            ),
          ),
        ],
      ),
      bottomNavigationBar: MyBottomNavBar(currentIndex: 1),
    );
  }
}



