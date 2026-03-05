// lib/presentation/pages/reading/reading_practice_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import '../../providers/reading_provider.dart';
import '../../widgets/common/custom_button.dart';

class ReadingPracticePage extends StatefulWidget {
  final Map<String, dynamic> passage;

  const ReadingPracticePage({
    Key? key,
    required this.passage,
  }) : super(key: key);

  @override
  State<ReadingPracticePage> createState() => _ReadingPracticePageState();
}

class _ReadingPracticePageState extends State<ReadingPracticePage> {
  final PageController _pageController = PageController();
  final Map<int, dynamic> _answers = {};

  int _currentPage = 0;
  int _timeElapsed = 0;
  Timer? _timer;
  bool _showPassage = true;

  List<Map<String, dynamic>> get _questions =>
      List<Map<String, dynamic>>.from(widget.passage['questions']);

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  @override
  void dispose() {
    _timer?.cancel();
    _pageController.dispose();
    super.dispose();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() => _timeElapsed++);

      // Auto-submit after 20 minutes
      if (_timeElapsed >= 1200) {
        _submitTest();
      }
    });
  }

  void _toggleView() {
    setState(() => _showPassage = !_showPassage);
  }

  void _nextQuestion() {
    if (_currentPage < _questions.length - 1) {
      _pageController.nextPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }

  void _previousQuestion() {
    if (_currentPage > 0) {
      _pageController.previousPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }

  Future<void> _submitTest() async {
    _timer?.cancel();

    // Check if all questions are answered
    final unanswered = _questions.length - _answers.length;
    if (unanswered > 0) {
      final confirm = await showDialog<bool>(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Submit Test?'),
          content: Text(
            'You have $unanswered unanswered question${unanswered > 1 ? 's' : ''}. '
            'Are you sure you want to submit?',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Continue'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.pop(context, true),
              child: const Text('Submit'),
            ),
          ],
        ),
      );

      if (confirm != true) return;
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
                Text('Evaluating your answers...'),
              ],
            ),
          ),
        ),
      ),
    );

    final provider = context.read<ReadingProvider>();
    await provider.submitReading(
      passageId: widget.passage['id'],
      answers: _answers,
      timeSpent: _timeElapsed,
    );

    if (mounted) {
      Navigator.pop(context);
      Navigator.pushReplacementNamed(
        context,
        '/reading/result',
        arguments: {'result': provider.lastResult},
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Reading Practice'),
        actions: [
          // Timer
          Container(
            margin: const EdgeInsets.only(right: 8),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: _timeElapsed >= 1080 // 18 mins
                  ? Colors.orange[50]
                  : Colors.green[50],
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              children: [
                Icon(
                  Icons.timer,
                  size: 16,
                  color: _timeElapsed >= 1080 ? Colors.orange : Colors.green,
                ),
                const SizedBox(width: 6),
                Text(
                  '${(_timeElapsed ~/ 60).toString().padLeft(2, '0')}:'
                  '${(_timeElapsed % 60).toString().padLeft(2, '0')}',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: _timeElapsed >= 1080 ? Colors.orange : Colors.green,
                  ),
                ),
              ],
            ),
          ),
          // Toggle view
          IconButton(
            icon: Icon(_showPassage ? Icons.question_answer : Icons.article),
            onPressed: _toggleView,
            tooltip: _showPassage ? 'Show Questions' : 'Show Passage',
          ),
        ],
      ),
      body: Row(
        children: [
          // Passage panel
          if (_showPassage)
            Expanded(
              flex: _showPassage && MediaQuery.of(context).size.width > 600
                  ? 1
                  : 0,
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.grey[50],
                  border: Border(
                    right: BorderSide(color: Colors.grey[300]!),
                  ),
                ),
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        widget.passage['title'],
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        widget.passage['text'],
                        style: const TextStyle(
                          fontSize: 16,
                          height: 1.8,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

          // Questions panel
          Expanded(
            child: Column(
              children: [
                // Progress indicator
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    border: Border(
                      bottom: BorderSide(color: Colors.grey[200]!),
                    ),
                  ),
                  child: Row(
                    children: [
                      Text(
                        'Question ${_currentPage + 1} of ${_questions.length}',
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        '${_answers.length}/${_questions.length} answered',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),

                // Questions PageView
                Expanded(
                  child: PageView.builder(
                    controller: _pageController,
                    onPageChanged: (index) {
                      setState(() => _currentPage = index);
                    },
                    itemCount: _questions.length,
                    itemBuilder: (context, index) {
                      return _buildQuestionCard(_questions[index], index);
                    },
                  ),
                ),

                // Navigation buttons
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
                  child: SafeArea(
                    child: Row(
                      children: [
                        if (_currentPage > 0)
                          Expanded(
                            child: OutlinedButton.icon(
                              icon: const Icon(Icons.arrow_back),
                              label: const Text('Previous'),
                              onPressed: _previousQuestion,
                              style: OutlinedButton.styleFrom(
                                padding:
                                    const EdgeInsets.symmetric(vertical: 16),
                              ),
                            ),
                          ),
                        if (_currentPage > 0) const SizedBox(width: 12),
                        Expanded(
                          flex: 2,
                          child: _currentPage == _questions.length - 1
                              ? CustomButton(
                                  text: 'Submit Test',
                                  icon: Icons.check,
                                  onPressed: _submitTest,
                                  backgroundColor: Colors.green,
                                )
                              : CustomButton(
                                  text: 'Next',
                                  icon: Icons.arrow_forward,
                                  onPressed: _nextQuestion,
                                ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuestionCard(Map<String, dynamic> question, int index) {
    final type = question['type'];

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Question text
          Text(
            question['question'],
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              height: 1.5,
            ),
          ),
          const SizedBox(height: 24),

          // Answer options based on type
          if (type == 'multiple_choice')
            _buildMultipleChoice(question, index)
          else if (type == 'true_false_not_given')
            _buildTrueFalseNotGiven(question, index)
          else if (type == 'matching')
            _buildMatching(question, index)
          else if (type == 'fill_in_blank')
            _buildFillInBlank(question, index),
        ],
      ),
    );
  }

  Widget _buildMultipleChoice(Map<String, dynamic> question, int index) {
    final options = List<String>.from(question['options']);

    return Column(
      children: List.generate(
        options.length,
        (optIndex) {
          final option = options[optIndex];
          final optionLetter = String.fromCharCode(65 + optIndex); // A, B, C, D
          final isSelected = _answers[index] == option;

          return GestureDetector(
            onTap: () {
              setState(() => _answers[index] = option);
            },
            child: Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: isSelected
                    ? Theme.of(context).primaryColor.withOpacity(0.1)
                    : Colors.white,
                border: Border.all(
                  color: isSelected
                      ? Theme.of(context).primaryColor
                      : Colors.grey[300]!,
                  width: isSelected ? 2 : 1,
                ),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  Container(
                    width: 32,
                    height: 32,
                    decoration: BoxDecoration(
                      color: isSelected
                          ? Theme.of(context).primaryColor
                          : Colors.grey[200],
                      shape: BoxShape.circle,
                    ),
                    child: Center(
                      child: Text(
                        optionLetter,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: isSelected ? Colors.white : Colors.black87,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Text(
                      option,
                      style: const TextStyle(fontSize: 16),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildTrueFalseNotGiven(Map<String, dynamic> question, int index) {
    final options = ['TRUE', 'FALSE', 'NOT GIVEN'];

    return Row(
      children: List.generate(
        options.length,
        (optIndex) {
          final option = options[optIndex];
          final isSelected = _answers[index] == option;

          return Expanded(
            child: GestureDetector(
              onTap: () {
                setState(() => _answers[index] = option);
              },
              child: Container(
                margin: EdgeInsets.only(
                  right: optIndex < options.length - 1 ? 8 : 0,
                ),
                padding: const EdgeInsets.symmetric(vertical: 20),
                decoration: BoxDecoration(
                  color: isSelected
                      ? Theme.of(context).primaryColor
                      : Colors.white,
                  border: Border.all(
                    color: isSelected
                        ? Theme.of(context).primaryColor
                        : Colors.grey[300]!,
                  ),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  option,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: isSelected ? Colors.white : Colors.black87,
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildMatching(Map<String, dynamic> question, int index) {
    return const Text('Matching questions - Implementation similar to above');
  }

  Widget _buildFillInBlank(Map<String, dynamic> question, int index) {
    return TextField(
      onChanged: (value) {
        setState(() => _answers[index] = value);
      },
      decoration: InputDecoration(
        hintText: 'Type your answer here',
        filled: true,
        fillColor: Colors.grey[50],
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      style: const TextStyle(fontSize: 16),
    );
  }
}
