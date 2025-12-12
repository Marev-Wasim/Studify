"use client"; 

import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; 
import "./login.css"; 
// نستخدم هذا لصور Next.js في جزء Right، إذا لم يكن موجودًا يمكن استبداله بـ <img> عادي
import Image from 'next/image';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter(); 
  
  const handleSubmit = async (e) => {
    e.preventDefault(); 
    setError(null);
    setIsLoading(true);
    
    // نقطة النهاية للباك إند
    //const API_ENDPOINT = 'http://127.0.0.1:5000/auth/login';
    const API_ENDPOINT = `${process.env.NEXT_PUBLIC_API_URL}/auth/login`;

    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify({
          email: email, 
          password: password,
        }),
      });

      const data = await response.json(); 

      if (response.ok) {
        // التوجيه إلى صفحة الرئيسية عند النجاح
        console.log('Login successful:', data);
        router.push('/home'); 
      } else {
        const errorMessage = data.message || 'Login failed. Please check your credentials.';
        setError(errorMessage);
        console.error('Login failed with status:', response.status, data);
      }

    } catch (err) {
      console.error('Network or parsing error:', err);
      setError('Could not connect to the server. Please check your network or try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const hasError = !!error;

  return (
    <>
      <div className="container">
        <div className="left">
          
          {/* تنسيق اللوجو والاسم معتمد على كلاس .brand في CSS */}
          <div className="brand">
            <img 
              src="https://api.builder.io/api/v1/image/assets/TEMP/a972516383bf9672b4c04259e76273dcddd61507?width=328"
              alt="Studify logo"
            />
            <h1>studify</h1>
          </div>

          <h2>Welcome Back!</h2>
          <p>Log in to continue your study journey.</p>

          <form id="loginForm" onSubmit={handleSubmit}> 
            
            <input 
              type="email" 
              id="emailInput" 
              name="email" 
              placeholder="Email Address" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)} 
              // تطبيق كلاس الخطأ من CSS
              className={hasError ? 'error' : ''}
            /> 
            
            <input 
              type="password" 
              id="passwordInput" 
              name="password" 
              placeholder="Password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)} 
              // تطبيق كلاس الخطأ من CSS
              className={hasError ? 'error' : ''}
            /> 

            {/* عرض رسالة الخطأ باللون الأحمر */}
            {error && (
              <div 
                id="errorMessage" 
                className="error-msg" 
                style={{ display: 'block' }} 
              >
                {error}
              </div>
            )}
            
            {/* زر Log In - نعتمد على تنسيق .login-btn في CSS */}
            <button 
              type="submit" 
              className="login-btn" 
              disabled={isLoading} 
            >
              {isLoading ? 'Logging In...' : 'Log In'}
            </button>
          </form>

          <div className="links">
            <a href="#" className="forgot-password-link">Forgot Password?</a>
          </div>

          {/* ************ */}
          {/* تنسيق رابط Sign up ليتطابق مع صفحة التسجيل */}
          <div className="signup-link-container">
            <p className="dont-have">
                Don't have an account? 
                <a 
                    onClick={() => router.push('/signup')} 
                    // استخدام كلاس مخصص للون التركواز
                    className="signup-redirect-link"
                >
                    Sign up
                </a>
            </p>
          </div>
        </div>

        <div className="right">
          <div className="deco-blob blob-1"></div>
          <div className="deco-blob blob-2"></div>
          {/* الصورة التوضيحية */}
          <img src="/download.png" alt="Study illustration" />
        </div>
      </div>
    </>
  );
};


export default LoginPage;
