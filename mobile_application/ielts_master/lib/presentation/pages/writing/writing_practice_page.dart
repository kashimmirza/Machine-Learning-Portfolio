// lib/presentation/pages/writing/writing_practice_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import '../../providers/writing_provider.dart';
import '../../widgets/common/custom_button.dart';

class WritingPracticePage extends StatefulWidget {
  final String taskType;
  final String prompt;

  const WritingPracticePage({
    Key? key,
    required this.taskType,
    required this.prompt,
  }) : super(key: key);

  @override
  State<WritingPracticePage> createState() => _WritingPracticePageState();
}

class _WritingPracticePageState extends State<WritingPracticePage> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  int _wordCount = 0;
  int _timeElapsed = 0;
  Timer? _timer;
  Timer? _analysisTimer;
  bool _showFeedbackPanel = false;

  // Highlighted errors
  List<ErrorHighlight> _highlights = [];

  @override
  void initState() {
    super.initState();
    _textController.addListener(_onTextChanged);
    _startTimer();
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    _timer?.cancel();
    _analysisTimer?.cancel();
    super.dispose();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted) {
        setState(() => _timeElapsed++);
      }
    });
  }

  void _onTextChanged() {
    final text = _textController.text.trim();

    // Update word count
    setState(() {
      _wordCount = text.isEmpty ? 0 : text.split(RegExp(r'\s+')).length;
    });

    // Debounced real-time analysis
    _analysisTimer?.cancel();
    _analysisTimer = Timer(const Duration(seconds: 2), () {
      if (text.length > 50) {
        _analyzeText(text);
      }
    });
  }

  Future<void> _analyzeText(String text) async {
    final provider = context.read<WritingProvider>();
    await provider.analyzeRealTime(text);

    if (mounted && provider.currentFeedback != null) {
      setState(() {
        _highlights = _parseHighlights(provider.currentFeedback!);
      });
    }
  }

  List<ErrorHighlight> _parseHighlights(Map<String, dynamic> feedback) {
    final errors = feedback['errors'] as List<dynamic>? ?? [];
    return errors.map((e) => ErrorHighlight.fromJson(e)).toList();
  }

  Future<void> _submitForFeedback() async {
    if (_wordCount < (widget.taskType == 'task1' ? 150 : 250)) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Please write at least ${widget.taskType == 'task1' ? 150 : 250} words',
          ),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => const Center(
        child: Card(
          child: Padding(
            padding: EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                CircularProgressIndicator(),
                SizedBox(height: 16),
                Text('Getting AI feedback...'),
              ],
            ),
          ),
        ),
      ),
    );

    final provider = context.read<WritingProvider>();
    await provider.submitAssessment(
      taskType: widget.taskType,
      prompt: widget.prompt,
      answer: _textController.text,
      timeSpent: _timeElapsed,
    );

    if (mounted) {
      Navigator.pop(context);
      Navigator.pushNamed(
        context,
        '/writing/feedback',
        arguments: {'result': provider.lastAssessmentResult},
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
            Text('Writing ${widget.taskType == 'task1' ? 'Task 1' : 'Task 2'}'),
        actions: [
          // Timer
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  const Icon(Icons.timer, size: 20),
                  const SizedBox(width: 6),
                  Text(
                    '${(_timeElapsed ~/ 60).toString().padLeft(2, '0')}:${(_timeElapsed % 60).toString().padLeft(2, '0')}',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Feedback panel toggle
          IconButton(
            icon: Icon(
                _showFeedbackPanel ? Icons.close : Icons.lightbulb_outline),
            onPressed: () {
              setState(() => _showFeedbackPanel = !_showFeedbackPanel);
            },
            tooltip: 'AI Suggestions',
          ),
        ],
      ),
      body: Row(
        children: [
          // Main writing area
          Expanded(
            flex: _showFeedbackPanel ? 2 : 1,
            child: Column(
              children: [
                // Prompt
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.grey[50],
                    border: Border(
                      bottom: BorderSide(color: Colors.grey[300]!),
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Task ${widget.taskType == 'task1' ? '1' : '2'}',
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: Colors.grey,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        widget.prompt,
                        style: const TextStyle(
                          fontSize: 15,
                          height: 1.6,
                        ),
                      ),
                    ],
                  ),
                ),

                // Stats bar
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 12,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    border: Border(
                      bottom: BorderSide(color: Colors.grey[200]!),
                    ),
                  ),
                  child: Row(
                    children: [
                      _StatChip(
                        icon: Icons.text_fields,
                        label: 'Words',
                        value: _wordCount.toString(),
                        color: _wordCount >=
                                (widget.taskType == 'task1' ? 150 : 250)
                            ? Colors.green
                            : Colors.orange,
                      ),
                      const SizedBox(width: 16),
                      _StatChip(
                        icon: Icons.error_outline,
                        label: 'Errors',
                        value: _highlights.length.toString(),
                        color: _highlights.isEmpty ? Colors.green : Colors.red,
                      ),
                      const Spacer(),
                      // AI Status
                      Consumer<WritingProvider>(
                        builder: (context, provider, _) {
                          return Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 12,
                              vertical: 6,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.green[50],
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Container(
                                  width: 8,
                                  height: 8,
                                  decoration: const BoxDecoration(
                                    color: Colors.green,
                                    shape: BoxShape.circle,
                                  ),
                                ),
                                const SizedBox(width: 8),
                                const Text(
                                  'AI Active',
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w600,
                                    color: Colors.green,
                                  ),
                                ),
                              ],
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                ),

                // Text editor
                Expanded(
                  child: Stack(
                    children: [
                      // Highlighted text (background layer)
                      if (_highlights.isNotEmpty)
                        Padding(
                          padding: const EdgeInsets.all(20),
                          child: _buildHighlightedText(),
                        ),

                      // Actual editable text
                      TextField(
                        controller: _textController,
                        maxLines: null,
                        expands: true,
                        style: const TextStyle(
                          fontSize: 16,
                          height: 1.8,
                          color: Colors.black87,
                        ),
                        decoration: const InputDecoration(
                          hintText: 'Start writing your answer here...\n\n'
                              'Tips:\n'
                              '• Structure your essay with clear paragraphs\n'
                              '• Use a variety of vocabulary\n'
                              '• Check grammar as you write',
                          hintStyle: TextStyle(color: Colors.grey),
                          border: InputBorder.none,
                          contentPadding: EdgeInsets.all(20),
                        ),
                      ),
                    ],
                  ),
                ),

                // Bottom action bar
                Container(
                  padding: const EdgeInsets.all(16),
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
                  child: Row(
                    children: [
                      Expanded(
                        child: OutlinedButton.icon(
                          icon: const Icon(Icons.save_outlined),
                          label: const Text('Save Draft'),
                          onPressed: () {
                            // Save draft
                          },
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        flex: 2,
                        child: CustomButton(
                          text: 'Get Feedback',
                          icon: Icons.check_circle_outline,
                          onPressed: _submitForFeedback,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Feedback panel
          if (_showFeedbackPanel)
            Container(
              width: 350,
              decoration: BoxDecoration(
                color: Colors.white,
                border: Border(
                  left: BorderSide(color: Colors.grey[300]!),
                ),
              ),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Theme.of(context).primaryColor.withOpacity(0.1),
                      border: Border(
                        bottom: BorderSide(color: Colors.grey[300]!),
                      ),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          Icons.auto_awesome,
                          color: Theme.of(context).primaryColor,
                        ),
                        const SizedBox(width: 12),
                        const Text(
                          'AI Suggestions',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: _highlights.isEmpty
                        ? Center(
                            child: Padding(
                              padding: const EdgeInsets.all(32),
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Icon(
                                    Icons.check_circle_outline,
                                    size: 64,
                                    color: Colors.green[300],
                                  ),
                                  const SizedBox(height: 16),
                                  const Text(
                                    'Looking good!',
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    'No errors detected. Keep writing!',
                                    style: TextStyle(
                                      color: Colors.grey[600],
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                ],
                              ),
                            ),
                          )
                        : ListView.separated(
                            padding: const EdgeInsets.all(16),
                            itemCount: _highlights.length,
                            separatorBuilder: (_, __) =>
                                const SizedBox(height: 12),
                            itemBuilder: (context, index) {
                              final highlight = _highlights[index];
                              return _ErrorCard(highlight: highlight);
                            },
                          ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildHighlightedText() {
    // This would overlay highlighted errors
    return const SizedBox();
  }
}

class _StatChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;

  const _StatChip({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 18, color: color),
        const SizedBox(width: 6),
        Text(
          '$label: ',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
          ),
        ),
        Text(
          value,
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }
}

class _ErrorCard extends StatelessWidget {
  final ErrorHighlight highlight;

  const _ErrorCard({required this.highlight});

  IconData get _icon {
    switch (highlight.type) {
      case 'grammar':
        return Icons.spellcheck;
      case 'vocabulary':
        return Icons.book;
      case 'structure':
        return Icons.account_tree;
      default:
        return Icons.error_outline;
    }
  }

  Color get _color {
    switch (highlight.severity) {
      case 'error':
        return Colors.red;
      case 'warning':
        return Colors.orange;
      default:
        return Colors.blue;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: _color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: _color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(_icon, size: 20, color: _color),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  highlight.category.toUpperCase(),
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: _color,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),

          // Error text
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.red[50],
              borderRadius: BorderRadius.circular(6),
            ),
            child: Row(
              children: [
                const Icon(Icons.close, size: 16, color: Colors.red),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    highlight.text,
                    style: const TextStyle(
                      decoration: TextDecoration.lineThrough,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),

          // Correction
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.green[50],
              borderRadius: BorderRadius.circular(6),
            ),
            child: Row(
              children: [
                const Icon(Icons.check, size: 16, color: Colors.green),
                const SizedBox(width: 6),
                Expanded(
                  child: Text(
                    highlight.correction,
                    style: const TextStyle(
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),

          // Explanation
          Text(
            highlight.explanation,
            style: TextStyle(
              fontSize: 13,
              color: Colors.grey[700],
            ),
          ),
        ],
      ),
    );
  }
}

class ErrorHighlight {
  final String type;
  final String category;
  final String text;
  final String correction;
  final String explanation;
  final String severity;
  final int start;
  final int end;

  ErrorHighlight({
    required this.type,
    required this.category,
    required this.text,
    required this.correction,
    required this.explanation,
    required this.severity,
    required this.start,
    required this.end,
  });

  factory ErrorHighlight.fromJson(Map<String, dynamic> json) {
    return ErrorHighlight(
      type: json['type'] ?? 'grammar',
      category: json['category'] ?? 'Error',
      text: json['text'] ?? '',
      correction: json['correction'] ?? '',
      explanation: json['explanation'] ?? '',
      severity: json['severity'] ?? 'error',
      start: json['position']?['start'] ?? 0,
      end: json['position']?['end'] ?? 0,
    );
  }
}

// pubspec.yaml
/*
name: ielts_master
description: AI-powered IELTS preparation platform
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.1.1
  
  # UI & Animations
  flutter_animate: ^4.5.0
  shimmer: ^3.0.0
  lottie: ^3.0.0
  
  # Network & API
  dio: ^5.4.0
  http: ^1.1.2
  
  # Storage
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # Firebase
  firebase_core: ^2.24.2
  firebase_auth: ^4.15.3
  firebase_analytics: ^10.8.0
  cloud_firestore: ^4.14.0
  firebase_storage: ^11.6.0
  
  # Audio & Recording (for Speaking module)
  just_audio: ^0.9.36
  record: ^5.0.4
  audio_waveforms: ^1.0.5
  
  # Charts & Graphs
  fl_chart: ^0.66.0
  syncfusion_flutter_charts: ^24.1.41
  
  # Date & Time
  intl: ^0.18.1
  
  # Payment
  razorpay_flutter: ^1.3.6
  stripe_payment: ^1.1.4
  
  # Utilities
  path_provider: ^2.1.1
  url_launcher: ^6.2.2
  share_plus: ^7.2.1
  image_picker: ^1.0.5
  
  # Icons & Fonts
  cupertino_icons: ^1.0.6
  google_fonts: ^6.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  build_runner: ^2.4.7
  hive_generator: ^2.0.1

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/icons/
    - assets/animations/
    - assets/audio/
  
  fonts:
    - family: Poppins
      fonts:
        - asset: assets/fonts/Poppins-Regular.ttf
        - asset: assets/fonts/Poppins-Medium.ttf
          weight: 500
        - asset: assets/fonts/Poppins-SemiBold.ttf
          weight: 600
        - asset: assets/fonts/Poppins-Bold.ttf
          weight: 700
*/