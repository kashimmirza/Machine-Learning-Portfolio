/ backend/routes/reading.js
const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/auth');
const ReadingService = require('../services/readingService');

// Get reading passages
router.get('/passages', authMiddleware, async (req, res) => {
  try {
    const { difficulty } = req.query;
    const passages = await ReadingService.getPassages(difficulty);
    res.json(passages);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Submit reading test
router.post('/submit', authMiddleware, async (req, res) => {
  try {
    const { passageId, answers, timeSpent } = req.body;
    const userId = req.user.id;

    const result = await ReadingService.evaluateAnswers({
      userId,
      passageId,
      answers,
      timeSpent,
    });

    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
