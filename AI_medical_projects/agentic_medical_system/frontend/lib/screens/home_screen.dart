import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import 'analysis_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              FadeInDown(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Welcome Back,",
                          style: TextStyle(
                              fontSize: 16, color: Colors.grey, fontWeight: FontWeight.w500),
                        ),
                        Text(
                          "Dr. User",
                          style: TextStyle(
                              fontSize: 24, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    CircleAvatar(
                      radius: 24,
                      backgroundColor: Colors.blue.withOpacity(0.1),
                      child: const Icon(Icons.person, color: Colors.blue),
                    )
                  ],
                ),
              ),
              const SizedBox(height: 32),
              FadeInUp(
                delay: const Duration(milliseconds: 200),
                child: _buildActionCard(
                  context,
                  title: "New Analysis",
                  subtitle: "Scan or upload Image",
                  icon: Icons.add_a_photo,
                  color: Theme.of(context).colorScheme.primary,
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const AnalysisScreen()),
                    );
                  },
                ),
              ),
              const SizedBox(height: 16),
              FadeInUp(
                delay: const Duration(milliseconds: 400),
                child: _buildActionCard(
                  context,
                  title: "History",
                  subtitle: "View past reports",
                  icon: Icons.history,
                  color: Colors.orangeAccent,
                  isSecondary: true,
                  onTap: () {
                    // Navigate to history
                  },
                ),
              ),
              const SizedBox(height: 32),
              const Text(
                "Recent Cases",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: ListView.separated(
                  itemCount: 5,
                  separatorBuilder: (_, __) => const SizedBox(height: 12),
                  itemBuilder: (context, index) {
                    return FadeInLeft(
                      delay: Duration(milliseconds: 600 + (index * 100)),
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Theme.of(context).cardColor,
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                             BoxShadow(
                              color: Colors.black.withOpacity(0.05),
                              blurRadius: 10,
                              offset: const Offset(0, 4),
                            )
                          ]
                        ),
                        child: Row(
                          children: [
                            Container(
                              width: 50,
                              height: 50,
                              decoration: BoxDecoration(
                                color: Colors.blue.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: const Icon(Icons.description, color: Colors.blue),
                            ),
                            const SizedBox(width: 16),
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text("Case #10${23 + index}", style: const TextStyle(fontWeight: FontWeight.bold)),
                                const Text("CT Scan - Thorax", style: TextStyle(color: Colors.grey, fontSize: 13)),
                              ],
                            ),
                            const Spacer(),
                            const Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildActionCard(BuildContext context,
      {required String title,
      required String subtitle,
      required IconData icon,
      required Color color,
      required VoidCallback onTap,
      bool isSecondary = false}) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: 140,
        decoration: BoxDecoration(
          color: isSecondary ? Theme.of(context).cardColor : color,
          borderRadius: BorderRadius.circular(24),
          border: isSecondary ? Border.all(color: Colors.grey.withOpacity(0.2)) : null,
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.3),
              blurRadius: 20,
              offset: const Offset(0, 8),
            )
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                          color: isSecondary ? Colors.black : Colors.white),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      subtitle,
                      style: TextStyle(
                          fontSize: 14,
                          color: isSecondary ? Colors.grey : Colors.white.withOpacity(0.8)),
                    ),
                  ],
                ),
              ),
              Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(isSecondary ? 0.0 : 0.2),
                   borderRadius: BorderRadius.circular(16),
                ),
                 child: Icon(icon, size: 30, color: isSecondary ? color : Colors.white),
              )
            ],
          ),
        ),
      ),
    );
  }
}
