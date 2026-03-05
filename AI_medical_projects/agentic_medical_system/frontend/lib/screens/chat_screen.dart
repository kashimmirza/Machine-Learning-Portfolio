import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:animate_do/animate_do.dart';

class ChatScreen extends StatefulWidget {
  final File? image;
  final Map<String, dynamic>? analysisResult;
  const ChatScreen({super.key, this.image, this.analysisResult});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Map<String, String>> _messages = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    if (widget.analysisResult != null) {
       _messages.add({
        "role": "assistant",
        "content": widget.analysisResult!['report'] ?? "Analysis complete."
      });
    } else if (widget.image != null) {
      _messages.add({
        "role": "assistant",
        "content": "I have analyzed the uploaded image. I detected a potential irregularity in the upper right quadrant. How can I help you further?"
      });
    }
  }

  void _sendMessage() async {
    if (_controller.text.isEmpty) return;
    
    final userMessage = _controller.text;
    setState(() {
      _messages.add({"role": "user", "content": userMessage});
      _isLoading = true;
      _controller.clear();
    });
    
    _scrollToBottom();

    // Simulate backend streaming response (Replace with Dio SSE later)
    await Future.delayed(const Duration(seconds: 1));
    
    setState(() {
      _messages.add({"role": "assistant", "content": ""}); // Placeholder for stream
    });

    final fullResponse = "Based on the findings, this appears to be... [Detailed medical explanation would stream here]. \n\n**Recommendation:** Consult a specialist.";
    
    // Simulate streaming
    for (int i = 0; i < fullResponse.length; i++) {
        await Future.delayed(const Duration(milliseconds: 30));
        if (mounted) {
          setState(() {
             _messages.last["content"] = (_messages.last["content"] ?? "") + fullResponse[i];
          });
          _scrollToBottom();
        }
    }

    if (mounted) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Medical Analysis"),
        actions: [
          IconButton(
            icon: const Icon(Icons.summarize),
            onPressed: () {
              // Generate Report
            },
          )
        ],
      ),
      body: Column(
        children: [
          if (widget.image != null)
            Container(
              height: 200,
              width: double.infinity,
              color: Colors.black,
              child: Image.file(widget.image!, fit: BoxFit.contain),
            ),
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isUser = message["role"] == "user";
                return FadeInUp(
                  duration: const Duration(milliseconds: 300),
                  child: Align(
                    alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.symmetric(vertical: 8),
                      padding: const EdgeInsets.all(12),
                      constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
                      decoration: BoxDecoration(
                        color: isUser ? Theme.of(context).primaryColor : Theme.of(context).cardColor,
                        borderRadius: BorderRadius.circular(16).copyWith(
                          bottomRight: isUser ? Radius.zero : null,
                          bottomLeft: !isUser ? Radius.zero : null,
                        ),
                         boxShadow: [
                            if (!isUser)
                              BoxShadow(
                                color: Colors.black.withOpacity(0.05),
                                blurRadius: 4,
                                offset: const Offset(0, 2),
                              )
                          ]
                      ),
                      child: MarkdownBody(
                        data: message["content"]!,
                        styleSheet: MarkdownStyleSheet(
                          p: TextStyle(color: isUser ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color),
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isLoading)
             const Padding(
               padding: EdgeInsets.all(8.0),
               child: LinearProgressIndicator(),
             ),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 10,
                  offset: const Offset(0, -5),
                )
              ]
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: "Ask a follow-up question...",
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: Theme.of(context).scaffoldBackgroundColor,
                      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                CircleAvatar(
                  backgroundColor: Theme.of(context).primaryColor,
                  radius: 24,
                  child: IconButton(
                    icon: const Icon(Icons.send, color: Colors.white),
                    onPressed: _sendMessage,
                  ),
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}
