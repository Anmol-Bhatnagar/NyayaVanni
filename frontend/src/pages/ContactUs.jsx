import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, Mail, Phone, Clock, Send, CheckCircle, AlertCircle, MapPin } from "lucide-react";
import { useLanguage } from "../contexts/LanguageContext";
import ThemeToggle from "../components/ThemeToggle";
import Footer from "../components/Footer";

export default function ContactUs() {
  const navigate = useNavigate();
  const { language, t } = useLanguage();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: ""
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null); // 'success' | 'error' | null

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim())  newErrors.name = language === 'en' ? "Full Name is required" : "à¤ªà¥‚à¤°à¤¾ à¤¨à¤¾à¤® à¤†à¤µà¤¶à¥à¤¯à¤• à¤¹à¥ˆ";
    
    if (!formData.email.trim())  {
      newErrors.email = language === 'en' ? "Email is required" : "à¤ˆà¤®à¥‡à¤² à¤†à¤µà¤¶à¥à¤¯à¤• à¤¹à¥ˆ";
    }  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email.trim()))  {
      newErrors.email = language === 'en' ? "Invalid email format" : "à¤…à¤®à¤¾à¤¨à¥à¤¯ à¤ˆà¤®à¥‡à¤² à¤ªà¥à¤°à¤¾à¤°à¥‚à¤ª";
    }

    if (!formData.subject.trim())  newErrors.subject = language === 'en' ? "Subject is required" : "à¤µà¤¿à¤·à¤¯ à¤†à¤µà¤¶à¥à¤¯à¤• à¤¹à¥ˆ";
    if (!formData.message.trim())  {
      newErrors.message = language === 'en' ? "Message is required" : "à¤¸à¤‚à¤¦à¥‡à¤¶ à¤†à¤µà¤¶à¥à¤¯à¤• à¤¹à¥ˆ";
    } else if (formData.message.trim().length < 10)  {
      newErrors.message = language === 'en' ? "Message must be at least 10 characters" : "à¤¸à¤‚à¤¦à¥‡à¤¶ à¤•à¤® à¤¸à¥‡ à¤•à¤® 10 à¤µà¤°à¥à¤£à¥‹à¤‚ à¤•à¤¾ à¤¹à¥‹à¤¨à¤¾ à¤šà¤¾à¤¹à¤¿à¤";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error for field on type
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: "" }));
    }
    setSubmitStatus(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to send message");
      }

      setSubmitStatus("success");
      setFormData({ name: "", email: "", subject: "", message: "" });
    } catch (error) {
      setSubmitStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100 flex flex-col transition-colors duration-300">
      <div className="max-w-6xl mx-auto flex flex-col flex-1 w-full px-6 py-6">
        
        {/* Navigation / Header */}
        <header className="flex items-center justify-between py-4 mb-8 border-b border-slate-200 dark:border-slate-800">
          <button 
            onClick={() => navigate(-1)} 
            className="flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-xl border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-900 transition text-slate-700 dark:text-slate-200 cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" /> {language === 'en' ? 'Back' : 'à¤µà¤¾à¤ªà¤¸'}
          </button>
          <ThemeToggle />
        </header>

        {/* Content */}
        <main className="flex-1 w-full flex flex-col md:flex-row gap-12">
          {/* Left Column: Form */}
          <div className="flex-1 flex flex-col">
            <h1 className="text-4xl md:text-5xl font-extrabold text-slate-850 dark:text-white mb-4">
              {language === 'en' ? 'Contact Us' : 'à¤¸à¤‚à¤ªà¤°à¥à¤• à¤•à¤°à¥‡à¤‚'}
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mb-8 text-lg">
              {language === 'en' 
                ? 'Have questions about NyayaVanni? We are here to help. Send us a message and our team will get back to you.'
                : 'à¤¨à¥à¤¯à¤¾à¤¯à¤µà¤¾à¤£à¥€ à¤•à¥‡ à¤¬à¤¾à¤°à¥‡ à¤®à¥‡à¤‚ à¤ªà¥à¤°à¤¶à¥à¤¨ à¤¹à¥ˆà¤‚? à¤¹à¤® à¤¯à¤¹à¤¾à¤ à¤®à¤¦à¤¦ à¤•à¥‡ à¤²à¤¿à¤ à¤¹à¥ˆà¤‚à¥¤ à¤¹à¤®à¥‡à¤‚ à¤à¤• à¤¸à¤‚à¤¦à¥‡à¤¶ à¤­à¥‡à¤œà¥‡à¤‚ à¤”à¤° à¤¹à¤®à¤¾à¤°à¥€ à¤Ÿà¥€à¤® à¤†à¤ªà¤¸à¥‡ à¤¸à¤‚à¤ªà¤°à¥à¤• à¤•à¤°à¥‡à¤—à¥€à¥¤'}
            </p>

            <form onSubmit={handleSubmit} className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col gap-6">
              
              {submitStatus === 'success' && (
                <div className="bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-emerald-700 dark:text-emerald-400 p-4 rounded-xl flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 mt-0.5 shrink-0" />
                  <div>
                    <p className="font-semibold">{language === 'en' ? 'Message Sent!' : 'à¤¸à¤‚à¤¦à¥‡à¤¶ à¤­à¥‡à¤œà¤¾ à¤—à¤¯à¤¾!'}</p>
                    <p className="text-sm mt-1">{language === 'en' ? 'Thank you for reaching out. We will get back to you shortly.' : 'à¤¸à¤‚à¤ªà¤°à¥à¤• à¤•à¤°à¤¨à¥‡ à¤•à¥‡ à¤²à¤¿à¤ à¤§à¤¨à¥à¤¯à¤µà¤¾à¤¦à¥¤ à¤¹à¤® à¤¶à¥€à¤˜à¥à¤° à¤¹à¥€ à¤†à¤ªà¤¸à¥‡ à¤¸à¤‚à¤ªà¤°à¥à¤• à¤•à¤°à¥‡à¤‚à¤—à¥‡à¥¤'}</p>
                  </div>
                </div>
              )}

              {submitStatus === 'error' && (
                <div className="bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-700 dark:text-red-400 p-4 rounded-xl flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
                  <div>
                    <p className="font-semibold">{language === 'en' ? 'Failed to send message.' : 'à¤¸à¤‚à¤¦à¥‡à¤¶ à¤­à¥‡à¤œà¤¨à¥‡ à¤®à¥‡à¤‚ à¤µà¤¿à¤«à¤²à¥¤'}</p>
                    <p className="text-sm mt-1">{language === 'en' ? 'Please try again later.' : 'à¤•à¥ƒà¤ªà¤¯à¤¾ à¤¬à¤¾à¤¦ à¤®à¥‡à¤‚ à¤ªà¥à¤¨à¤ƒ à¤ªà¥à¤°à¤¯à¤¾à¤¸ à¤•à¤°à¥‡à¤‚à¥¤'}</p>
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex flex-col gap-2">
                  <label htmlFor="name" className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {language === 'en' ? 'Full Name' : 'à¤ªà¥‚à¤°à¤¾ à¤¨à¤¾à¤®'}
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className={`px-4 py-3 rounded-xl border ${errors.name ? 'border-red-500 focus:ring-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-nyaya-500 dark:focus:border-nyaya-500'} bg-slate-50 dark:bg-slate-950 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:ring-2 focus:ring-nyaya-500/20 outline-none transition-all`}
                    placeholder={language === 'en' ? "John Doe" : "जॉन डो"}
                    className={`px-4 py-3 rounded-xl border ${errors.name ? 'border-red-500 focus:ring-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-nyaya-500 dark:focus:border-nyaya-500'} bg-slate-50 dark:bg-slate-950 focus:ring-2 focus:ring-nyaya-500/20 outline-none transition-all`}
                    placeholder={language === 'en' ? "John Doe" : "à¤œà¥‰à¤¨ à¤¡à¥‹"}
                  />
                  {errors.name && <span className="text-red-500 text-xs">{errors.name}</span>}
                </div>

                <div className="flex flex-col gap-2">
                  <label htmlFor="email" className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                    {language === 'en' ? 'Email Address' : 'à¤ˆà¤®à¥‡à¤² à¤ªà¤¤à¤¾'}
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`px-4 py-3 rounded-xl border ${errors.email ? 'border-red-500 focus:ring-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-nyaya-500 dark:focus:border-nyaya-500'} bg-slate-50 dark:bg-slate-950 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:ring-2 focus:ring-nyaya-500/20 outline-none transition-all`}
                    placeholder="john@example.com"
                  />
                  {errors.email && <span className="text-red-500 text-xs">{errors.email}</span>}
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label htmlFor="subject" className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  {language === 'en' ? 'Subject' : 'à¤µà¤¿à¤·à¤¯'}
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  className={`px-4 py-3 rounded-xl border ${errors.subject ? 'border-red-500 focus:ring-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-nyaya-500 dark:focus:border-nyaya-500'} bg-slate-50 dark:bg-slate-950 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:ring-2 focus:ring-nyaya-500/20 outline-none transition-all`}
                  placeholder={language === 'en' ? "How can we help?" : "हम कैसे मदद कर सकते हैं?"}
                  className={`px-4 py-3 rounded-xl border ${errors.subject ? 'border-red-500 focus:ring-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-nyaya-500 dark:focus:border-nyaya-500'} bg-slate-50 dark:bg-slate-950 focus:ring-2 focus:ring-nyaya-500/20 outline-none transition-all`}
                  placeholder={language === 'en' ? "How can we help?" : "à¤¹à¤® à¤•à¥ˆà¤¸à¥‡ à¤®à¤¦à¤¦ à¤•à¤° à¤¸à¤•à¤¤à¥‡ à¤¹à¥ˆà¤‚?"}
                />
                {errors.subject && <span className="text-red-500 text-xs">{errors.subject}</span>}
              </div>

              <div className="flex flex-col gap-2">
                <label htmlFor="message" className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  {language === 'en' ? 'Message' : 'à¤¸à¤‚à¤¦à¥‡à¤¶'}
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows="5"
                  value={formData.message}
                  onChange={handleChange}
                  className={`px-4 py-3 rounded-xl border ${errors.message ? 'border-red-500 focus:ring-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-nyaya-500 dark:focus:border-nyaya-500'} bg-slate-50 dark:bg-slate-950 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:ring-2 focus:ring-nyaya-500/20 outline-none transition-all resize-none`}
                  placeholder={language === 'en' ? "Describe your issue or feedback..." : "अपनी समस्या या प्रतिक्रिया का वर्णन करें..."}
                  className={`px-4 py-3 rounded-xl border ${errors.message ? 'border-red-500 focus:ring-red-500' : 'border-slate-200 dark:border-slate-700 focus:border-nyaya-500 dark:focus:border-nyaya-500'} bg-slate-50 dark:bg-slate-950 focus:ring-2 focus:ring-nyaya-500/20 outline-none transition-all resize-none`}
                  placeholder={language === 'en' ? "Describe your issue or feedback..." : "à¤…à¤ªà¤¨à¥€ à¤¸à¤®à¤¸à¥à¤¯à¤¾ à¤¯à¤¾ à¤ªà¥à¤°à¤¤à¤¿à¤•à¥à¤°à¤¿à¤¯à¤¾ à¤•à¤¾ à¤µà¤°à¥à¤£à¤¨ à¤•à¤°à¥‡à¤‚..."}
                ></textarea>
                {errors.message && <span className="text-red-500 text-xs">{errors.message}</span>}
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="mt-2 flex items-center justify-center gap-2 w-full md:w-auto self-start bg-linear-to-r from-nyaya-600 to-nyaya-500 hover:from-nyaya-500 hover:to-nyaya-400 text-white px-8 py-3 rounded-xl font-semibold transition-all shadow-lg shadow-nyaya-500/20 dark:shadow-nyaya-500/30 hover:scale-105 disabled:opacity-70 disabled:hover:scale-100 cursor-pointer"
              >
                {isSubmitting ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    {language === 'en' ? 'Sending...' : 'à¤­à¥‡à¤œà¤¾ à¤œà¤¾ à¤°à¤¹à¤¾ à¤¹à¥ˆ...'}
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    {language === 'en' ? 'Send Message' : 'à¤¸à¤‚à¤¦à¥‡à¤¶ à¤­à¥‡à¤œà¥‡à¤‚'}
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Right Column: Contact Info */}
          <div className="w-full md:w-80 flex flex-col gap-6 mt-8 md:mt-24">
            
            <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <h3 className="text-xl font-bold text-slate-850 dark:text-white mb-6">
                {language === 'en' ? 'Contact Information' : 'à¤¸à¤‚à¤ªà¤°à¥à¤• à¤œà¤¾à¤¨à¤•à¤¾à¤°à¥€'}
              </h3>
              
              <div className="flex flex-col gap-6">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-full bg-nyaya-500/10 flex items-center justify-center shrink-0 text-nyaya-600 dark:text-nyaya-400">
                    <Mail className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800 dark:text-white">Email</p>
                    <a href="mailto:support@nyayavanni.com" className="text-sm text-slate-600 dark:text-slate-400 hover:text-nyaya-600 dark:hover:text-nyaya-400 transition-colors">
                      support@nyayavanni.com
                    </a>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-full bg-nyaya-500/10 flex items-center justify-center shrink-0 text-nyaya-600 dark:text-nyaya-400">
                    <Clock className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800 dark:text-white">
                      {language === 'en' ? 'Business Hours' : 'à¤µà¥à¤¯à¤¾à¤ªà¤¾à¤° à¤•à¥‡ à¤˜à¤‚à¤Ÿà¥‡'}
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      {language === 'en' ? 'Monâ€“Fri, 10AMâ€“6PM (IST)' : 'à¤¸à¥‹à¤®â€“à¤¶à¥à¤•à¥à¤°, à¤¸à¥à¤¬à¤¹ 10â€“à¤¶à¤¾à¤® 6 (IST)'}
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-full bg-nyaya-500/10 flex items-center justify-center shrink-0 text-nyaya-600 dark:text-nyaya-400">
                    <MapPin className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-800 dark:text-white">
                      {language === 'en' ? 'Location' : 'à¤¸à¥à¤¥à¤¾à¤¨'}
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      {language === 'en' ? 'New Delhi, India' : 'à¤¨à¤ˆ à¤¦à¤¿à¤²à¥à¤²à¥€, à¤­à¤¾à¤°à¤¤'}
                    </p>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </main>
      </div>

      <section className="z-10 w-full">
        <Footer />
      </section>
    </div>
  );
}

