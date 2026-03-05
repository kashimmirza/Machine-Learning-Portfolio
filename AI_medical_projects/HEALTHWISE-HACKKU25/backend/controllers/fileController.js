import { GoogleGenerativeAI } from '@google/generative-ai';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { promisify } from 'util';
import pdf from "pdf-parse/lib/pdf-parse.js";
 
// Configure multer for file upload
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadDir = 'uploads';
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir);
        }
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});

const upload = multer({
    storage: storage,
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'application/pdf') {
            cb(null, true);
        } else {
            cb(new Error('Only PDF files are allowed'), false);
        }
    },
    limits: {
        fileSize: 5 * 1024 * 1024 // 5MB limit
    }
}).single('file');

const uploadFile = async (req, res) => {
    try {
        await promisify(upload)(req, res);

        if (!req.file) {
            return res.status(400).json({
                success: false,
                message: 'No file uploaded'
            });
        }
        
        var inputMessage = ""
        if (req.body.metadata) {
            const metadata = JSON.parse(req.body.metadata);
            inputMessage = metadata.message;
        }

        console.log(`Message is ${inputMessage}`);

        // Read and parse the PDF

        console.log(`INFO ${JSON.stringify(req.file.path)}`);
        const pdfData = await pdf(req.file.path);
        console.log(`DATA IS ${pdfData.text}`);
        // 
        // Initialize Gemini
        const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
        const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

        // Create a prompt with the PDF content
        const prompt = `
        You are a medical assistant. Analyze the following medical document thoroughly:

        ${pdfData.text}

        Based on this document, respond accurately to the user’s question below:

        User query: "${inputMessage}"

        Answer the query using relevant information from the document only. If the answer is not available in the document, say so clearly.
        `;

        // Generate content
        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        // // Store the PDF content in the session for future reference
        // req.session.pdfContent = pdfData.text;

        res.json({
            success: true,
            message: text
        });
    } catch (error) {
        console.error('File upload error:', error);
        res.status(500).json({
            success: false,
            message: 'Error processing the file'
        });
    }
};

const extract = async (filePath) => {
    console.log("AT EXTRACT");
    const pdf = await pdfjsLib.getDocument(filePath).promise;
    let text = '';

    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const content = await page.getTextContent();
      const strings = content.items.map((item) => item.str);
      text += strings.join(' ') + '\n';
    }
    console.log("PARSED DATA");
    console.log(`${text}`)

    return text;
}

export { uploadFile }; 
