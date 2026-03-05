// lib/presentation/pages/listening/listening_practice_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:just_audio/just_audio.dart';
import '../../providers/listening_provider.dart';
import '../../widgets/common/custom_button.dart';

class ListeningPracticePage extends StatefulWidget {
  final Map<String, dynamic> audio;

  const ListeningPracticePage({
    Key? key,
    required this.audio,
  }) : super(key: key);

  @override
  State<ListeningPracticePage> createState() => _ListeningPracticePageState();
}

class _ListeningPracticePageState extends State<ListeningPracticePage> {
  final AudioPlayer _player = AudioPlayer();
  final Map<int, dynamic> _answers = {};

  bool _isPlaying = false;
  bool _hasStarted = false;
  Duration _duration = Duration.zero;
  Duration _position = Duration.zero;

  List<Map<String, dynamic>> get _questions =>
      List<Map<String, dynamic>>.from(widget.audio['questions']);

  @override
  void initState() {
    super.initState();
    _initPlayer();
  }

  @override
  void dispose() {
    _player.dispose();
    super.dispose();
  }

  Future<void> _initPlayer() async {
    try {
      await _player.setUrl(widget.audio['audioUrl']);

      _player.durationStream.listen((duration) {
        setState(() => _duration = duration ?? Duration.zero);
      });

      _player.positionStream.listen((position) {
        setState(() => _position = position);
      });

      _player.playerStateStream.listen((state) {
        setState(() {
          _isPlaying = state.playing;
        });
      });
    } catch (e) {
      _showError('Failed to load audio: $e');
    }
  }

  Future<void> _playPause() async {
    if (!_hasStarted) {
      setState(() => _hasStarted = true);
    }

    if (_isPlaying) {
      await _player.pause();
    } else {
      await _player.play();
    }
  }

  Future<void> _seekBackward() async {
    final newPosition = _position - const Duration(seconds: 5);
    await _player
        .seek(newPosition < Duration.zero ? Duration.zero : newPosition);
  }

  Future<void> _seekForward() async {
    final newPosition = _position + const Duration(seconds: 5);
    await _player.seek(newPosition > _duration ? _duration : newPosition);
  }

  Future<void> _submitTest() async {
    await _player.pause();

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

    final provider = context.read<ListeningProvider>();
    await provider.submitListening(
      audioId: widget.audio['id'],
      answers: _answers,
    );

    if (mounted) {
      Navigator.pop(context);
      Navigator.pushReplacementNamed(
        context,
        '/listening/result',
        arguments: {'result': provider.lastResult},
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Listening Practice'),
      ),
      body: Column(
        children: [
          // Audio player
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  Theme.of(context).primaryColor,
                  Theme.of(context).colorScheme.secondary,
                ],
              ),
            ),
            child: Column(
              children: [
                Text(
                  widget.audio['title'],
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  widget.audio['accent'] ?? 'British Accent',
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.white70,
                  ),
                ),
                const SizedBox(height: 24),

                // Progress bar
                SliderTheme(
                  data: SliderThemeData(
                    activeTrackColor: Colors.white,
                    inactiveTrackColor: Colors.white.withOpacity(0.3),
                    thumbColor: Colors.white,
                    overlayColor: Colors.white.withOpacity(0.2),
                  ),
                  child: Slider(
                    value: _position.inSeconds.toDouble(),
                    max: _duration.inSeconds.toDouble(),
                    onChanged: (value) {
                      _player.seek(Duration(seconds: value.toInt()));
                    },
                  ),
                ),

                // Time display
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        _formatDuration(_position),
                        style: const TextStyle(color: Colors.white70),
                      ),
                      Text(
                        _formatDuration(_duration),
                        style: const TextStyle(color: Colors.white70),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),

                // Playback controls
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      icon: const Icon(Icons.replay_5, color: Colors.white),
                      iconSize: 32,
                      onPressed: _seekBackward,
                    ),
                    const SizedBox(width: 24),
                    Container(
                      width: 64,
                      height: 64,
                      decoration: const BoxDecoration(
                        color: Colors.white,
                        shape: BoxShape.circle,
                      ),
                      child: IconButton(
                        icon: Icon(
                          _isPlaying ? Icons.pause : Icons.play_arrow,
                          color: Theme.of(context).primaryColor,
                        ),
                        iconSize: 32,
                        onPressed: _playPause,
                      ),
                    ),
                    const SizedBox(width: 24),
                    IconButton(
                      icon: const Icon(Icons.forward_5, color: Colors.white),
                      iconSize: 32,
                      onPressed: _seekForward,
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Instructions
          if (!_hasStarted)
            Container(
              margin: const EdgeInsets.all(20),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.orange[50],
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.orange[200]!),
              ),
              child: Row(
                children: [
                  Icon(Icons.info_outline, color: Colors.orange[700]),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Text(
                      'Play the audio and answer the questions. You can replay the audio anytime.',
                      style: TextStyle(fontSize: 14),
                    ),
                  ),
                ],
              ),
            ),

          // Questions
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(20),
              itemCount: _questions.length,
              itemBuilder: (context, index) {
                return _buildQuestionCard(_questions[index], index);
              },
            ),
          ),

          // Submit button
          Container(
            padding: const EdgeInsets.all(20),
            child: SafeArea(
              child: CustomButton(
                text: 'Submit Test',
                icon: Icons.check,
                onPressed:
                    _answers.length == _questions.length ? _submitTest : null,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuestionCard(Map<String, dynamic> question, int index) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Question ${index + 1}',
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              question['question'],
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              onChanged: (value) {
                setState(() => _answers[index] = value);
              },
              decoration: InputDecoration(
                hintText: 'Type your answer',
                filled: true,
                fillColor: Colors.grey[50],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _formatDuration(Duration duration) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    final mins = twoDigits(duration.inMinutes.remainder(60));
    final secs = twoDigits(duration.inSeconds.remainder(60));
    return '$mins:$secs';
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }
}
