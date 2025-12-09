 <div class="container">
        <header>
            <div class="logo-section">
                <img src="https://api.builder.io/api/v1/image/assets/TEMP/a972516383bf9672b4c04259e76273dcddd61507?width=328"
                    alt="Studify logo">
                <h1>studify</h1>
            </div>
            <nav>
                <a href="Home.html">Home</a> <a href="friends.html">Friends</a> <a href="#about">About us</a>
            </nav>
            <button class="mobile-menu-btn">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16">
                    </path>
                </svg>
            </button>
            <div class="header-blob"></div>
        </header>

        <main>
            <img class="deco-image left"
                src="https://api.builder.io/api/v1/image/assets/TEMP/24375f52f9e1b8b805b0963c3072fcbb6a9bb0df?width=296"
                alt="">
            <img class="deco-image bottom-left"
                src="https://api.builder.io/api/v1/image/assets/TEMP/fa793776abd3adf2301513f8cfb90a229732362f?width=374"
                alt="">
            <img class="deco-image top-left"
                src="https://api.builder.io/api/v1/image/assets/TEMP/fa793776abd3adf2301513f8cfb90a229732362f?width=374"
                alt="">
            <img class="deco-image right"
                src="https://api.builder.io/api/v1/image/assets/TEMP/e847a0dd2b30751e0856b81ae858e79a43d5e4d1?width=374"
                alt="">

            <div class="content-grid">
                <div class="profile-section">
                    <h2>My Profile</h2>
                    <div class="profile-card">
                        <div class="avatar-wrapper">
                            <div class="avatar">
                                <img src="https://api.builder.io/api/v1/image/assets/TEMP/14b992f93b6150097c71e1c5dd691af6b6bee56e?width=318"
                                    alt="Profile avatar">
                            </div>
                        </div>
                        <div class="profile-info">
                            <h3 id="profileName">Name Of Account</h3>
                            <p id="profileEmail">email@address.com</p>
                            <p id="passwordLabel" style="font-weight: bold; font-size: 1rem; color: #0a2139;">Password:
                                <span id="profilePassword"
                                    style="font-weight: normal; color: rgba(0,0,0,0.6);">********</span>
                            </p>

                            <button class="btn-edit" id="editBtn">Edit Profile</button>
                        </div>
                    </div>
                </div>

                <div class="hours-card">
                    <h3>Total Learning Hours</h3>
                    <p class="hours-value">120 Hours</p>
                    <div class="progress-container">
                        <div class="progress-fill"></div>
                    </div>
                    <p class="hours-text">Next Reward at 200 Hours</p>
                </div>
            </div>

            <div class="bottom-grid">
                <div class="progress-carousel">
                    <button class="carousel-btn" id="btnLeft">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7">
                            </path>
                        </svg>
                    </button>

                    <div class="carousel-scroll" id="carousel">
                        <div class="progress-card">
                            <h4>Subject Progress</h4>
                            <div class="progress-circle">
                                <svg class="progress-ring" width="90" height="90" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="40" stroke="#e5e7eb" stroke-width="8" fill="none" />
                                    <circle cx="50" cy="50" r="40" stroke="#4cd4d0" stroke-width="8" fill="none"
                                        stroke-dasharray="226.2 251.2" stroke-linecap="round" />
                                </svg>
                            </div>
                            <p>9/10 Tasks</p>
                        </div>

                        <div class="progress-card">
                            <h4>Subject Progress</h4>
                            <div class="progress-circle">
                                <svg class="progress-ring" width="90" height="90" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="40" stroke="#e5e7eb" stroke-width="8" fill="none" />
                                    <circle cx="50" cy="50" r="40" stroke="#4cd4d0" stroke-width="8" fill="none"
                                        stroke-dasharray="125.6 251.2" stroke-linecap="round" />
                                </svg>
                            </div>
                            <p>5/10 Tasks</p>
                        </div>

                        <div class="progress-card history">
                            <h4>History</h4>
                            <div style="height: 106px;"></div>
                            <p>View Log</p>
                        </div>

                        <div class="progress-card">
                            <h4>Physics</h4>
                            <div class="progress-circle">
                                <svg class="progress-ring" width="90" height="90" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="40" stroke="#e5e7eb" stroke-width="8" fill="none" />
                                    <circle cx="50" cy="50" r="40" stroke="#4cd4d0" stroke-width="8" fill="none"
                                        stroke-dasharray="100 251.2" stroke-linecap="round" />
                                </svg>
                            </div>
                            <p>4/10 Tasks</p>
                        </div>

                        <div class="progress-card">
                            <h4>Chemistry</h4>
                            <div class="progress-circle">
                                <svg class="progress-ring" width="90" height="90" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="40" stroke="#e5e7eb" stroke-width="8" fill="none" />
                                    <circle cx="50" cy="50" r="40" stroke="#4cd4d0" stroke-width="8" fill="none"
                                        stroke-dasharray="200 251.2" stroke-linecap="round" />
                                </svg>
                            </div>
                            <p>8/10 Tasks</p>
                        </div>
                    </div>

                    <button class="carousel-btn" id="btnRight">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7">
                            </path>
                        </svg>
                    </button>
                </div>

                <div class="reward-card">
                    <div class="reward-icon">
                        <svg viewBox="0 0 125 118" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M59.2941 2.06119C60.1996 -0.687026 64.0872 -0.687034 64.9927 2.06118L77.6293 40.4123C78.0346 41.6424 79.1835 42.4735 80.4786 42.4735H121.281C124.197 42.4735 125.399 46.2137 123.028 47.9122L90.0909 71.5103C89.0247 72.2741 88.5784 73.6421 88.9888 74.8878L101.587 113.122C102.495 115.878 99.3496 118.19 96.9903 116.499L63.8906 92.7851C62.8461 92.0367 61.4408 92.0367 60.3962 92.7851L27.2966 116.499C24.9373 118.19 21.7918 115.878 22.7001 113.122L35.298 74.8878C35.7085 73.6421 35.2621 72.2741 34.1959 71.5103L1.25853 47.9122C-1.11215 46.2137 0.0894127 42.4735 3.00573 42.4735H43.8083C45.1034 42.4735 46.2523 41.6424 46.6576 40.4123L59.2941 2.06119Z"
                                fill="#E5982E" />
                            <path
                                d="M55.765 1.38194C56.3637 -0.460681 58.9705 -0.460687 59.5692 1.38193L71.8115 39.0598C72.0792 39.8838 72.8472 40.4417 73.7136 40.4417H113.33C115.268 40.4417 116.073 42.921 114.506 44.0598L82.4553 67.3459C81.7543 67.8552 81.461 68.758 81.7288 69.582L93.971 107.26C94.5697 109.102 92.4608 110.635 90.8934 109.496L58.8427 86.2097C58.1417 85.7004 57.1925 85.7004 56.4915 86.2097L24.4409 109.496C22.8734 110.635 20.7645 109.102 21.3632 107.26L33.6055 69.582C33.8732 68.758 33.5799 67.8552 32.8789 67.3459L0.828241 44.0598C-0.739186 42.921 0.0663619 40.4417 2.00381 40.4417H41.6206C42.4871 40.4417 43.255 39.8838 43.5227 39.0598L55.765 1.38194Z"
                                fill="#F9C440" />
                        </svg>
                    </div>
                    <div class="reward-text">
                        <h3>Reward Points Earned</h3>
                        <p>2500</p>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // --- كود تحريك الكروت (Carousel) ---
        const carousel = document.getElementById('carousel');
        const btnLeft = document.getElementById('btnLeft');
        const btnRight = document.getElementById('btnRight');

        btnLeft.addEventListener('click', () => {
            const width = carousel.clientWidth;
            carousel.scrollBy({ left: -width, behavior: 'smooth' });
        });

        btnRight.addEventListener('click', () => {
            const width = carousel.clientWidth;
            carousel.scrollBy({ left: width, behavior: 'smooth' });
        });

        // --- كود تعديل البروفايل (اسم + باسوورد فقط) ---
        const profileName = document.getElementById('profileName');
        const profileEmail = document.getElementById('profileEmail'); // لن يتم تعديله
        const profilePassword = document.getElementById('profilePassword'); // النص الذي يحتوي على النجوم
        const editBtn = document.getElementById('editBtn');

        let isEditing = false;

        editBtn.addEventListener('click', function () {
            if (!isEditing) {
                // --- وضع التعديل ---
                const currentName = profileName.innerText;

                // تحويل الاسم إلى Input
                profileName.innerHTML = `<input type="text" class="edit-input" id="nameInput" value="${currentName}">`;

                // تحويل الباسوورد إلى Input (فارغ أو يمكن وضع قيمة افتراضية)
                profilePassword.innerHTML = `<input type="password" class="edit-input" id="passwordInput" placeholder="New Password">`;

                // تغيير شكل الزر
                editBtn.innerText = "Save Changes";
                editBtn.style.background = "#34BDAD";
                isEditing = true;
            } else {
                // --- وضع الحفظ ---
                const nameInput = document.getElementById('nameInput');
                const passwordInput = document.getElementById('passwordInput');

                // حفظ الاسم الجديد
                profileName.innerText = nameInput.value;

                // إعادة الباسوورد لشكل نجوم (لا نظهر الباسوورد الجديد)
                // في تطبيق حقيقي، هنا نرسل البيانات للسيرفر
                if (passwordInput.value.length > 0) {
                    profilePassword.innerText = "********";
                } else {
                    profilePassword.innerText = "********";
                }

                // إرجاع الزر لوضعه الأصلي
                editBtn.innerText = "Edit Profile";
                editBtn.style.background = "#4a7fb8";
                isEditing = false;
            }
        });
    </script>
</body>