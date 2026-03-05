import 'package:flutter/material.dart';
import 'widgets/module_card.dart';
import '../../widgets/common/custom_button.dart';

class ModuleSelectionPage extends StatefulWidget {
  const ModuleSelectionPage({Key? key}) : super(key: key);

  @override
  State<ModuleSelectionPage> createState() => _ModuleSelectionPageState();
}

class _ModuleSelectionPageState extends State<ModuleSelectionPage> {
  final List<String> _selectedModules = [];

  final List<Map<String, dynamic>> _modules = [
    {
      'id': 'writing',
      'title': 'Writing',
      'icon': Icons.edit_note_rounded,
      'color': const Color(0xFF6C63FF),
      'description': 'Master Task 1 & Task 2 with AI feedback',
      'features': [
        'Real-time grammar correction',
        'Vocabulary enhancement',
        'Band score prediction',
        'Personalized improvement tips',
      ],
      'estimatedDuration': '4-8 weeks',
      'practiceCount': '100+ exercises',
    },
    {
      'id': 'speaking',
      'title': 'Speaking',
      'icon': Icons.mic_rounded,
      'color': const Color(0xFFFF6584),
      'description': 'Practice with AI tutor, improve fluency',
      'features': [
        'Pronunciation analysis',
        'Fluency assessment',
        'Part 1, 2, 3 practice',
        'Mock interviews',
      ],
      'estimatedDuration': '6-10 weeks',
      'practiceCount': '150+ topics',
    },
    {
      'id': 'reading',
      'title': 'Reading',
      'icon': Icons.menu_book_rounded,
      'color': const Color(0xFF00D4FF),
      'description': 'Speed reading & comprehension strategies',
      'features': [
        'Timed practice tests',
        'Strategy guides',
        'Answer explanations',
        'Progress tracking',
      ],
      'estimatedDuration': '3-6 weeks',
      'practiceCount': '80+ passages',
    },
    {
      'id': 'listening',
      'title': 'Listening',
      'icon': Icons.headphones_rounded,
      'color': const Color(0xFF4CAF50),
      'description': 'Train your ears with diverse accents',
      'features': [
        'Multiple accents (UK, US, AUS)',
        'Section-wise practice',
        'Speed adjustment',
        'Transcripts available',
      ],
      'estimatedDuration': '4-7 weeks',
      'practiceCount': '120+ audios',
    },
  ];

  void _toggleModule(String moduleId) {
    setState(() {
      if (_selectedModules.contains(moduleId)) {
        _selectedModules.remove(moduleId);
      } else {
        _selectedModules.add(moduleId);
      }
    });
  }

  void _proceedToGoalSetting() {
    if (_selectedModules.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select at least one module'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    // For now, navigate to goal setting for the first selected module
    Navigator.pushNamed(
      context,
      '/goal-setting',
      arguments: {'moduleId': _selectedModules.first},
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Choose Your Module'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'What would you like to master?',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Select one or more modules to get started',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.grey[600],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Module Cards
                  ...List.generate(_modules.length, (index) {
                    final module = _modules[index];
                    final isSelected = _selectedModules.contains(module['id']);

                    return Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: ModuleCard(
                        module: module,
                        isSelected: isSelected,
                        onTap: () => _toggleModule(module['id']),
                      ),
                    );
                  }),
                ],
              ),
            ),
          ),

          // Bottom Action Bar
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
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (_selectedModules.isNotEmpty)
                    Container(
                      padding: const EdgeInsets.all(12),
                      margin: const EdgeInsets.only(bottom: 16),
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            Icons.info_outline,
                            color: Theme.of(context).primaryColor,
                            size: 20,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              '${_selectedModules.length} module${_selectedModules.length > 1 ? 's' : ''} selected',
                              style: TextStyle(
                                color: Theme.of(context).primaryColor,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  CustomButton(
                    text: 'Continue',
                    onPressed: _proceedToGoalSetting,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
