import { Link } from 'react-router-dom'

export default function Home() {
    return (
        <div className="w-full">
            {/* Hero Section */}
            <section className="pt-32 pb-16 md:pt-36 md:pb-20 bg-white overflow-hidden">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col lg:flex-row items-center">
                        {/* Left Content */}
                        <div className="lg:w-1/2 mb-10 lg:mb-0 lg:pr-12">
                            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-8 text-slate-dark">
                                All-in-One Virtual Practice Platform for{' '}
                                <span className="text-blue-accent">Modern Clinics</span>
                            </h1>
                            <p className="text-xl md:text-2xl mb-10 text-slate-700 leading-relaxed">
                                Run and grow your clinic with telehealth, EHR, payments, and AI-powered documentation—everything in one secure, branded system.
                            </p>

                            {/* Feature List */}
                            <div className="space-y-6 mb-10">
                                <div className="flex items-center gap-3">
                                    <svg className="h-7 w-7 text-green-success flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span className="text-xl text-slate-700">Save hours with AI-generated consultation notes</span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <svg className="h-7 w-7 text-green-success flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span className="text-xl text-slate-700">End-to-end practice management in one system</span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <svg className="h-7 w-7 text-green-success flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span className="text-xl text-slate-700">White-label and startup-ready for digital health innovators</span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <svg className="h-7 w-7 text-green-success flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span className="text-xl text-slate-700">Go live in hours, not months</span>
                                </div>
                            </div>

                            {/* CTA Button */}
                            <div className="flex flex-col sm:flex-row gap-4">
                                <Link to="/register">
                                    <button className="inline-flex items-center justify-center font-medium transition-all duration-200 rounded-md px-6 py-3 text-lg bg-blue-vibrant text-white hover:bg-blue-accent shadow-lg">
                                        Start Free Trial
                                    </button>
                                </Link>
                            </div>
                        </div>

                        {/* Right Image */}
                        <div className="lg:w-1/2">
                            <div className="relative">
                                <img
                                    alt="Healthcare professionals using technology"
                                    className="rounded-lg shadow-xl w-full h-auto object-cover"
                                    src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=1000"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Why Section */}
            <section className="py-12 md:py-16" style={{ backgroundColor: '#dcf2ed' }}>
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4 text-slate-dark">
                            Why Your Clinic Needs a Virtual Practice
                        </h2>
                        <div className="w-16 h-1 bg-blue-vibrant mx-auto"></div>
                    </div>

                    <div className="max-w-5xl mx-auto">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                            {/* Feature Cards */}
                            <FeatureCard
                                icon={
                                    <svg className="w-6 h-6 text-blue-vibrant" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                    </svg>
                                }
                                title="AI Reduces Documentation Time"
                                description="Spend more time with patients and less on paperwork with AI-generated notes."
                            />
                            <FeatureCard
                                icon={
                                    <svg className="w-6 h-6 text-green-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                                    </svg>
                                }
                                title="Everything in One Platform"
                                description="Manage appointments, billing, patient records, and engagement tools from a single system."
                            />
                            <FeatureCard
                                icon={
                                    <svg className="w-6 h-6 text-purple-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                }
                                title="Affordable for Every Practice"
                                description="Built to fit the budgets of solo practices, growing clinics, and healthcare startups."
                            />
                            <FeatureCard
                                icon={
                                    <svg className="w-6 h-6 text-teal-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                    </svg>
                                }
                                title="Secure & Compliant"
                                description="HIPAA secure and GDPR compliant, so you can go live in hours with full peace of mind."
                            />
                        </div>
                    </div>
                </div>
            </section>

            {/* Multi-modal Section */}
            <section className="py-16 md:py-24 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col lg:flex-row items-center gap-12">
                        <div className="lg:w-1/2">
                            <div className="relative rounded-xl overflow-hidden shadow-2xl">
                                <img
                                    src="https://images.unsplash.com/photo-1576091160550-2187580016f3?q=80&w=800"
                                    alt="Video consultation"
                                    className="w-full h-auto"
                                />
                                <div className="absolute bottom-4 left-4 right-4 bg-white/95 backdrop-blur-sm p-4 rounded-lg shadow-lg">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                                            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                                        </div>
                                        <div>
                                            <p className="font-semibold text-slate-800">Video Consultations</p>
                                            <p className="text-xs text-slate-500">HD Secure Video</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="lg:w-1/2">
                            <h2 className="text-3xl md:text-4xl font-bold mb-6 text-slate-dark">
                                Multi-modal Healthcare Delivery
                            </h2>
                            <p className="text-lg text-slate-700 mb-8 leading-relaxed">
                                Meet your patients where they are. ContinuousCare enables you to provide care through video, audio, text, and in-clinic visits—all from a single unified timeline.
                            </p>
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                <div className="flex items-start gap-3">
                                    <div className="mt-1 text-blue-vibrant">
                                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-slate-dark">Video Visits</h3>
                                        <p className="text-sm text-slate-600">Built-in secure telehealth</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="mt-1 text-blue-vibrant">
                                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-slate-dark">Secure Messaging</h3>
                                        <p className="text-sm text-slate-600">Asynchronous care text</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="mt-1 text-blue-vibrant">
                                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-slate-dark">Remote Monitoring</h3>
                                        <p className="text-sm text-slate-600">Device data integration</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <div className="mt-1 text-blue-vibrant">
                                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-slate-dark">In-Clinic</h3>
                                        <p className="text-sm text-slate-600">Traditional appointments</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* AI Documentation & EHR Section */}
            <section className="py-16 md:py-24 bg-slate-50">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col lg:flex-row-reverse items-center gap-12">
                        <div className="lg:w-1/2">
                            <div className="bg-white rounded-xl shadow-xl border border-gray-100 p-8">
                                <div className="flex items-center gap-4 mb-6 border-b border-gray-100 pb-4">
                                    <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-600">
                                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-slate-800">AI Medical Scribe</h3>
                                        <p className="text-xs text-slate-500">Generating SOAP note...</p>
                                    </div>
                                </div>
                                <div className="space-y-4">
                                    <div className="h-4 bg-gray-100 rounded w-3/4 animate-pulse"></div>
                                    <div className="h-4 bg-gray-100 rounded w-full animate-pulse"></div>
                                    <div className="h-4 bg-gray-100 rounded w-5/6 animate-pulse"></div>
                                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-100">
                                        <p className="text-sm text-slate-700 font-medium">Assessment:</p>
                                        <p className="text-sm text-slate-600 mt-1">Patient presents with acute bronchitis. Symptoms include...</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="lg:w-1/2">
                            <div className="inline-block px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold mb-4">
                                AI-Powered
                            </div>
                            <h2 className="text-3xl md:text-4xl font-bold mb-6 text-slate-dark">
                                Documentation that writes itself
                            </h2>
                            <p className="text-lg text-slate-700 mb-6 leading-relaxed">
                                Stop typing and start listening. Our AI Scribe listens to your consultation and automatically generates accurate SOAP notes, coding, and summaries in seconds.
                            </p>
                            <ul className="space-y-3 mb-8">
                                <li className="flex items-center gap-3">
                                    <svg className="w-5 h-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                                    <span className="text-slate-700">Ambient listening technology</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <svg className="w-5 h-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                                    <span className="text-slate-700">Integrated directly into the EHR</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <svg className="w-5 h-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                                    <span className="text-slate-700">Works for all medical specialties</span>
                                </li>
                            </ul>
                            <Link to="/register">
                                <button className="text-purple-600 font-semibold flex items-center gap-2 hover:gap-3 transition-all">
                                    Learn about AI Scribe <span className="text-xl">→</span>
                                </button>
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Patient Engagement Section */}
            <section className="py-16 md:py-24 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl md:text-4xl font-bold mb-6 text-slate-dark">
                        Digital Front Door & Patient Engagement
                    </h2>
                    <p className="text-lg text-slate-700 mb-12 max-w-3xl mx-auto">
                        Delight your patients with a modern digital experience. From online booking to branded patient portals, give them the convenience they expect.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="p-6 rounded-xl border border-gray-100 hover:border-blue-200 hover:shadow-lg transition-all">
                            <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4 text-blue-600">
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                            </div>
                            <h3 className="font-bold text-lg mb-2 text-slate-dark">Online Scheduling</h3>
                            <p className="text-slate-600 text-sm">Real-time booking widget for your website</p>
                        </div>
                        <div className="p-6 rounded-xl border border-gray-100 hover:border-blue-200 hover:shadow-lg transition-all">
                            <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4 text-blue-600">
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                            </div>
                            <h3 className="font-bold text-lg mb-2 text-slate-dark">Patient App</h3>
                            <p className="text-slate-600 text-sm">White-labeled mobile app for iOS and Android</p>
                        </div>
                        <div className="p-6 rounded-xl border border-gray-100 hover:border-blue-200 hover:shadow-lg transition-all">
                            <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4 text-blue-600">
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
                            </div>
                            <h3 className="font-bold text-lg mb-2 text-slate-dark">Payments</h3>
                            <p className="text-slate-600 text-sm">Integrated billing and automated collections</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="py-16 md:py-24 bg-blue-900 text-white bg-opacity-95">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl md:text-4xl font-bold mb-12 text-center">
                        Trusted by Healthcare Leaders
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <div className="bg-blue-800 bg-opacity-50 p-8 rounded-xl backdrop-blur-sm">
                            <div className="flex gap-1 text-yellow-400 mb-4">
                                {[1, 2, 3, 4, 5].map(i => <span key={i}>★</span>)}
                            </div>
                            <p className="text-lg mb-6 leading-relaxed italic">"ContinuousCare helped us launch our virtual clinic in less than a week. The AI features alone save me 2 hours a day."</p>
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-full bg-blue-200"></div>
                                <div>
                                    <p className="font-bold">Dr. Sarah Chen</p>
                                    <p className="text-sm text-blue-200">Medical Director, TeleHealth Now</p>
                                </div>
                            </div>
                        </div>
                        <div className="bg-blue-800 bg-opacity-50 p-8 rounded-xl backdrop-blur-sm">
                            <div className="flex gap-1 text-yellow-400 mb-4">
                                {[1, 2, 3, 4, 5].map(i => <span key={i}>★</span>)}
                            </div>
                            <p className="text-lg mb-6 leading-relaxed italic">"The patient portal is beautiful and easy to use. My patients love booking appointments online."</p>
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-full bg-blue-200"></div>
                                <div>
                                    <p className="font-bold">Dr. Michael Ross</p>
                                    <p className="text-sm text-blue-200">Founder, Ross Family Practice</p>
                                </div>
                            </div>
                        </div>
                        <div className="bg-blue-800 bg-opacity-50 p-8 rounded-xl backdrop-blur-sm">
                            <div className="flex gap-1 text-yellow-400 mb-4">
                                {[1, 2, 3, 4, 5].map(i => <span key={i}>★</span>)}
                            </div>
                            <p className="text-lg mb-6 leading-relaxed italic">"Integrated billing sent our revenue up by 20% in the first month. Best practice management software we've used."</p>
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-full bg-blue-200"></div>
                                <div>
                                    <p className="font-bold">Jennifer Wu</p>
                                    <p className="text-sm text-blue-200">Clinic Manager, City Health</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Built For Section */}
            <section className="py-16 md:py-24 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-0 overflow-hidden rounded-2xl shadow-xl">
                        <div className="bg-slate-50 p-12 lg:p-16 flex flex-col justify-center">
                            <h3 className="text-2xl md:text-3xl font-bold mb-4 text-slate-dark">Built for Practices</h3>
                            <p className="text-slate-600 mb-8 text-lg">
                                Streamline your operations, reduce burnout, and grow your patient base with tools designed for modern care delivery.
                            </p>
                            <ul className="space-y-3 mb-8">
                                <li className="flex items-center gap-2 text-slate-700">✓ Automated workflows</li>
                                <li className="flex items-center gap-2 text-slate-700">✓ Revenue cycle management</li>
                                <li className="flex items-center gap-2 text-slate-700">✓ Patient retention tools</li>
                            </ul>
                            <Link to="/register" className="text-blue-vibrant font-semibold hover:text-blue-700">
                                See solutions for practices →
                            </Link>
                        </div>
                        <div className="bg-slate-900 p-12 lg:p-16 flex flex-col justify-center text-white">
                            <h3 className="text-2xl md:text-3xl font-bold mb-4">Perfect for Startups</h3>
                            <p className="text-gray-300 mb-8 text-lg">
                                Launch your digital health product faster with our white-label platform and robust API infrastructure.
                            </p>
                            <ul className="space-y-3 mb-8">
                                <li className="flex items-center gap-2 text-gray-300">✓ White-label everything</li>
                                <li className="flex items-center gap-2 text-gray-300">✓ Developer-friendly API</li>
                                <li className="flex items-center gap-2 text-gray-300">✓ HIPAA compliant infrastructure</li>
                            </ul>
                            <Link to="/register" className="text-blue-400 font-semibold hover:text-blue-300">
                                See solutions for startups →
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-blue-vibrant text-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-4xl md:text-5xl font-bold mb-6">
                        Ready to Transform Your Healthcare Delivery?
                    </h2>
                    <p className="text-xl mb-8 max-w-3xl mx-auto">
                        Start your 14-day free trial of the Virtual Practice and see how it works for your clinic.
                    </p>
                    <div className="mb-8">
                        <Link to="/register">
                            <button className="inline-flex items-center justify-center font-medium transition-all duration-200 rounded-md px-6 py-3 text-lg bg-white text-blue-vibrant hover:bg-gray-100 shadow-lg">
                                Start Free 14-Day Trial
                            </button>
                        </Link>
                    </div>
                    <div className="flex flex-wrap justify-center gap-x-8 gap-y-4">
                        <div className="flex items-center gap-2">
                            <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>No credit card required</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>Full access to the Virtual Practice</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>Cancel anytime</span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}

// Feature Card Component
function FeatureCard({ icon, title, description }) {
    return (
        <div className="bg-white rounded-xl shadow-md p-6 text-center hover:shadow-lg transition-shadow duration-300">
            <div className="w-12 h-12 mx-auto mb-4 rounded-full bg-blue-50 flex items-center justify-center">
                {icon}
            </div>
            <h3 className="text-lg font-bold text-slate-dark mb-3">{title}</h3>
            <p className="text-slate-600 text-sm leading-relaxed">{description}</p>
        </div>
    )
}
