import { Link } from 'react-router-dom'
import { useState } from 'react'

export default function Pricing() {
    const [billingCycle, setBillingCycle] = useState('monthly')

    return (
        <div className="w-full">
            {/* Hero Section */}
            <section className="pt-32 pb-16 md:pt-36 md:pb-20 bg-gradient-to-b from-blue-50 to-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-slate-dark">
                        Simple, Transparent Pricing
                    </h1>
                    <p className="text-xl md:text-2xl text-slate-700 mb-10 max-w-3xl mx-auto">
                        Choose the plan that fits your practice. All plans include access to our complete platform.
                    </p>

                    {/* Billing Toggle */}
                    <div className="flex items-center justify-center gap-4 mb-12">
                        <span className={`text-lg ${billingCycle === 'monthly' ? 'text-blue-vibrant font-semibold' : 'text-slate-600'}`}>
                            Monthly
                        </span>
                        <button
                            onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')}
                            className="relative w-16 h-8 bg-blue-vibrant rounded-full transition-colors"
                        >
                            <div className={`absolute top-1 w-6 h-6 bg-white rounded-full transition-transform ${billingCycle === 'annual' ? 'translate-x-9' : 'translate-x-1'}`}></div>
                        </button>
                        <span className={`text-lg ${billingCycle === 'annual' ? 'text-blue-vibrant font-semibold' : 'text-slate-600'}`}>
                            Annual <span className="text-green-success text-sm">(Save 20%)</span>
                        </span>
                    </div>
                </div>
            </section>

            {/* Pricing Cards */}
            <section className="py-16 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">

                        {/* Starter Plan */}
                        <PricingCard
                            name="Starter"
                            price={billingCycle === 'monthly' ? '99' : '79'}
                            period={billingCycle === 'monthly' ? '/month' : '/month (billed annually)'}
                            description="Perfect for solo practitioners"
                            features={[
                                'Up to 50 patients',
                                'AI-powered documentation',
                                'Basic EHR',
                                'Telehealth visits',
                                'Patient portal',
                                'Email support'
                            ]}
                            cta="Start Free Trial"
                            highlighted={false}
                        />

                        {/* Professional Plan */}
                        <PricingCard
                            name="Professional"
                            price={billingCycle === 'monthly' ? '299' : '239'}
                            period={billingCycle === 'monthly' ? '/month' : '/month (billed annually)'}
                            description="For growing practices"
                            features={[
                                'Up to 500 patients',
                                'Everything in Starter, plus:',
                                'Advanced EHR features',
                                'Practice management',
                                'Billing & payments',
                                'Priority support',
                                'Custom branding'
                            ]}
                            cta="Start Free Trial"
                            highlighted={true}
                        />

                        {/* Enterprise Plan */}
                        <PricingCard
                            name="Enterprise"
                            price="Custom"
                            period=""
                            description="For hospitals and large practices"
                            features={[
                                'Unlimited patients',
                                'Everything in Professional, plus:',
                                'Multi-location support',
                                'Advanced analytics',
                                'API access',
                                'Dedicated account manager',
                                'Custom integrations',
                                'SLA guarantee'
                            ]}
                            cta="Contact Sales"
                            highlighted={false}
                        />
                    </div>
                </div>
            </section>

            {/* Features Comparison */}
            <section className="py-16 bg-gray-50">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-slate-dark">
                        Compare Features
                    </h2>
                    <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
                        <table className="w-full">
                            <thead className="bg-gray-100">
                                <tr>
                                    <th className="text-left p-4 text-slate-dark font-semibold">Feature</th>
                                    <th className="text-center p-4 text-slate-dark font-semibold">Starter</th>
                                    <th className="text-center p-4 text-slate-dark font-semibold">Professional</th>
                                    <th className="text-center p-4 text-slate-dark font-semibold">Enterprise</th>
                                </tr>
                            </thead>
                            <tbody>
                                <FeatureRow feature="AI Documentation" starter={true} professional={true} enterprise={true} />
                                <FeatureRow feature="Telehealth" starter={true} professional={true} enterprise={true} />
                                <FeatureRow feature="Patient Portal" starter={true} professional={true} enterprise={true} />
                                <FeatureRow feature="Billing & Payments" starter={false} professional={true} enterprise={true} />
                                <FeatureRow feature="Custom Branding" starter={false} professional={true} enterprise={true} />
                                <FeatureRow feature="Multi-location" starter={false} professional={false} enterprise={true} />
                                <FeatureRow feature="API Access" starter={false} professional={false} enterprise={true} />
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            {/* FAQ Section */}
            <section className="py-16 bg-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-slate-dark">
                        Frequently Asked Questions
                    </h2>
                    <div className="max-w-3xl mx-auto space-y-6">
                        <FAQItem
                            question="Can I try before I buy?"
                            answer="Yes! All plans come with a 14-day free trial. No credit card required."
                        />
                        <FAQItem
                            question="Can I change plans later?"
                            answer="Absolutely. You can upgrade or downgrade your plan at any time."
                        />
                        <FAQItem
                            question="What payment methods do you accept?"
                            answer="We accept all major credit cards, ACH transfers, and wire transfers for enterprise plans."
                        />
                        <FAQItem
                            question="Is my data secure?"
                            answer="Yes. We're HIPAA compliant and use bank-level encryption to protect your data."
                        />
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-blue-vibrant text-white">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-4xl md:text-5xl font-bold mb-6">
                        Ready to Get Started?
                    </h2>
                    <p className="text-xl mb-8 max-w-2xl mx-auto">
                        Join thousands of healthcare providers using ContinuousCare
                    </p>
                    <Link to="/register">
                        <button className="bg-white text-blue-vibrant px-8 py-4 rounded-md text-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg">
                            Start Your Free Trial
                        </button>
                    </Link>
                </div>
            </section>
        </div>
    )
}

