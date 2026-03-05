/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'blue-vibrant': '#0891b2',
                'blue-accent': '#0ea5e9',
                'blue-light': '#e0f2fe',
                'teal-primary': '#14b8a6',
                'green-success': '#10b981',
                'purple-accent': '#8b5cf6',
                'slate-dark': '#1e293b',
                'gray-light': '#f8fafc',
            },
            fontFamily: {
                'sans': ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
