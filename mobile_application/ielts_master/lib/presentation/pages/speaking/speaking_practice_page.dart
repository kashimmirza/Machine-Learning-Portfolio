// lib/presentation/pages/speaking/speaking_practice_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:record/record.dart';
import 'package:just_audio/just_audio.dart';
import 'dart:async';
import '../../providers/speaking_provider.dart';
import '../../widgets/common/custom_button.dart';
import 'widgets/voice_recorder.dart';
import 'widgets/waveform_visualizer.dart';

class SpeakingPracticePage extends StatefulWidget {
  final String part; // part1, part2, part3
  final Map<String, dynamic> question;

  const SpeakingPracticePage({
    Key? key,
    required this.part,
    required this.question,
  }) : super(key: key);

  @override
  State<SpeakingPracticePage> createState() => _SpeakingPracticePageState();
}

class _SpeakingPracticePageState extends State<SpeakingPracticePage> {
  final AudioRecorder _recorder = AudioRecorder();
  final AudioPlayer _player = AudioPlayer();

  bool _isRecording = false;
  bool _isPlaying = false;
  bool _isPaused = false;

  int _recordingDuration = 0;
  int _preparationTime = 0;
  Timer? _timer;

  String? _audioPath;
  List<double> _waveformData = [];

  @override
  void initState() {
    super.initState();
    _startPreparationTimer();
  }

  @override
  void dispose() {
    _recorder.dispose();
    _player.dispose();
    _timer?.cancel();
    super.dispose();
  }

