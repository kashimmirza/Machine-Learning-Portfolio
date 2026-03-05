import express from 'express';
import { chatWithAssistant } from '../controllers/chatController.js';
import authUser from '../middleware/authUser.js';

const chatRouter = express.Router();

// Main chat route (requires auth)
chatRouter.post('/', authUser, chatWithAssistant);

export default chatRouter; 