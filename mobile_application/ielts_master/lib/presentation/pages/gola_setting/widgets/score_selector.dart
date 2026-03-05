import 'package:flutter/material.dart';

class ScoreSelector extends StatefulWidget {
  final double score;
  final Function(double) onChanged;

  const ScoreSelector({
    Key? key,
    required this.score,
    required this.onChanged,
  }) : super(key: key);

  @override
  State<ScoreSelector> createState() => _ScoreSelectorState();
}

class _ScoreSelectorState extends State<ScoreSelector> {
  late double _selectedScore;

  @override
  void initState() {
    super.initState();
    _selectedScore = widget.score;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Target Score',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: Colors.grey[700],
                ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: Theme.of(context).primaryColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _selectedScore.toStringAsFixed(1),
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).primaryColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Slider(
            value: _selectedScore,
            min: 1.0,
            max: 9.0,
            divisions: 16,
            activeColor: Theme.of(context).primaryColor,
            onChanged: (value) {
              setState(() {
                _selectedScore = value;
              });
              widget.onChanged(value);
            },
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '1.0',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
              ),
              Text(
                '9.0',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