  void _startPreparationTimer() {
    if (widget.part == 'part2') {
      // Part 2 has 1 minute preparation time
      _preparationTime = 60;
      _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
        if (_preparationTime > 0) {
          setState(() => _preparationTime--);
        } else {
          timer.cancel();
          _showStartRecordingDialog();
        }
      });
    }
  }

  void _showStartRecordingDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Preparation Time Over'),
        content: const Text('You can now start recording your answer.'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _startRecording();
            },
            child: const Text('Start Recording'),
          ),
        ],
      ),
    );
  }

  Future<void> _startRecording() async {
    try {
      if (await _recorder.hasPermission()) {
        final path = await _getAudioPath();
        await _recorder.start(
          const RecordConfig(encoder: AudioEncoder.aacLc),
          path: path,
        );

        setState(() {
          _isRecording = true;
          _recordingDuration = 0;
          _audioPath = path;
        });

        _startRecordingTimer();
      }
    } catch (e) {
      _showError('Failed to start recording: $e');
    }
  }

  Future<void> _stopRecording() async {
    try {
      final path = await _recorder.stop();
      _timer?.cancel();

      setState(() {
        _isRecording = false;
        _audioPath = path;
      });

      if (path != null) {
        _showSubmitDialog();
      }
    } catch (e) {
      _showError('Failed to stop recording: $e');
    }
  }

  void _startRecordingTimer() {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() => _recordingDuration++);

      // Auto-stop for Part 2 after 2 minutes
      if (widget.part == 'part2' && _recordingDuration >= 120) {
        _stopRecording();
      }
    });
  }

  Future<void> _playRecording() async {
    if (_audioPath == null) return;

    try {
      await _player.setFilePath(_audioPath!);
      await _player.play();

      setState(() => _isPlaying = true);

      _player.playerStateStream.listen((state) {
        if (state.processingState == ProcessingState.completed) {
          setState(() => _isPlaying = false);
        }
      });
    } catch (e) {
      _showError('Failed to play recording: $e');
    }
  }

  Future<void> _pausePlayback() async {
    await _player.pause();
    setState(() => _isPaused = true);
  }

  Future<void> _resumePlayback() async {
    await _player.play();
    setState(() => _isPaused = false);
  }

  void _showSubmitDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Submit for Assessment?'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Your recording will be analyzed for:'),
            const SizedBox(height: 12),
            _buildFeatureItem('Pronunciation & Accent'),
            _buildFeatureItem('Fluency & Coherence'),
            _buildFeatureItem('Grammar & Vocabulary'),
            _buildFeatureItem('Task Response'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              setState(() => _audioPath = null);
            },
            child: const Text('Re-record'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              _submitForAssessment();
            },
            child: const Text('Submit'),
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureItem(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(
        children: [
          const Icon(Icons.check_circle, size: 16, color: Colors.green),
          const SizedBox(width: 8),
          Text(text, style: const TextStyle(fontSize: 14)),
        ],
      ),
    );
  }

  Future<void> _submitForAssessment() async {
    if (_audioPath == null) return;

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
                Text('Analyzing your speaking...'),
                SizedBox(height: 8),
                Text(
                  'AI is evaluating pronunciation, fluency, and content',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ),
    );

    final provider = context.read<SpeakingProvider>();
    await provider.submitSpeaking(
      part: widget.part,
      question: widget.question['question'],
      audioPath: _audioPath!,
      duration: _recordingDuration,
    );

    if (mounted) {
      Navigator.pop(context); // Close loading dialog
      Navigator.pushNamed(
        context,
        '/speaking/feedback',
        arguments: {'result': provider.lastAssessmentResult},
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Speaking ${widget.part.toUpperCase()}'),
        actions: [
          if (_preparationTime > 0)
            Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.orange[50],
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.timer, size: 16, color: Colors.orange),
                      const SizedBox(width: 6),
                      Text(
                        'Prep: ${_preparationTime}s',
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: Colors.orange,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          // Question Card
          Container(
            width: double.infinity,
            margin: const EdgeInsets.all(20),
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  Theme.of(context).primaryColor.withOpacity(0.1),
                  Theme.of(context).colorScheme.secondary.withOpacity(0.1),
                ],
              ),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        widget.part.toUpperCase(),
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const Spacer(),
                    if (widget.part == 'part2')
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 6,
                        ),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: const Text(
                          '1-2 minutes',
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 16),
                Text(
                  widget.question['question'],
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    height: 1.5,
                  ),
                ),
                if (widget.question['prompts'] != null) ...[
                  const SizedBox(height: 12),
                  ...List.generate(
                    (widget.question['prompts'] as List).length,
                    (index) => Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('• ', style: TextStyle(fontSize: 16)),
                          Expanded(
                            child: Text(
                              widget.question['prompts'][index],
                              style: const TextStyle(fontSize: 15),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),

          const Spacer(),

          // Recording Interface
          if (!_isRecording && _audioPath == null)
            _buildReadyToRecordUI()
          else if (_isRecording)
            _buildRecordingUI()
          else if (_audioPath != null)
            _buildPlaybackUI(),

          const Spacer(),

          // Action Buttons
          Container(
            padding: const EdgeInsets.all(20),
            child: SafeArea(
              child: _buildActionButtons(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReadyToRecordUI() {
    return Column(
      children: [
        Icon(
          Icons.mic_none,
          size: 120,
          color: Colors.grey[300],
        ),
        const SizedBox(height: 24),
        Text(
          _preparationTime > 0 ? 'Prepare your answer...' : 'Ready to record',
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          _preparationTime > 0
              ? 'Use this time to organize your thoughts'
              : 'Tap the microphone button to start',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
          ),
        ),
      ],
    );
  }

  Widget _buildRecordingUI() {
    return Column(
      children: [
        // Animated microphone
        Container(
          width: 120,
          height: 120,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.red[50],
            boxShadow: [
              BoxShadow(
                color: Colors.red.withOpacity(0.3),
                blurRadius: 20,
                spreadRadius: 5,
              ),
            ],
          ),
          child: const Icon(
            Icons.mic,
            size: 60,
            color: Colors.red,
          ),
        ),
        const SizedBox(height: 24),
        const Text(
          'Recording...',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.red,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          _formatDuration(_recordingDuration),
          style: const TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 24),
        // Waveform visualizer
        Container(
          height: 60,
          margin: const EdgeInsets.symmetric(horizontal: 40),
          child: WaveformVisualizer(isRecording: _isRecording),
        ),
      ],
    );
  }

  Widget _buildPlaybackUI() {
    return Column(
      children: [
        Icon(
          _isPlaying ? Icons.volume_up : Icons.check_circle,
          size: 120,
          color: _isPlaying ? Theme.of(context).primaryColor : Colors.green,
        ),
        const SizedBox(height: 24),
        Text(
          _isPlaying ? 'Playing...' : 'Recording Complete',
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          'Duration: ${_formatDuration(_recordingDuration)}',
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
          ),
        ),
      ],
    );
  }

  Widget _buildActionButtons() {
    if (!_isRecording && _audioPath == null) {
      return CustomButton(
        text: _preparationTime > 0 ? 'Preparing...' : 'Start Recording',
        icon: Icons.mic,
        onPressed: _preparationTime > 0 ? null : _startRecording,
        backgroundColor: Colors.red,
      );
    } else if (_isRecording) {
      return CustomButton(
        text: 'Stop Recording',
        icon: Icons.stop,
        onPressed: _stopRecording,
        backgroundColor: Colors.red,
      );
    } else {
      return Row(
        children: [
          Expanded(
            child: OutlinedButton.icon(
              icon: Icon(_isPlaying
                  ? (_isPaused ? Icons.play_arrow : Icons.pause)
                  : Icons.play_arrow),
              label: Text(_isPlaying ? 'Pause' : 'Play'),
              onPressed: () {
                if (_isPlaying) {
                  if (_isPaused) {
                    _resumePlayback();
                  } else {
                    _pausePlayback();
                  }
                } else {
                  _playRecording();
                }
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
              text: 'Submit',
              icon: Icons.send,
              onPressed: () => _showSubmitDialog(),
            ),
          ),
        ],
      );
    }
  }

  String _formatDuration(int seconds) {
    final mins = (seconds ~/ 60).toString().padLeft(2, '0');
    final secs = (seconds % 60).toString().padLeft(2, '0');
    return '$mins:$secs';
  }

  Future<String> _getAudioPath() async {
    // Implementation depends on path_provider
    return '/path/to/audio_${DateTime.now().millisecondsSinceEpoch}.aac';
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }
}
