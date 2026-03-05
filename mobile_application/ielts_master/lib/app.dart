import 'package:flutter/material.dart';
import 'core/theme/app_theme.dart';
import 'config/routes/route_generator.dart';

class IELTSMasterApp extends StatelessWidget {
  const IELTSMasterApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'IELTS Master',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      initialRoute: '/',
      onGenerateRoute: RouteGenerator.generateRoute,
    );
  }
}
