
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* 🚀 Navigation (Simple) */}
      <nav className="flex items-center justify-between px-6 py-5 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          {/* Logo Placeholder - PostHog Style Hedgehog/Icon */}
          <div className="w-8 h-8 bg-black rounded-sm flex items-center justify-center text-white font-bold text-xs">
            SAU
          </div>
          <span className="font-bold text-lg tracking-tight">Social Auto Upload</span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm font-semibold text-gray-600">
          <a href="#features" className="hover:text-black">Features</a>
          <a href="#pricing" className="hover:text-black">Pricing</a>
          <a href="https://github.com/social-auto-upload" className="hover:text-black">Docs</a>
        </div>
        <div className="flex items-center gap-4">
          <Link href="http://localhost:8501" className="text-sm font-bold hover:underline">
            Log in
          </Link>
          <Link
            href="http://localhost:8501"
            className="ph-button ph-button-primary px-4 py-2 text-xs"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* 🚀 Hero Section */}
      <section className="pt-20 pb-32 px-6 max-w-6xl mx-auto text-center">
        <div className="inline-block mb-8 px-4 py-1.5 rounded-full bg-[#E3E3E0] border border-[#d0d1c9] text-gray-700 text-sm font-semibold">
          <span className="mr-2">🎉</span> V5.0 Commercial Release
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 leading-[1.1]">
          The single platform to <br className="hidden md:block" />
          <span className="text-[#f54e00] highlight-underline">automate your social growth.</span>
        </h1>

        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-12 leading-relaxed font-medium">
          Stop uploading manually. Start scaling infinitely. <br/>
          SAU provides the "Active Nervous System" that learns from your data.
        </p>

        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
          <Link
            href="http://localhost:8501"
            target="_blank"
            className="ph-button ph-button-primary text-base px-8 py-4"
          >
            Launch Dashboard
          </Link>
          <a 
            href="#pricing" 
            className="ph-button ph-button-secondary text-base px-8 py-4"
          >
            View Pricing
          </a>
        </div>

        {/* Hero Image / ASCII Art Placeholder */}
        <div className="mt-20 border-4 border-black rounded-xl overflow-hidden shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] bg-white max-w-4xl mx-auto">
           <div className="bg-gray-100 border-b border-black p-3 flex gap-2">
             <div className="w-3 h-3 rounded-full bg-red-500 border border-black"></div>
             <div className="w-3 h-3 rounded-full bg-yellow-500 border border-black"></div>
             <div className="w-3 h-3 rounded-full bg-green-500 border border-black"></div>
           </div>
           <div className="p-8 md:p-12 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
              <div className="bg-[#eeefe9] p-4 rounded border border-gray-300">
                 <div className="font-bold mb-2">Upload Queue</div>
                 <div className="space-y-2">
                    <div className="h-2 bg-gray-300 rounded w-3/4"></div>
                    <div className="h-2 bg-gray-300 rounded w-1/2"></div>
                 </div>
              </div>
              <div className="bg-[#eeefe9] p-4 rounded border border-gray-300 md:col-span-2">
                 <div className="font-bold mb-2">Analytics Graph</div>
                 <div className="h-32 bg-orange-100 border border-orange-200 rounded flex items-end justify-between p-2 gap-1">
                    <div className="w-full bg-orange-500 h-[40%] rounded-t"></div>
                    <div className="w-full bg-orange-500 h-[60%] rounded-t"></div>
                    <div className="w-full bg-orange-500 h-[30%] rounded-t"></div>
                    <div className="w-full bg-orange-500 h-[80%] rounded-t"></div>
                    <div className="w-full bg-orange-500 h-[50%] rounded-t"></div>
                 </div>
              </div>
           </div>
        </div>
      </section>

      {/* 🔮 Features */}
      <section id="features" className="py-24 px-6 bg-white border-y border-[#dadbd2]">
        <div className="max-w-7xl mx-auto">
          <div className="mb-16 md:text-center max-w-3xl mx-auto">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">Everything you need to go viral.</h2>
            <p className="text-lg text-gray-600">Built for engineers and growth hackers who hate manual work.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { 
                tag: "01", 
                title: "Smart Brain", 
                desc: "DeepSeek-integrated title generation that writes viral hooks automatically based on platform trends.",
                icon: "🧠"
              },
              { 
                tag: "02", 
                title: "Analytics Lab", 
                desc: "Self-evolving scraper that learns which content formats perform best and iterates your strategy.",
                icon: "📊"
              },
              { 
                tag: "03", 
                title: "Anti-Fragile", 
                desc: "Resilient uploading that auto-retries on failure. Handles network jitter and platform quirks gracefully.",
                icon: "🛡️"
              }
            ].map((feature, i) => (
              <div key={i} className="ph-card group hover:-translate-y-1 hover:shadow-lg duration-300">
                <div className="flex items-center justify-between mb-4">
                   <span className="text-4xl">{feature.icon}</span>
                   <span className="font-mono text-xs font-bold bg-black text-white px-2 py-1 rounded">{feature.tag}</span>
                </div>
                <h3 className="text-xl font-bold mb-3 group-hover:text-[#f54e00] transition-colors">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 💰 Pricing */}
      <section id="pricing" className="py-24 px-6 bg-[#FDFBF6]">
        <div className="max-w-5xl mx-auto">
           <div className="bg-[#FFF9F5] border-2 border-black rounded-2xl overflow-hidden shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] md:flex">
              <div className="p-12 md:w-1/2 border-b md:border-b-0 md:border-r-2 border-black flex flex-col justify-between">
                 <div>
                    <h2 className="text-3xl font-bold mb-2">Professional Access</h2>
                    <p className="text-gray-600 mb-8">For serious creators scaling up.</p>
                    <div className="text-6xl font-extrabold text-[#f54e00] mb-2">
                      ￥199<span className="text-2xl text-black font-medium">/mo</span>
                    </div>
                    <p className="text-sm font-medium text-gray-500">Cancel anytime. ROI guaranteed.</p>
                 </div>
                 
                 <div className="mt-8">
                    <button className="w-full ph-button ph-button-primary py-4 text-lg">
                      Get Access Now
                    </button>
                    <p className="text-center text-xs text-gray-500 mt-4">Scan code -> Contact Admin -> Get Key</p>
                 </div>
              </div>

              <div className="p-12 md:w-1/2 bg-white">
                <h3 className="font-bold text-lg mb-6 uppercase tracking-wider">What's included</h3>
                <ul className="space-y-4">
                  {["Unlimited Batch Uploads", "DeepSeek Smart Titles", "Analytics Dashboard", "Priority Support", "Cookie Management", "Multi-Platform Sync"].map((item) => (
                    <li key={item} className="flex items-center gap-3">
                      <div className="w-6 h-6 rounded-full bg-[#EAF2E2] border border-[#76B041] flex items-center justify-center text-[#76B041] font-bold text-sm">✓</div>
                      <span className="font-medium text-gray-800">{item}</span>
                    </li>
                  ))}
                </ul>
                
                <div className="mt-8 pt-8 border-t border-dashed border-gray-300">
                   <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gray-100 rounded flex items-center justify-center text-2xl">💬</div>
                      <div>
                        <div className="font-bold text-sm">Need help?</div>
                        <div className="text-xs text-gray-500">Contact support for custom enterprise plans.</div>
                      </div>
                   </div>
                </div>
              </div>
           </div>
        </div>
      </section>

      {/* 🦶 Footer */}
      <footer className="py-12 px-6 border-t border-[#dadbd2] bg-white text-center">
        <div className="mb-8">
           <span className="font-bold text-xl">Social Auto Upload</span>
        </div>
        <div className="flex justify-center gap-6 text-sm font-medium text-gray-500 mb-8">
           <a href="#" className="hover:text-[#f54e00]">Twitter</a>
           <a href="#" className="hover:text-[#f54e00]">GitHub</a>
           <a href="#" className="hover:text-[#f54e00]">Terms</a>
           <a href="#" className="hover:text-[#f54e00]">Privacy</a>
        </div>
        <p className="text-xs text-gray-400">© 2024 Social Auto Upload. All rights reserved.</p>
      </footer>
    </div>
  );
}
