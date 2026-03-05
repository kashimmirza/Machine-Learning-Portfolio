/** @format */

// backend/routes/listening.js
const express = require("express");
const router = express.Router();
const authMiddleware = require("../middleware/auth");
const ListeningService = require("../services/listeningService");

// Get listening audios
router.get("/audios", authMiddleware, async (req, res) => {
 try {
  const { accent, difficulty } = req.query;
  const audios = await ListeningService.getAudios(accent, difficulty);
  res.json(audios);
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

// Submit listening test
router.post("/submit", authMiddleware, async (req, res) => {
 try {
  const { audioId, answers } = req.body;
  const userId = req.user.id;

  const result = await ListeningService.evaluateAnswers({
   userId,
   audioId,
   answers,
  });

  res.json(result);
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

module.exports = router;
