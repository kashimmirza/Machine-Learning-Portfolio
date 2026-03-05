import express from 'express';
import { analyzeHealthData } from '../controllers/healthAnalysisController.js';

const router = express.Router();

// Health analysis route
router.post('/health-analysis', analyzeHealthData);

export default router; 