// Pricing Card Component
function PricingCard({ name, price, period, description, features, cta, highlighted }) {
    return (
        <div className={`rounded-xl p-8 ${highlighted ? 'bg-blue-vibrant text-white shadow-2xl transform scale-105' : 'bg-white border-2 border-gray-200'}`}>
            <h3 className={`text-2xl font-bold mb-2 ${highlighted ? 'text-white' : 'text-slate-dark'}`}>
                {name}
            </h3>
            <p className={`text-sm mb-6 ${highlighted ? 'text-blue-100' : 'text-slate-600'}`}>
                {description}
            </p>
            <div className="mb-6">
                <span className="text-4xl font-bold">${price}</span>
                <span className={`text-sm ${highlighted ? 'text-blue-100' : 'text-slate-600'}`}>{period}</span>
            </div>
            <Link to="/register">
                <button className={`w-full py-3 rounded-md font-semibold transition-colors mb-8 ${highlighted
                        ? 'bg-white text-blue-vibrant hover:bg-gray-100'
                        : 'bg-blue-vibrant text-white hover:bg-blue-accent'
                    }`}>
                    {cta}
                </button>
            </Link>
            <ul className="space-y-3">
                {features.map((feature, index) => (
                    <li key={index} className="flex items-start gap-2">
                        <svg className={`w-5 h-5 flex-shrink-0 mt-0.5 ${highlighted ? 'text-white' : 'text-green-success'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span className="text-sm">{feature}</span>
                    </li>
                ))}
            </ul>
        </div>
    )
}

// Feature Row Component
function FeatureRow({ feature, starter, professional, enterprise }) {
    const CheckIcon = () => (
        <svg className="w-6 h-6 text-green-success mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
    )
    const XIcon = () => (
        <svg className="w-6 h-6 text-gray-300 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
    )

    return (
        <tr className="border-t border-gray-200">
            <td className="p-4 text-slate-700">{feature}</td>
            <td className="p-4 text-center">{starter ? <CheckIcon /> : <XIcon />}</td>
            <td className="p-4 text-center">{professional ? <CheckIcon /> : <XIcon />}</td>
            <td className="p-4 text-center">{enterprise ? <CheckIcon /> : <XIcon />}</td>
        </tr>
    )
}

// FAQ Item Component
function FAQItem({ question, answer }) {
    const [isOpen, setIsOpen] = useState(false)

    return (
        <div className="border-b border-gray-200 pb-6">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full text-left flex justify-between items-center"
            >
                <h3 className="text-lg font-semibold text-slate-dark">{question}</h3>
                <svg className={`w-6 h-6 text-slate-600 transition-transform ${isOpen ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
            </button>
            {isOpen && (
                <p className="mt-3 text-slate-600 leading-relaxed">{answer}</p>
            )}
        </div>
    )
}
