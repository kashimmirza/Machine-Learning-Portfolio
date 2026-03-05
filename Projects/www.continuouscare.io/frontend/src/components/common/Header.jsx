import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function Header() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
    const [platformMenuOpen, setPlatformMenuOpen] = useState(false)
    const [solutionsMenuOpen, setSolutionsMenuOpen] = useState(false)

    return (
        <header className="fixed w-full z-50 transition-all duration-300 bg-white shadow-sm py-4">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="relative flex items-center justify-between">
                    {/* Logo */}
                    <div className="flex items-center justify-between">
                        <Link to="/">
                            <img
                                alt="ContinuousCare"
                                width="100"
                                height="100"
                                className="h-8 w-auto"
                                src="/cc-logo.svg"
                            />
                        </Link>
                    </div>

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex items-center gap-1 lg:gap-3">
                        {/* Platform Dropdown */}
                        <div
                            className="relative"
                            onMouseEnter={() => setPlatformMenuOpen(true)}
                            onMouseLeave={() => setPlatformMenuOpen(false)}
                        >
                            <button className="flex items-center text-xs md:text-sm text-slate-800 hover:text-blue-vibrant px-1 md:px-2 py-2 whitespace-nowrap">
                                Platform
                                <svg className="w-3.5 h-3.5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>
                        </div>

                        {/* Solutions Dropdown */}
                        <div
                            className="relative"
                            onMouseEnter={() => setSolutionsMenuOpen(true)}
                            onMouseLeave={() => setSolutionsMenuOpen(false)}
                        >
                            <button className="flex items-center text-xs md:text-sm text-slate-800 hover:text-blue-vibrant px-1 md:px-2 py-2 whitespace-nowrap">
                                Solutions
                                <svg className="w-3.5 h-3.5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>
                        </div>

                        <Link className="text-xs md:text-sm text-slate-800 hover:text-blue-vibrant px-1 md:px-2 py-2 whitespace-nowrap" to="/pricing">
                            Pricing
                        </Link>
                        <Link className="text-xs md:text-sm text-slate-800 hover:text-blue-vibrant px-1 md:px-2 py-2 whitespace-nowrap" to="/blog">
                            Blog
                        </Link>
                    </nav>

                    {/* Get Started Button */}
                    <div className="hidden md:flex items-center gap-3">
                        <Link to="/register">
                            <button className="inline-flex items-center justify-center font-medium transition-all duration-200 rounded-md px-4 py-2 text-sm bg-blue-vibrant text-white hover:bg-blue-accent shadow-sm">
                                Get Started
                            </button>
                        </Link>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        className="md:hidden text-slate-800"
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    >
                        <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </header>
    )
}
