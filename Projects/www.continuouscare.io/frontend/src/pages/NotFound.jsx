import { Link } from 'react-router-dom'

export default function NotFound() {
    return (
        <div className="min-h-screen pt-24 pb-12 flex items-center justify-center">
            <div className="text-center">
                <h1 className="text-6xl font-bold text-slate-dark mb-4">404</h1>
                <p className="text-xl text-slate-700 mb-6">Page not found</p>
                <Link to="/" className="text-blue-vibrant hover:text-blue-accent">
                    Go back home
                </Link>
            </div>
        </div>
    )
}
