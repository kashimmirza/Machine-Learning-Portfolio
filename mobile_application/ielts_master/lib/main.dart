import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'app.dart';
import 'presentation/providers/auth_provider.dart';
import 'presentation/providers/user_provider.dart';
import 'presentation/providers/module_provider.dart';
import 'presentation/providers/writing_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => UserProvider()),
        ChangeNotifierProvider(create: (_) => ModuleProvider()),
        ChangeNotifierProvider(create: (_) => WritingProvider()),
      ],
      child: const IELTSMasterApp(),
    ),
  );
}
