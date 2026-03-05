import { Link } from 'react-router-dom'

export default function Footer() {
    const currentYear = new Date().getFullYear()

    return (
        <footer className="bg-gray-900 text-white">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
                    {/* Brand Section */}
                    <div className="col-span-2 md:col-span-3 lg:col-span-2 mb-8 lg:mb-0">
                        <div className="flex items-center mb-4">
                            <Link to="/">
                                <img
                                    alt="ContinuousCare"
                                    width="100"
                                    height="20"
                                    className="h-auto"
                                    src="/cc-logo.svg"
                                />
                            </Link>
                        </div>
                        <p className="text-sm text-gray-300 mb-6 max-w-md">
                            Digital Health platform for clinics and healthcare services
                        </p>
                        <p className="text-sm text-gray-300 font-semibold mb-3">
                            Stay Connected With Us
                        </p>
                        <div className="flex items-center gap-5">
                            <a href="https://www.facebook.com/CCbyNeedStreet" target="_blank" rel="noopener noreferrer">
                                <span className="sr-only">Facebook</span>
                                📘
                            </a>
                            <a href="https://www.linkedin.com/company/needstreet" target="_blank" rel="noopener noreferrer">
                                <span className="sr-only">LinkedIn</span>
                                💼
                            </a>
                            <a href="https://x.com/continuouscareH" target="_blank" rel="noopener noreferrer">
                                <span className="sr-only">Twitter</span>
                                🐦
                            </a>
                        </div>
                    </div>

                    {/* Company */}
                    <div>
                        <h3 className="text-white font-semibold mb-4">Company</h3>
                        <ul className="space-y-2">
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/about">
                                    About
                                </Link>
                            </li>
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/contact-us">
                                    Contact
                                </Link>
                            </li>
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/jobs">
                                    Jobs
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Solutions */}
                    <div>
                        <h3 className="text-white font-semibold mb-4">Solutions</h3>
                        <ul className="space-y-2">
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/solutions/virtual-practice">
                                    Virtual Practice
                                </Link>
                            </li>
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/solutions/for-clinics">
                                    For Clinics
                                </Link>
                            </li>
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/solutions/for-startups">
                                    For Startups
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Resources */}
                    <div>
                        <h3 className="text-white font-semibold mb-4">Resources</h3>
                        <ul className="space-y-2">
                            <li>
                                <a href="#" className="text-gray-300 hover:text-white text-sm transition-colors">
                                    Help
                                </a>
                            </li>
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/blog">
                                    Blog
                                </Link>
                            </li>
                            <li>
                                <Link className="text-gray-300 hover:text-white text-sm transition-colors" to="/platform-security">
                                    Security
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Mobile App */}
                    <div>
                        <h3 className="text-white font-semibold mb-4">Virtual Practice Mobile App</h3>
                        <div className="flex flex-col items-start gap-3">
                            <a href="https://apps.apple.com" target="_blank" rel="noopener noreferrer">
                                <div className="bg-white text-black px-3 py-1 rounded text-xs">App Store</div>
                            </a>
                            <a href="https://play.google.com" target="_blank" rel="noopener noreferrer">
                                <div className="bg-white text-black px-3 py-1 rounded text-xs">Google Play</div>
                            </a>
                        </div>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="mt-8 pt-8 border-t border-gray-300 text-sm flex flex-col md:flex-row items-center justify-center gap-4">
                    <div className="text-gray-300">
                        © {currentYear} NeedStreet All Rights Reserved
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-3">
                            <Link className="text-gray-300 hover:text-white transition-colors" to="/terms-conditions">
                                Terms
                            </Link>
                            <div>|</div>
                            <Link className="text-gray-300 hover:text-white transition-colors" to="/privacy-policy">
                                Privacy
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    )
}
