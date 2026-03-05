// lib/presentation/pages/assessment/assessment_result_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../widgets/common/custom_button.dart';

class AssessmentResultPage extends StatelessWidget {
  final Map<String, dynamic> result;

  const AssessmentResultPage({
    Key? key,
    required this.result,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final overallScore = result['score']['overall'] ?? 0.0;
    final taskAchievement = result['score']['taskAchievement'] ?? 0.0;
    final coherence = result['score']['coherenceCohesion'] ?? 0.0;
    final lexical = result['score']['lexicalResource'] ?? 0.0;
    final grammar = result['score']['grammaticalAccuracy'] ?? 0.0;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Assessment Result'),
        automaticallyImplyLeading: false,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Score Header
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(32),
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
                  const Text(
                    'Your Current Level',
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.white70,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    overallScore.toStringAsFixed(1),
                    style: const TextStyle(
                      fontSize: 72,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ).animate().fadeIn().scale(),
                  const Text(
                    'Band Score',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.white70,
                    ),
                  ),
                  const SizedBox(height: 24),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 20,
                      vertical: 12,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Text(
                      'Intermediate User',
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Score Breakdown
                  const Text(
                    'Score Breakdown',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),

                  _ScoreCriteriaCard(
                    title: 'Task Achievement',
                    score: taskAchievement,
                    description: 'How well you addressed the task',
                    icon: Icons.assignment_turned_in,
                    color: const Color(0xFF6C63FF),
                  ),
                  const SizedBox(height: 12),

                  _ScoreCriteriaCard(
                    title: 'Coherence & Cohesion',
                    score: coherence,
                    description: 'Organization and flow of ideas',
                    icon: Icons.link,
                    color: const Color(0xFF00D4FF),
                  ),
                  const SizedBox(height: 12),

                  _ScoreCriteriaCard(
                    title: 'Lexical Resource',
                    score: lexical,
                    description: 'Vocabulary range and accuracy',
                    icon: Icons.book,
                    color: const Color(0xFF4CAF50),
                  ),
                  const SizedBox(height: 12),

                  _ScoreCriteriaCard(
                    title: 'Grammatical Accuracy',
                    score: grammar,
                    description: 'Grammar and sentence structures',
                    icon: Icons.spellcheck,
                    color: const Color(0xFFFF6584),
                  ),
                  const SizedBox(height: 24),

                  // Key Findings
                  const Text(
                    'Key Findings',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),

                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.green[50],
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.green[200]!),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.check_circle, color: Colors.green[700]),
                            const SizedBox(width: 12),
                            const Text(
                              'Strengths',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        const Text(
                          '• Good use of linking words and phrases\n'
                          '• Clear paragraph structure\n'
                          '• Accurate use of present tense',
                          style: TextStyle(height: 1.6),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.orange[50],
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.orange[200]!),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.trending_up, color: Colors.orange[700]),
                            const SizedBox(width: 12),
                            const Text(
                              'Areas for Improvement',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        const Text(
                          '• Expand vocabulary range\n'
                          '• Use more complex sentence structures\n'
                          '• Pay attention to article usage',
                          style: TextStyle(height: 1.6),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 32),

                  // Action Buttons
                  CustomButton(
                    text: 'View Detailed Feedback',
                    icon: Icons.article,
                    onPressed: () {
                      Navigator.pushNamed(context, '/writing/feedback');
                    },
                  ),
                  const SizedBox(height: 12),

                  CustomButton(
                    text: 'Start Learning',
                    icon: Icons.play_arrow,
                    backgroundColor: Theme.of(context).secondaryColor,
                    onPressed: () {
                      Navigator.pushReplacementNamed(context, '/writing/home');
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ScoreCriteriaCard extends StatelessWidget {
  final String title;
  final double score;
  final String description;
  final IconData icon;
  final Color color;

  const _ScoreCriteriaCard({
    required this.title,
    required this.score,
    required this.description,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        children: [
          Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: color.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(icon, color: color, size: 24),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      description,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ),
              Text(
                score.toStringAsFixed(1),
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: color,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: LinearProgressIndicator(
              value: score / 9.0,
              minHeight: 8,
              backgroundColor: Colors.grey[200],
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
          ),
        ],
      ),
    );
  }
}
