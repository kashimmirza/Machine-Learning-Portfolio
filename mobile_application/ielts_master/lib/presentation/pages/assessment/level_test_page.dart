// lib/presentation/pages/assessment/level_test_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/writing_provider.dart';
import '../../widgets/common/custom_button.dart';

class LevelTestPage extends StatefulWidget {
  final String moduleId;
  final double targetScore;

  const LevelTestPage({
    Key? key,
    required this.moduleId,
    required this.targetScore,
  }) : super(key: key);

  @override
  State<LevelTestPage> createState() => _LevelTestPageState();
}

class _LevelTestPageState extends State<LevelTestPage> {
  final TextEditingController _answerController = TextEditingController();
  int _wordCount = 0;
  int _timeElapsed = 0;
  bool _isTestStarted = false;

  final String _prompt = '''
You should spend about 20 minutes on this task.

The chart below shows the percentage of households in owned and rented accommodation in England and Wales between 1918 and 2011.

Summarise the information by selecting and reporting the main features, and make comparisons where relevant.

Write at least 150 words.
''';

  @override
  void initState() {
    super.initState();
    _answerController.addListener(_updateWordCount);
  }

  @override
  void dispose() {
    _answerController.dispose();
    super.dispose();
  }

  void _updateWordCount() {
    final text = _answerController.text.trim();
    if (text.isEmpty) {
      setState(() => _wordCount = 0);
    } else {
      setState(() {
        _wordCount = text.split(RegExp(r'\s+')).length;
      });
    }
  }

  Future<void> _submitTest() async {
    if (_wordCount < 150) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please write at least 150 words'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    final writingProvider = context.read<WritingProvider>();

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => Center(
        child: Card(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const CircularProgressIndicator(),
                const SizedBox(height: 16),
                const Text('Analyzing your writing...'),
                const SizedBox(height: 8),
                const Text(
                  'AI is evaluating grammar, vocabulary, and structure',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );

    try {
      writingProvider.setLoading(true);
      // Simulate assessment processing
      await Future.delayed(const Duration(seconds: 2));
      writingProvider.setLoading(false);

      if (mounted) {
        Navigator.pop(context); // Close loading dialog
        Navigator.pushReplacementNamed(
          context,
          '/assessment-result',
          arguments: {
            'result': writingProvider.lastAssessmentResult,
          },
        );
      }
    } catch (e) {
      writingProvider.setLoading(false);
      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Level Assessment - Writing'),
        actions: [
          if (_isTestStarted)
            Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Text(
                  '${(_timeElapsed ~/ 60).toString().padLeft(2, '0')}:${(_timeElapsed % 60).toString().padLeft(2, '0')}',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          // Instructions Banner
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            color: Theme.of(context).primaryColor.withOpacity(0.1),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(
                      Icons.info_outline,
                      color: Theme.of(context).primaryColor,
                    ),
                    const SizedBox(width: 12),
                    const Text(
                      'Assessment Instructions',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                const Text(
                  '• Write at least 150 words\n'
                  '• Recommended time: 20 minutes\n'
                  '• Your writing will be scored on 4 criteria',
                  style: TextStyle(fontSize: 14),
                ),
              ],
            ),
          ),

          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Prompt
                  const Text(
                    'Task 1',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      _prompt,
                      style: const TextStyle(
                        fontSize: 15,
                        height: 1.6,
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Writing Area
                  const Text(
                    'Your Answer',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),

                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.grey[300]!),
                    ),
                    child: Column(
                      children: [
                        // Word count bar
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 12,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.grey[50],
                            borderRadius: const BorderRadius.only(
                              topLeft: Radius.circular(12),
                              topRight: Radius.circular(12),
                            ),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'Word Count: $_wordCount',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.w600,
                                  color: _wordCount >= 150
                                      ? Colors.green
                                      : Colors.orange,
                                ),
                              ),
                              if (_wordCount > 0)
                                Text(
                                  _wordCount >= 150 ? '✓ Good' : 'Min: 150',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey[600],
                                  ),
                                ),
                            ],
                          ),
                        ),

                        // Text editor
                        TextField(
                          controller: _answerController,
                          maxLines: 15,
                          style: const TextStyle(
                            fontSize: 16,
                            height: 1.8,
                          ),
                          decoration: const InputDecoration(
                            hintText: 'Start typing your answer here...',
                            border: InputBorder.none,
                            contentPadding: EdgeInsets.all(16),
                          ),
                          onChanged: (text) {
                            if (!_isTestStarted && text.isNotEmpty) {
                              setState(() => _isTestStarted = true);
                              _startTimer();
                            }
                          },
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Bottom action bar
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: const Offset(0, -5),
                ),
              ],
            ),
            child: SafeArea(
              child: CustomButton(
                text: 'Submit for Assessment',
                onPressed: _submitTest,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _startTimer() {
    Future.delayed(const Duration(seconds: 1), () {
      if (mounted && _isTestStarted) {
        setState(() => _timeElapsed++);
        _startTimer();
      }
    });
  }
}
