import React, { useState, useEffect } from 'react';

const HealthSignup = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [strength, setStrength] = useState({ score: 0, label: '', color: 'bg-gray-200' });
  const [errors, setErrors] = useState({});

  // Password Logic
  const checkStrength = (pass) => {
    let s = 0;
    if (pass.length > 8) s++;
    if (/[A-Z]/.test(pass)) s++;
    if (/[0-9]/.test(pass)) s++;
    if (/[^A-Za-z0-9]/.test(pass)) s++;

    const levels = [
      { label: 'Too Short', color: 'bg-red-400', width: '25%' },
      { label: 'Weak', color: 'bg-orange-400', width: '50%' },
      { label: 'Good', color: 'bg-blue-400', width: '75%' },
      { label: 'Medical Grade', color: 'bg-green-500', width: '100%' }
    ];
    
    return pass.length === 0 ? { width: '0%', label: '', color: 'bg-gray-200' } : levels[s - 1] || levels[0];
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    if (name === 'password') {
      setStrength(checkStrength(value));
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
        <div className="text-center mb-8">
          <div className="inline-block p-3 rounded-full bg-blue-50 mb-4">
            <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-slate-800">Create Patient Account</h2>
          <p className="text-slate-500 text-sm mt-2">Join 10,000+ patients managing their health securely.</p>
        </div>

        <form className="space-y-5">
          {/* Email Field */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Medical Email</label>
            <input
              type="email"
              name="email"
              className="w-full px-4 py-3 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              placeholder="name@hospital.com"
              onChange={handleChange}
            />
          </div>

          {/* Password Field */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Secure Password</label>
            <input
              type="password"
              name="password"
              className="w-full px-4 py-3 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              placeholder="••••••••"
              onChange={handleChange}
            />
            
            {/* Smart Strength Meter */}
            <div className="mt-3">
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-medium text-slate-500">Security Strength:</span>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700">{strength.label}</span>
              </div>
              <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${strength.color}`} 
                  style={{ width: strength.width }}
                ></div>
              </div>
            </div>
          </div>

          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-colors shadow-lg shadow-blue-200">
            Securely Register
          </button>
        </form>

        <p className="text-center text-xs text-slate-400 mt-6">
          By signing up, you agree to our <span className="underline cursor-pointer">HIPAA Privacy Policy</span> and <span className="underline cursor-pointer">Patient Terms of Service</span>.
        </p>
      </div>
    </div>
  );
};

export default HealthSignup;