import express from 'express';
import { analyzeMentalHealthData } from '../controllers/mentalHealthAnalysisController.js';

const router = express.Router();

// Mental health analysis route
router.post('/mental-health-analysis', analyzeMentalHealthData);

export default router; 