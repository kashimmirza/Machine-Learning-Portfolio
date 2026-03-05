import { GoogleGenerativeAI } from '@google/generative-ai';

// Queue system for managing requests
const requestQueue = [];
let isProcessing = false;

// Rate limiting configuration
const RATE_LIMIT = {
    maxRequestsPerMinute: 5,
    maxTokensPerMinute: 150,
    requests: [],
    tokens: [],
    lastErrorTime: 0,
    errorRetryDelay: 20000
};

// Helper function to clean up old requests
const cleanupOldRequests = (requests, timeWindow) => {
    const now = Date.now();
    return requests.filter(time => now - time < timeWindow);
};

// Helper function to check if we should wait due to rate limits
const shouldWaitForRateLimit = () => {
    const now = Date.now();
    const oneMinuteAgo = now - 60000;
    
    // Clean up old requests
    RATE_LIMIT.requests = cleanupOldRequests(RATE_LIMIT.requests, 60000);
    RATE_LIMIT.tokens = cleanupOldRequests(RATE_LIMIT.tokens, 60000);
    
    // Check if we've hit the rate limits
    if (RATE_LIMIT.requests.length >= RATE_LIMIT.maxRequestsPerMinute) {
        return true;
    }
    
    // Check if we're still in the error retry delay period
    if (now - RATE_LIMIT.lastErrorTime < RATE_LIMIT.errorRetryDelay) {
        return true;
    }
    
    return false;
};

// Process the queue
const processQueue = async () => {
    if (isProcessing || requestQueue.length === 0) return;
    
    if (shouldWaitForRateLimit()) {
        setTimeout(processQueue, 1000);
        return;
    }
    
    isProcessing = true;
    const { req, res } = requestQueue.shift();
    
    try {
        const { message } = req.body;
        
        if (!message) {
            res.json({ success: false, message: 'Message is required' });
            isProcessing = false;
            processQueue();
            return;
        }

        // Initialize Gemini
        const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
        const model = genAI.getGenerativeModel({ 
            model: "gemini-2.0-flash",
        });

        // Create a prompt with context
        const prompt = `You are a medical assistant. Your role is to provide general medical information, answer health-related questions, and offer guidance on common health concerns. However, you should always remind users that you are not a substitute for professional medical advice, diagnosis, or treatment. For serious medical conditions or emergencies, users should always consult a qualified healthcare provider.

User question: ${message}`;

        // Generate content
        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        // Update rate limit counters
        RATE_LIMIT.requests.push(Date.now());
        
        res.json({ success: true, message: text });
    } catch (error) {
        console.error('Chat error:', error);
        
        if (error.message.includes('429 Too Many Requests') || 
            error.message.includes('quota')) {
            RATE_LIMIT.lastErrorTime = Date.now();
            res.status(429).json({ 
                success: false, 
                message: 'Rate limit exceeded. Please try again in a few moments.',
                retryAfter: RATE_LIMIT.errorRetryDelay / 1000
            });
        } else {
            res.status(500).json({ 
                success: false, 
                message: 'An error occurred while processing your request.' 
            });
        }
    } finally {
        isProcessing = false;
        processQueue();
    }
};

const chatWithAssistant = async (req, res) => {
    // Add request to queue
    requestQueue.push({ req, res });
    
    // If queue was empty, start processing
    if (requestQueue.length === 1) {
        processQueue();
    }
};

export { chatWithAssistant }; 