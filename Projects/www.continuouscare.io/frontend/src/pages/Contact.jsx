import { useState } from 'react'

export default function Contact() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        company: '',
        helpWith: '',
        message: ''
    })

    const handleSubmit = async (e) => {
        e.preventDefault()
        // API call will be added
        console.log('Form submitted:', formData)
        alert('Thank you for contacting us! We\'ll get back to you soon.')
    }

    return (
        <div className="w-full">
            {/* Hero Section */}
            <section className="pt-32 pb-16 md:pt-36 md:pb-20 bg-gradient-to-b from-blue-50 to-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-slate-dark">
                        Get in Touch
                    </h1>
                    <p className="text-xl md:text-2xl text-slate-700 mb-10 max-w-3xl mx-auto">
                        Have questions? We're here to help. Reach out to our team and we'll respond as soon as possible.
                    </p>
                </div>
            </section>

            {/* Contact Form Section */}
            <section className="py-16 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="max-w-3xl mx-auto">
                        <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                            <form onSubmit={handleSubmit} className="space-y-6">
                                {/* Name */}
                                <div>
                                    <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-2">
                                        Name *
                                    </label>
                                    <input
                                        type="text"
                                        id="name"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-vibrant focus:border-blue-vibrant transition-colors"
                                        required
                                    />
                                </div>

                                {/* Email */}
                                <div>
                                    <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">
                                        Email *
                                    </label>
                                    <input
                                        type="email"
                                        id="email"
                                        value={formData.email}
                                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-vibrant focus:border-blue-vibrant transition-colors"
                                        required
                                    />
                                </div>

                                {/* Phone */}
                                <div>
                                    <label htmlFor="phone" className="block text-sm font-medium text-slate-700 mb-2">
                                        Phone
                                    </label>
                                    <input
                                        type="tel"
                                        id="phone"
                                        value={formData.phone}
                                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-vibrant focus:border-blue-vibrant transition-colors"
                                    />
                                </div>

                                {/* Company */}
                                <div>
                                    <label htmlFor="company" className="block text-sm font-medium text-slate-700 mb-2">
                                        Company / Practice Name
                                    </label>
                                    <input
                                        type="text"
                                        id="company"
                                        value={formData.company}
                                        onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-vibrant focus:border-blue-vibrant transition-colors"
                                    />
                                </div>

                                {/* How can we help? */}
                                <div>
                                    <label htmlFor="helpWith" className="block text-sm font-medium text-slate-700 mb-2">
                                        How can we help? *
                                    </label>
                                    <select
                                        id="helpWith"
                                        value={formData.helpWith}
                                        onChange={(e) => setFormData({ ...formData, helpWith: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-vibrant focus:border-blue-vibrant transition-colors"
                                        required
                                    >
                                        <option value="">Select an option</option>
                                        <option value="demo">Request a demo</option>
                                        <option value="pricing">Pricing inquiry</option>
                                        <option value="technical">Technical support</option>
                                        <option value="partnership">Partnership opportunity</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>

                                {/* Message */}
                                <div>
                                    <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-2">
                                        Message *
                                    </label>
                                    <textarea
                                        id="message"
                                        rows="6"
                                        value={formData.message}
                                        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                                        className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-vibrant focus:border-blue-vibrant transition-colors"
                                        required
                                    ></textarea>
                                </div>

                                {/* Consent Checkbox */}
                                <div className="flex items-start gap-2">
                                    <input
                                        type="checkbox"
                                        id="consent"
                                        className="mt-1 w-4 h-4 text-blue-vibrant focus:ring-blue-vibrant border-gray-300 rounded"
                                        required
                                    />
                                    <label htmlFor="consent" className="text-sm text-slate-600">
                                        I agree to receive communications from ContinuousCare about products and services.
                                    </label>
                                </div>

                                {/* Submit Button */}
                                <button
                                    type="submit"
                                    className="w-full bg-blue-vibrant text-white py-4 px-6 rounded-md hover:bg-blue-accent transition-colors font-semibold text-lg shadow-lg"
                                >
                                    Send Message
                                </button>
                            </form>
                        </div>

                        {/* Contact Info */}
                        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
                            <div>
                                <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <svg className="w-6 h-6 text-blue-vibrant" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <h3 className="font-semibold text-slate-dark mb-2">Email</h3>
                                <p className="text-slate-600">support@continuouscare.io</p>
                            </div>
                            <div>
                                <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <svg className="w-6 h-6 text-blue-vibrant" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                    </svg>
                                </div>
                                <h3 className="font-semibold text-slate-dark mb-2">Phone</h3>
                                <p className="text-slate-600">1-800-CARE-NOW</p>
                            </div>
                            <div>
                                <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <svg className="w-6 h-6 text-blue-vibrant" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                                    </svg>
                                </div>
                                <h3 className="font-semibold text-slate-dark mb-2">Live Chat</h3>
                                <p className="text-slate-600">Available 24/7</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}
