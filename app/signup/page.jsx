"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation'; 
import Image from 'next/image'; 
import "./signup.css"; // استيراد ملف CSS

/**
 * دالة المكون الرئيسي للتسجيل
 */
export default function SignupForm() {
  const router = useRouter(); 

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
  });
  // حالة رسالة الخطأ
  const [passwordError, setPasswordError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false); 

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value,
    }));
    if (passwordError) {
      setPasswordError('');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    setPasswordError('');

    // التحقق من تطابق كلمة المرور
    if (formData.password !== formData.confirm_password) {
      setPasswordError('Error: The password and confirmation password do not match!');
      setIsSubmitting(false);
      return; 
    }

    // const backendUrl = 'http://127.0.0.1:5000/auth/register'; 
    const backendUrl = `${process.env.NEXT_PUBLIC_API_URL}/auth/signup`;

    try {
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          confirm_password: formData.confirm_password,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        alert('Account created successfully! Please log in with your new credentials.');
        router.push('/login'); 
      } else {
        setPasswordError(result.message || 'Signup failed. Please try again.');
      }
    } catch (error) {
      console.error('Submission Error:', error);
      setPasswordError('Network error or server connection failed.');
    } finally {
      setIsSubmitting(false); 
    }
  };

  // تطبيق كلاس input-error إذا كان هناك خطأ
  const hasError = !!passwordError;

  return (
    <div className="container">

      <div className="left">

        <div className="brand">
          {/* الصورة الآن ستأخذ تنسيقها من .brand img في CSS */}
          <img
            src="https://api.builder.io/api/v1/image/assets/TEMP/a972516383bf9672b4c04259e76273dcddd61507?width=328" 
            alt="Studify logo" 
            // تم حذف style={{ width: '150px', height: 'auto' }}
          />
          <h1>studify</h1>
        </div>

        {/* تم تعديل h2 ليتوافق مع .brand top:-130px و h2 margin-top: -70px */}
        <h2>Join Studify Today!</h2>
        <p>Join us and start your study journey!</p>

        <form onSubmit={handleSubmit} method="POST">
            <div className="form-row">
            <input 
              type="text" 
              name="username" 
              placeholder="Full Name" 
              value={formData.username}
              onChange={handleChange}
              required 
            />
            <input 
              type="email" 
              name="email" 
              placeholder="Email Address" 
              value={formData.email}
              onChange={handleChange}
              required 
            />
          </div>

        <div className="form-row">
            <input 
              type="password" 
              name="password" 
              placeholder="Password" 
              value={formData.password}
              onChange={handleChange}
              // تطبيق كلاس الخطأ من CSS
              className={hasError ? 'input-error' : ''} 
              required 
            />
            <input 
              type="password" 
              name="confirm_password" 
              placeholder="Confirm Password"
              value={formData.confirm_password}
              onChange={handleChange}
              // تطبيق كلاس الخطأ من CSS
              className={hasError ? 'input-error' : ''} 
              required 
            />
          </div>
          
          {/* عرض رسالة الخطأ - نعتمد على تنسيق CSS لكن نحافظ على display:block لعرضها */}
          <div 
            id="password-error-msg" 
            className="error-msg" 
            style={{ display: passwordError ? 'block' : 'none', marginTop: '-10px' }} 
            // نعتمد على تنسيق .error-msg في CSS
          >
            {passwordError}
          </div>

          <button 
            type="submit" 
            className="create-btn"
            disabled={isSubmitting}
            // تم حذف style={{ marginBottom: '15px' }} والاعتماد على margin-top: 20px في CSS
          >
            {isSubmitting ? 'Creating...' : 'Create Account'}
          </button>

        </form>
        
        {/* ************ */}
        {/* رابط Log In - تم حذف الأنماط الداخلية والاعتماد على CSS */}
        {/* ************ */}
        <div className="login-link-container">
            <p className="dont-have" style={{ textAlign: 'left', marginBottom: '5px', marginTop: '10px' }}> {/* تم تعديل محاذاة النص داخل p */}
                Already have an account? 
                <a 
                    onClick={() => router.push('/login')} 
                    // استخدام كلاس مخصص لتطبيق لون التركواز
                    className="login-redirect-link"
                >
                    Log In
                </a>
            </p>
        </div>


      </div>

      <div className="right">
        <div className="deco-blob blob-1"></div>
        <div className="deco-blob blob-2"></div>
        
        {/* الصورة التوضيحية */}
        <Image
          src="/download.png" 
          alt="Study illustration" 
          width={500} 
          height={500} 
        />
      </div>

    </div>
  );
}
