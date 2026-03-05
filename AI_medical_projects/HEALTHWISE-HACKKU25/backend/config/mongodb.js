/** @format */

// import dotenv from "dotenv";

// import mongoose from "mongoose";
// import express from "express";
// const connectDB = async () => {
//     try {
//         // Set up event listeners
//         mongoose.connection.on('connected', () => {
//             console.log("MongoDB Connected Successfully");
//         });

//         mongoose.connection.on('error', (err) => {
//             console.error("MongoDB Connection Error:", err);
//         });

//         mongoose.connection.on('disconnected', () => {
//             console.log("MongoDB Disconnected");
//         });

//         // Connect to MongoDB
//         await mongoose.connect(process.env.MONGODB_URI, {
//             dbName: 'prescripto',
//             serverSelectionTimeoutMS: 5000, // Timeout after 5s instead of 30s
//             socketTimeoutMS: 45000, // Close sockets after 45s of inactivity
//         });

//         console.log("MongoDB Connection Initialized");
//     } catch (error) {
//         console.error("MongoDB Connection Error:", error);
//         process.exit(1);
//     }
// }

// export default connectDB;

// // Do not use '@' symbol in your databse user's password else it will show an error.

// config/mongodb.js

import dotenv from "dotenv";
import mongoose from "mongoose";

// Load environment variables
dotenv.config();

const connectDB = async () => {
 try {
  const mongoUri = process.env.MONGODB_URI;

  if (!mongoUri) {
   throw new Error("MONGODB_URI is not defined in the .env file.");
  }

  // Event listeners for MongoDB connection
  mongoose.connection.on("connected", () => {
   console.log("✅ MongoDB Connected Successfully");
  });

  mongoose.connection.on("error", (err) => {
   console.error("❌ MongoDB Connection Error:", err);
  });

  mongoose.connection.on("disconnected", () => {
   console.log("⚠️ MongoDB Disconnected");
  });

  // Connect to MongoDB
  await mongoose.connect(mongoUri, {
   dbName: "prescripto",
   serverSelectionTimeoutMS: 5000,
   socketTimeoutMS: 45000,
  });

  console.log("🚀 MongoDB Connection Initialized");
 } catch (error) {
  console.error("❌ MongoDB Connection Error:", error.message);
  process.exit(1);
 }
};

export default connectDB;
