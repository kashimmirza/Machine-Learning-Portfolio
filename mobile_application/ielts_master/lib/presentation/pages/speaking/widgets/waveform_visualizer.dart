// lib/presentation/pages/speaking/widgets/waveform_visualizer.dart
import 'package:flutter/material.dart';
import 'dart:math';

class WaveformVisualizer extends StatefulWidget {
  final bool isRecording;

  const WaveformVisualizer({
    Key? key,
    required this.isRecording,
  }) : super(key: key);

  @override
  State<WaveformVisualizer> createState() => _WaveformVisualizerState();
}

class _WaveformVisualizerState extends State<WaveformVisualizer>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<double> _amplitudes = List.generate(30, (_) => 0.5);
  final Random _random = Random();

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 100),
    )..repeat();

    _controller.addListener(() {
      if (widget.isRecording) {
        setState(() {
          for (int i = 0; i < _amplitudes.length; i++) {
            _amplitudes[i] = _random.nextDouble() * 0.8 + 0.2;
          }
        });
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: WaveformPainter(
        amplitudes: _amplitudes,
        color: Colors.red,
      ),
      size: Size.infinite,
    );
  }
}

class WaveformPainter extends CustomPainter {
  final List<double> amplitudes;
  final Color color;

  WaveformPainter({
    required this.amplitudes,
    required this.color,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round;

    final barWidth = size.width / amplitudes.length;

    for (int i = 0; i < amplitudes.length; i++) {
      final x = i * barWidth + barWidth / 2;
      final barHeight = amplitudes[i] * size.height;
      final y1 = (size.height - barHeight) / 2;
      final y2 = y1 + barHeight;

      canvas.drawLine(Offset(x, y1), Offset(x, y2), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
