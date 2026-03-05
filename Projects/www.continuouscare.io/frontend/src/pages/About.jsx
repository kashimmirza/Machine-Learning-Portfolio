import { Link } from 'react-router-dom'

export default function About() {
    return (
        <div className="w-full">
            {/* Hero Section */}
            <section className="pt-32 pb-16 md:pt-36 md:pb-20 bg-gradient-to-b from-blue-50 to-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-slate-dark">
                        Transforming Healthcare Delivery
                    </h1>
                    <p className="text-xl md:text-2xl text-slate-700 mb-10 max-w-3xl mx-auto">
                        We're on a mission to make digital health accessible, affordable, and easy to use for healthcare providers everywhere.
                    </p>
                </div>
            </section>

            {/* Mission Section */}
            <section className="py-16 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="max-w-4xl mx-auto">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-16">
                            <div>
                                <h2 className="text-3xl md:text-4xl font-bold mb-6 text-slate-dark">Our Mission</h2>
                                <p className="text-lg text-slate-700 leading-relaxed mb-4">
                                    At ContinuousCare, we believe that every healthcare provider deserves access to world-class technology—regardless of their size or budget.
                                </p>
                                <p className="text-lg text-slate-700 leading-relaxed">
                                    We're building a platform that combines telehealth, EHR, practice management, and AI-powered documentation into one seamless experience that saves time, reduces costs, and improves patient outcomes.
                                </p>
                            </div>
                            <div>
                                <img
                                    src="https://images.unsplash.com/photo-1559757175-5700dde675bc?q=80&w=800"
                                    alt="Healthcare team"
                                    className="rounded-lg shadow-xl w-full"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Values Section */}
            <section className="py-16 bg-gray-50">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-slate-dark">
                        Our Values
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                        <ValueCard
                            icon={
                                <svg className="w-8 h-8 text-blue-vibrant" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                                </svg>
                            }
                            title="Patient-First"
                            description="Everything we build is designed to improve patient care and outcomes."
                        />
                        <ValueCard
                            icon={
                                <svg className="w-8 h-8 text-green-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            }
                            title="Innovation"
                            description="We leverage cutting-edge AI and technology to solve healthcare's toughest challenges."
                        />
                        <ValueCard
                            icon={
                                <svg className="w-8 h-8 text-purple-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                </svg>
                            }
                            title="Trust & Security"
                            description="We're committed to the highest standards of data security and privacy."
                        />
                    </div>
                </div>
            </section>

            {/* Story Section */}
            <section className="py-16 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="max-w-3xl mx-auto">
                        <h2 className="text-3xl md:text-4xl font-bold mb-8 text-slate-dark text-center">Our Story</h2>
                        <div className="space-y-6 text-lg text-slate-700 leading-relaxed">
                            <p>
                                ContinuousCare was founded by a team of healthcare professionals and technologists who experienced firsthand the challenges of managing a modern healthcare practice.
                            </p>
                            <p>
                                After spending countless hours on paperwork, dealing with disconnected systems, and struggling with expensive software, we knew there had to be a better way.
                            </p>
                            <p>
                                We built ContinuousCare to be the platform we wished we had—one that's intuitive, affordable, and powerful enough to handle everything from telehealth appointments to billing and compliance.
                            </p>
                            <p>
                                Today, thousands of healthcare providers trust ContinuousCare to help them deliver better care while spending less time on administrative tasks.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="py-16 bg-blue-vibrant text-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
                        <StatCard number="10,000+" label="Healthcare Providers" />
                        <StatCard number="1M+" label="Patients Served" />
                        <StatCard number="50M+" label="Appointments Booked" />
                        <StatCard number="99.9%" label="Uptime SLA" />
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-4xl md:text-5xl font-bold mb-6 text-slate-dark">
                        Join Us in Transforming Healthcare
                    </h2>
                    <p className="text-xl text-slate-700 mb-8 max-w-2xl mx-auto">
                        Whether you're a solo practitioner or running a multi-location practice, we're here to help you succeed.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link to="/register">
                            <button className="bg-blue-vibrant text-white px-8 py-4 rounded-md text-lg font-semibold hover:bg-blue-accent transition-colors shadow-lg">
                                Start Free Trial
                            </button>
                        </Link>
                        <Link to="/contact-us">
                            <button className="bg-white text-blue-vibrant border-2 border-blue-vibrant px-8 py-4 rounded-md text-lg font-semibold hover:bg-blue-50 transition-colors">
                                Contact Us
                            </button>
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    )
}

// Value Card Component
function ValueCard({ icon, title, description }) {
    return (
        <div className="bg-white rounded-xl shadow-md p-8 text-center hover:shadow-lg transition-shadow">
            <div className="flex justify-center mb-4">
                {icon}
            </div>
            <h3 className="text-xl font-bold mb-3 text-slate-dark">{title}</h3>
            <p className="text-slate-600 leading-relaxed">{description}</p>
        </div>
    )
}

// Stat Card Component
function StatCard({ number, label }) {
    return (
        <div>
            <div className="text-4xl md:text-5xl font-bold mb-2">{number}</div>
            <div className="text-lg text-blue-100">{label}</div>
        </div>
    )
}
