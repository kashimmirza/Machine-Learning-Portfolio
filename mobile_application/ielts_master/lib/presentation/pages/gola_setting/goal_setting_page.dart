// lib/presentation/pages/goal_setting/goal_setting_page.dart
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'widgets/score_selector.dart';
import '../../widgets/common/custom_button.dart';

class GoalSettingPage extends StatefulWidget {
  final String moduleId;

  const GoalSettingPage({
    Key? key,
    required this.moduleId,
  }) : super(key: key);

  @override
  State<GoalSettingPage> createState() => _GoalSettingPageState();
}

class _GoalSettingPageState extends State<GoalSettingPage> {
  double _targetScore = 7.0;
  DateTime? _testDate;
  int _studyDaysPerWeek = 5;

  Future<void> _selectTestDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now().add(const Duration(days: 90)),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );

    if (picked != null) {
      setState(() {
        _testDate = picked;
      });
    }
  }

  int get _daysRemaining {
    if (_testDate == null) return 0;
    return _testDate!.difference(DateTime.now()).inDays;
  }

  int get _weeksRemaining {
    return (_daysRemaining / 7).ceil();
  }

  void _proceedToAssessment() {
    if (_testDate == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select your test date'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    Navigator.pushNamed(
      context,
      '/assessment',
      arguments: {
        'moduleId': widget.moduleId,
        'targetScore': _targetScore,
        'testDate': _testDate,
        'studyDaysPerWeek': _studyDaysPerWeek,
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Set Your Goals'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Header
                  const Text(
                    'Let\'s create your personalized study plan',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Help us understand your goals better',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.grey[600],
                    ),
                  ),
                  const SizedBox(height: 32),

                  // Target Score
                  const Text(
                    'Target Band Score',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 16),
                  ScoreSelector(
                    score: _targetScore,
                    onChanged: (value) {
                      setState(() {
                        _targetScore = value;
                      });
                    },
                  ),
                  const SizedBox(height: 32),

                  // Test Date
                  const Text(
                    'When is your test?',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 16),
                  GestureDetector(
                    onTap: _selectTestDate,
                    child: Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.grey[300]!),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            Icons.calendar_today,
                            color: Theme.of(context).primaryColor,
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Text(
                              _testDate == null
                                  ? 'Select test date'
                                  : DateFormat('MMMM dd, yyyy')
                                      .format(_testDate!),
                              style: TextStyle(
                                fontSize: 16,
                                color: _testDate == null
                                    ? Colors.grey[600]
                                    : Colors.black87,
                                fontWeight: _testDate == null
                                    ? FontWeight.normal
                                    : FontWeight.w600,
                              ),
                            ),
                          ),
                          Icon(
                            Icons.arrow_forward_ios,
                            size: 16,
                            color: Colors.grey[400],
                          ),
                        ],
                      ),
                    ),
                  ),

                  if (_testDate != null) ...[
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _StatItem(
                            label: 'Days',
                            value: _daysRemaining.toString(),
                          ),
                          Container(
                            width: 1,
                            height: 40,
                            color: Colors.grey[300],
                          ),
                          _StatItem(
                            label: 'Weeks',
                            value: _weeksRemaining.toString(),
                          ),
                        ],
                      ),
                    ),
                  ],
                  const SizedBox(height: 32),

                  // Study Days Per Week
                  const Text(
                    'How many days per week can you study?',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: List.generate(7, (index) {
                      final day = index + 1;
                      final isSelected = _studyDaysPerWeek == day;

                      return GestureDetector(
                        onTap: () {
                          setState(() {
                            _studyDaysPerWeek = day;
                          });
                        },
                        child: Container(
                          width: 44,
                          height: 44,
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
                          child: Center(
                            child: Text(
                              day.toString(),
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color:
                                    isSelected ? Colors.white : Colors.black87,
                              ),
                            ),
                          ),
                        ),
                      );
                    }),
                  ),
                  const SizedBox(height: 32),

                  // Study Plan Preview
                  if (_testDate != null)
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            Theme.of(context).primaryColor.withOpacity(0.1),
                            Theme.of(context)
                                .colorScheme
                                .secondary
                                .withOpacity(0.1),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(
                                Icons.auto_awesome,
                                color: Theme.of(context).primaryColor,
                              ),
                              const SizedBox(width: 12),
                              const Text(
                                'Your Study Plan',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          _PlanItem(
                            icon: Icons.assignment_outlined,
                            label: 'Total practice sessions',
                            value: '${_weeksRemaining * _studyDaysPerWeek}',
                          ),
                          const SizedBox(height: 12),
                          _PlanItem(
                            icon: Icons.trending_up,
                            label: 'Expected improvement',
                            value:
                                '${(_targetScore - 5.0).toStringAsFixed(1)} bands',
                          ),
                          const SizedBox(height: 12),
                          _PlanItem(
                            icon: Icons.timer_outlined,
                            label: 'Daily study time',
                            value: '45-60 min',
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),
          ),

          // Bottom Button
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
                text: 'Start Assessment',
                icon: Icons.play_arrow,
                onPressed: _proceedToAssessment,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatItem extends StatelessWidget {
  final String label;
  final String value;

  const _StatItem({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
            color: Theme.of(context).primaryColor,
          ),
        ),
        Text(
          label,
          style: TextStyle(
            fontSize: 14,
            color: Colors.grey[600],
          ),
        ),
      ],
    );
  }
}

class _PlanItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _PlanItem({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Colors.grey[600]),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            label,
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey[700],
            ),
          ),
        ),
        Text(
          value,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }
}
