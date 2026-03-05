import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const AgenticMedicalApp());
}

class AgenticMedicalApp extends StatelessWidget {
  const AgenticMedicalApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Agentic Medical AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0055FF), // Professional Medical Blue
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        textTheme: GoogleFonts.interTextTheme(),
        scaffoldBackgroundColor: const Color(0xFFF8FAFC),
      ),
      darkTheme: ThemeData(
         colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0055FF),
          brightness: Brightness.dark,
          surface: const Color(0xFF0F172A),
        ),
        useMaterial3: true,
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
        scaffoldBackgroundColor: const Color(0xFF0F172A),
      ),
      themeMode: ThemeMode.system, // Auto-switch
      home: const HomeScreen(),
    );
  }
}
