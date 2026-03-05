import jwt from 'jsonwebtoken'

// user authentication middleware
const authUser = async (req, res, next) => {
    try {
        // Check for token in Authorization header
        const authHeader = req.headers.authorization;
        let token;
        
        if (authHeader && authHeader.startsWith('Bearer ')) {
            token = authHeader.split(' ')[1];
        } else {
            // Fallback to token in headers
            token = req.headers.token;
        }

        if (!token) {
            return res.json({ success: false, message: 'Not Authorized Login Again' })
        }

        const token_decode = jwt.verify(token, process.env.JWT_SECRET)
        req.body.userId = token_decode.id
        next()
    } catch (error) {
        console.log('Auth error:', error)
        res.json({ success: false, message: 'Not Authorized Login Again' })
    }
}

export default authUser;