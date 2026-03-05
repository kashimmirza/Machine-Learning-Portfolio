/** @format */

// backend/server.js
const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const mongoose = require("mongoose");
require("dotenv").config();

const authRoutes = require("./routes/auth");
const writingRoutes = require("./routes/writing");
const userRoutes = require("./routes/user");
const paymentRoutes = require("./routes/payment");

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan("dev"));
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));

// Database connection
mongoose
 .connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
 })
 .then(() => console.log("✅ MongoDB connected"))
 .catch((err) => console.error("❌ MongoDB connection error:", err));

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/writing", writingRoutes);
app.use("/api/user", userRoutes);
app.use("/api/payment", paymentRoutes);

// Health check
app.get("/health", (req, res) => {
 res.json({ status: "ok", timestamp: new Date() });
});

// Error handler
app.use((err, req, res, next) => {
 console.error(err.stack);
 res.status(err.status || 500).json({
  error: err.message || "Internal server error",
 });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
 console.log(`🚀 Server running on port ${PORT}`);
});

// backend/routes/writing.js
const express = require("express");
const router = express.Router();
const authMiddleware = require("../middleware/auth");
const WritingService = require("../services/writingService");
const AIService = require("../services/aiService");

// Get writing prompts
router.get("/prompts", authMiddleware, async (req, res) => {
 try {
  const { taskType, difficulty } = req.query;
  const prompts = await WritingService.getPrompts(taskType, difficulty);
  res.json(prompts);
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

// Submit writing for assessment
router.post("/assess", authMiddleware, async (req, res) => {
 try {
  const { taskType, prompt, answer, timeSpent } = req.body;
  const userId = req.user.id;

  // Call AI service for assessment
  const assessment = await AIService.assessWriting({
   taskType,
   prompt,
   answer,
   userId,
   timeSpent,
  });

  // Save to database
  const session = await WritingService.saveSession({
   userId,
   taskType,
   prompt,
   answer,
   wordCount: answer.trim().split(/\s+/).length,
   timeSpent,
   score: assessment.score,
   errors: assessment.errors,
   feedback: assessment.feedback,
   suggestions: assessment.suggestions,
  });

  res.json({
   id: session._id,
   score: assessment.score,
   errors: assessment.errors,
   feedback: assessment.feedback,
   suggestions: assessment.suggestions,
   createdAt: session.createdAt,
  });
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

// Real-time analysis
router.post("/analyze-realtime", authMiddleware, async (req, res) => {
 try {
  const { text } = req.body;

  const analysis = await AIService.analyzeTextRealtime(text);

  res.json({
   errors: analysis.errors,
   suggestions: analysis.suggestions,
   metrics: {
    wordCount: text.trim().split(/\s+/).length,
    sentenceCount: text.split(/[.!?]+/).length - 1,
    avgWordLength: analysis.avgWordLength,
   },
  });
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

// Get user's writing history
router.get("/sessions", authMiddleware, async (req, res) => {
 try {
  const userId = req.user.id;
  const sessions = await WritingService.getUserSessions(userId);
  res.json(sessions);
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

// Get detailed feedback for a session
router.get("/feedback/:sessionId", authMiddleware, async (req, res) => {
 try {
  const { sessionId } = req.params;
  const feedback = await WritingService.getDetailedFeedback(sessionId);
  res.json(feedback);
 } catch (error) {
  res.status(500).json({ error: error.message });
 }
});

module.exports = router;

// backend/services/aiService.js
const OpenAI = require("openai");

const openai = new OpenAI({
 apiKey: process.env.OPENAI_API_KEY,
});

class AIService {
 /**
  * Assess IELTS writing using GPT-4
  */
 static async assessWriting({ taskType, prompt, answer, timeSpent }) {
  const systemPrompt = this.buildAssessmentPrompt(taskType);

  try {
   const completion = await openai.chat.completions.create({
    model: "gpt-4-turbo-preview",
    messages: [
     { role: "system", content: systemPrompt },
     {
      role: "user",
      content: `Task Prompt:\n${prompt}\n\nStudent's Answer:\n${answer}`,
     },
    ],
    response_format: { type: "json_object" },
    temperature: 0.3,
   });

   const result = JSON.parse(completion.choices[0].message.content);

   return {
    score: {
     overall: result.overall_score,
     taskAchievement: result.task_achievement,
     coherenceCohesion: result.coherence_cohesion,
     lexicalResource: result.lexical_resource,
     grammaticalAccuracy: result.grammatical_accuracy,
    },
    errors: result.errors || [],
    feedback: result.feedback,
    suggestions: result.suggestions || [],
   };
  } catch (error) {
   console.error("AI Assessment Error:", error);
   throw new Error("Failed to assess writing");
  }
 }

 /**
  * Real-time text analysis for grammar and style
  */
 static async analyzeTextRealtime(text) {
  try {
   const completion = await openai.chat.completions.create({
    model: "gpt-4-turbo-preview",
    messages: [
     {
      role: "system",
      content: `You are an IELTS writing tutor. Analyze the text for grammar errors, vocabulary issues, and provide quick suggestions. Return JSON with:
{
  "errors": [
    {
      "type": "grammar|vocabulary|structure",
      "category": "specific error type",
      "text": "error text",
      "correction": "corrected text",
      "explanation": "brief explanation",
      "severity": "error|warning|suggestion",
      "position": {"start": 0, "end": 10}
    }
  ],
  "suggestions": ["suggestion 1", "suggestion 2"],
  "avgWordLength": 5.2
}`,
     },
     { role: "user", content: text },
    ],
    response_format: { type: "json_object" },
    temperature: 0.2,
    max_tokens: 1500,
   });

   return JSON.parse(completion.choices[0].message.content);
  } catch (error) {
   console.error("Real-time Analysis Error:", error);
   return { errors: [], suggestions: [], avgWordLength: 0 };
  }
 }

 /**
  * Build assessment prompt based on task type
  */
 static buildAssessmentPrompt(taskType) {
  const criteria =
   taskType === "task1"
    ? "Task 1 criteria (describing visual information accurately and coherently)"
    : "Task 2 criteria (presenting and supporting an argument)";

  return `You are an expert IELTS examiner. Assess this ${taskType.toUpperCase()} writing response according to official IELTS ${criteria}.

Provide a detailed assessment with scores (0.0-9.0, in 0.5 increments) for:
1. Task Achievement (how well the task requirements are met)
2. Coherence & Cohesion (organization, linking, paragraphing)
3. Lexical Resource (vocabulary range and accuracy)
4. Grammatical Range & Accuracy

Also identify specific errors with corrections and explanations.

Return ONLY valid JSON in this exact format:
{
  "overall_score": 7.0,
  "task_achievement": 7.0,
  "coherence_cohesion": 7.5,
  "lexical_resource": 6.5,
  "grammatical_accuracy": 7.0,
  "errors": [
    {
      "type": "grammar",
      "category": "subject-verb agreement",
      "text": "The data show",
      "correction": "The data shows",
      "explanation": "Data is singular in this context",
      "position": {"start": 45, "end": 59}
    }
  ],
  "feedback": "Detailed paragraph explaining strengths and areas for improvement",
  "suggestions": [
    "Use more varied linking phrases",
    "Expand vocabulary in the conclusion",
    "Check articles (a/an/the) usage"
  ]
}`;
 }
}

module.exports = AIService;

// backend/services/writingService.js
const WritingSession = require("../models/WritingSession");
const WritingPrompt = require("../models/WritingPrompt");

class WritingService {
 static async getPrompts(taskType, difficulty = "medium") {
  const prompts = await WritingPrompt.find({
   taskType,
   difficulty,
   isActive: true,
  }).limit(10);

  return prompts;
 }

 static async saveSession(sessionData) {
  const session = new WritingSession(sessionData);
  await session.save();
  return session;
 }

 static async getUserSessions(userId, limit = 20) {
  const sessions = await WritingSession.find({ userId })
   .sort({ createdAt: -1 })
   .limit(limit)
   .select("-answer"); // Don't send full answer in list

  return sessions;
 }

 static async getDetailedFeedback(sessionId) {
  const session = await WritingSession.findById(sessionId);

  if (!session) {
   throw new Error("Session not found");
  }

  return {
   id: session._id,
   taskType: session.taskType,
   prompt: session.prompt,
   answer: session.answer,
   wordCount: session.wordCount,
   timeSpent: session.timeSpent,
   score: session.score,
   errors: session.errors,
   feedback: session.feedback,
   suggestions: session.suggestions,
   createdAt: session.createdAt,
  };
 }
}

module.exports = WritingService;

// backend/models/WritingSession.js
const mongoose = require("mongoose");

const writingSessionSchema = new mongoose.Schema({
 userId: {
  type: mongoose.Schema.Types.ObjectId,
  ref: "User",
  required: true,
 },
 taskType: {
  type: String,
  enum: ["task1", "task2"],
  required: true,
 },
 prompt: {
  type: String,
  required: true,
 },
 answer: {
  type: String,
  required: true,
 },
 wordCount: {
  type: Number,
  required: true,
 },
 timeSpent: {
  type: Number, // in seconds
  required: true,
 },
 score: {
  overall: { type: Number, min: 0, max: 9 },
  taskAchievement: { type: Number, min: 0, max: 9 },
  coherenceCohesion: { type: Number, min: 0, max: 9 },
  lexicalResource: { type: Number, min: 0, max: 9 },
  grammaticalAccuracy: { type: Number, min: 0, max: 9 },
 },
 errors: [
  {
   type: String,
   category: String,
   text: String,
   correction: String,
   explanation: String,
   position: {
    start: Number,
    end: Number,
   },
  },
 ],
 feedback: String,
 suggestions: [String],
 createdAt: {
  type: Date,
  default: Date.now,
 },
});

// Index for faster queries
writingSessionSchema.index({ userId: 1, createdAt: -1 });

module.exports = mongoose.model("WritingSession", writingSessionSchema);

// backend/.env.example
/*
NODE_ENV=development
PORT=3000

# Database
MONGODB_URI=mongodb://localhost:27017/ielts_master

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# JWT
JWT_SECRET=your-secret-key-here
JWT_EXPIRE=7d

# Payment
STRIPE_SECRET_KEY=sk_test_...
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=your-secret

# Firebase Admin (for auth)
FIREBASE_ADMIN_SDK=./firebase-admin-sdk.json

# AWS S3 (for file uploads)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_BUCKET_NAME=ielts-master-uploads
AWS_REGION=us-east-1
*/

// backend/package.json
/*
{
  "name": "ielts-master-backend",
  "version": "1.0.0",
  "description": "IELTS Master Backend API",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^8.0.3",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "morgan": "^1.10.0",
    "dotenv": "^16.3.1",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.2",
    "openai": "^4.24.1",
    "stripe": "^14.10.0",
    "razorpay": "^2.9.2",
    "firebase-admin": "^12.0.0",
    "aws-sdk": "^2.1517.0",
    "multer": "^1.4.5-lts.1",
    "nodemailer": "^6.9.7",
    "joi": "^17.11.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.2",
    "jest": "^29.7.0"
  }
}
*/
