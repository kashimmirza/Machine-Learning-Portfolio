import 'package:flutter/material.dart';
import '../../presentation/pages/splash/splash_page.dart';
import '../../presentation/pages/module_selection/module_selection_page.dart';
import '../../presentation/pages/auth/login_page.dart';
import '../../presentation/pages/gola_setting/goal_setting_page.dart';
import '../../presentation/pages/assessment/level_test_page.dart';

class RouteGenerator {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case '/':
        return MaterialPageRoute(
          builder: (_) => const SplashPage(),
        );
      case '/modules':
        return MaterialPageRoute(
          builder: (_) => const ModuleSelectionPage(),
        );
      case '/login':
        return MaterialPageRoute(
          builder: (_) => const LoginPage(),
        );
      case '/goal-setting':
        final args = settings.arguments as Map<String, dynamic>?;
        final moduleId = args?['moduleId'] as String? ?? 'writing';
        return MaterialPageRoute(
          builder: (_) => GoalSettingPage(moduleId: moduleId),
        );
      case '/assessment':
        final args = settings.arguments as Map<String, dynamic>?;
        final moduleId = args?['moduleId'] as String? ?? 'writing';
        final targetScore = args?['targetScore'] as double? ?? 7.0;
        return MaterialPageRoute(
          builder: (_) => LevelTestPage(
            moduleId: moduleId,
            targetScore: targetScore,
          ),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            appBar: AppBar(
              title: const Text('Page Not Found'),
            ),
            body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Route not found: ${settings.name}'),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () =>
                        Navigator.of(_).pushReplacementNamed('/modules'),
                    child: const Text('Go to Modules'),
                  ),
                ],
              ),
            ),
          ),
        );
    }
  }
}
