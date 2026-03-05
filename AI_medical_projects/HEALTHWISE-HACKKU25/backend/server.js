/** @format */

import express from "express";
import cors from "cors";
import "dotenv/config";
import connectDB from "./config/mongodb.js";
import connectCloudinary from "./config/cloudinary.js";
import userRouter from "./routes/userRoute.js";
import doctorRouter from "./routes/doctorRoute.js";
import adminRouter from "./routes/adminRoute.js";
import chatRouter from "./routes/chatRoute.js";
import fileRouter from "./routes/fileRoutes.js";
import healthAnalysisRouter from "./routes/healthAnalysisRoutes.js";
import mentalHealthAnalysisRouter from "./routes/mentalHealthAnalysisRoutes.js";
import dotenv from "dotenv";
dotenv.config();

// app config
const app = express();
const port = process.env.PORT || 5000;
console.log(`Server is running on port ${port}`);
connectDB();
connectCloudinary();

// middlewares
app.use(express.json());
app.use(cors());

// api endpoints
app.use("/api/user", userRouter);
app.use("/api/admin", adminRouter);
app.use("/api/doctor", doctorRouter);
app.use("/api/chat", chatRouter);
app.use("/api/file", fileRouter);
app.use("/api", healthAnalysisRouter);
app.use("/api", mentalHealthAnalysisRouter);
app.get("/", (req, res) => {
 res.send("API Working");
});

app.listen(port, () => console.log(`Server started on PORT:${port}`));
