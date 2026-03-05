import express from 'express';
import { uploadFile } from '../controllers/fileController.js';
// import { authenticateToken } from '../middleware/authMiddleware.js';
import authUser from '../middleware/authUser.js';

const router = express.Router();

router.post('/upload', authUser, uploadFile);

export default router; 