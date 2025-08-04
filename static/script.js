
        // Global variables
        let courses = [];
        let lessons = [];
        let quizzes = [];
        let students = [];
        let questionCounter = 0;

        // Theme Management
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const themeSelect = document.getElementById('themeSelect');
        
        function setTheme(theme) {
            document.documentElement.setAttribute('data-bs-theme', theme);
            localStorage.setItem('theme', theme);
            
            if (theme === 'dark') {
                themeIcon.className = 'bi bi-moon-fill';
            } else {
                themeIcon.className = 'bi bi-sun-fill';
            }
            
            if (themeSelect) {
                themeSelect.value = theme;
            }
        }

        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        }

        // Initialize theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme);

        themeToggle.addEventListener('click', toggleTheme);
        
        if (themeSelect) {
            themeSelect.addEventListener('change', (e) => {
                setTheme(e.target.value);
            });
        }

        // Navigation Management
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Show selected section
            const targetSection = document.getElementById(sectionId + '-section');
            if (targetSection) {
                targetSection.style.display = 'block';
                targetSection.classList.add('fade-in');
            }
            
            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            const activeLink = document.querySelector(`[data-section="${sectionId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }

        // Sidebar navigation
        document.querySelectorAll('[data-section]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.closest('[data-section]').getAttribute('data-section');
                showSection(section);
            });
        });

        // Mobile sidebar toggle
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebar = document.getElementById('sidebar');
        
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('show');
            });
        }

        // Course Management
        function addCourse() {
            const form = document.getElementById('addCourseForm');
            const formData = new FormData(form);
            
            const course = {
                id: Date.now(),
                name: formData.get('courseName'),
                instructor: formData.get('instructor'),
                description: formData.get('description'),
                price: formData.get('price'),
                duration: formData.get('duration'),
                level: formData.get('level'),
                startDate: formData.get('startDate'),
                endDate: formData.get('endDate'),
                students: 0,
                status: 'نشط',
                createdAt: new Date().toLocaleDateString('ar-SA')
            };
            
            courses.push(course);
            updateCoursesTable();
            updateCourseSelects();
            
            // Close modal and reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById('addCourseModal'));
            modal.hide();
            form.reset();
            
            showNotification('تم إضافة الدورة بنجاح', 'success');
        }

        function updateCoursesTable() {
            const tbody = document.getElementById('coursesTableBody');
            
            if (courses.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center py-4">
                            <div class="empty-state">
                                <i class="bi bi-book"></i>
                                <p class="mb-0">لا توجد دورات متاحة حالياً</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = courses.map(course => `
                <tr>
                    <td>${course.name}</td>
                    <td>${course.instructor}</td>
                    <td>${course.students}</td>
                    <td><span class="badge bg-success">${course.status}</span></td>
                    <td>${course.createdAt}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editCourse(${course.id})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteCourse(${course.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        }

        function updateCourseSelects() {
            const selects = document.querySelectorAll('select[name="courseId"], select[name="enrolledCourses"]');
            
            selects.forEach(select => {
                const currentValue = select.value;
                const isMultiple = select.hasAttribute('multiple');
                
                if (!isMultiple) {
                    select.innerHTML = '<option value="">اختر الدورة</option>';
                } else {
                    select.innerHTML = '';
                }
                
                courses.forEach(course => {
                    const option = document.createElement('option');
                    option.value = course.id;
                    option.textContent = course.name;
                    select.appendChild(option);
                });
                
                if (currentValue) {
                    select.value = currentValue;
                }
            });
        }

        function deleteCourse(id) {
            if (confirm('هل أنت متأكد من حذف هذه الدورة؟')) {
                courses = courses.filter(course => course.id !== id);
                updateCoursesTable();
                updateCourseSelects();
                showNotification('تم حذف الدورة بنجاح', 'success');
            }
        }

        // Lesson Management
        function toggleLessonContent(type) {
            document.getElementById('videoContent').style.display = type === 'video' ? 'block' : 'none';
            document.getElementById('textContent').style.display = type === 'text' ? 'block' : 'none';
            document.getElementById('fileContent').style.display = type === 'file' ? 'block' : 'none';
        }

        function addLesson() {
            const form = document.getElementById('addLessonForm');
            const formData = new FormData(form);
            
            const lesson = {
                id: Date.now(),
                title: formData.get('lessonTitle'),
                courseId: formData.get('courseId'),
                courseName: courses.find(c => c.id == formData.get('courseId'))?.name || 'غير محدد',
                type: formData.get('lessonType'),
                duration: formData.get('duration'),
                description: formData.get('description'),
                content: formData.get('videoUrl') || formData.get('textContent') || formData.get('lessonFile')?.name,
                status: 'نشط',
                createdAt: new Date().toLocaleDateString('ar-SA')
            };
            
            lessons.push(lesson);
            updateLessonsTable();
            
            // Close modal and reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById('addLessonModal'));
            modal.hide();
            form.reset();
            toggleLessonContent('video');
            
            showNotification('تم إضافة الدرس بنجاح', 'success');
        }

        function updateLessonsTable() {
            const tbody = document.getElementById('lessonsTableBody');
            
            if (lessons.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center py-4">
                            <div class="empty-state">
                                <i class="bi bi-play-circle"></i>
                                <p class="mb-0">لا توجد دروس متاحة حالياً</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = lessons.map(lesson => `
                <tr>
                    <td>${lesson.title}</td>
                    <td>${lesson.courseName}</td>
                    <td>
                        <span class="badge bg-info">
                            ${lesson.type === 'video' ? 'فيديو' : lesson.type === 'text' ? 'نص' : 'ملف'}
                        </span>
                    </td>
                    <td>${lesson.duration} دقيقة</td>
                    <td><span class="badge bg-success">${lesson.status}</span></td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editLesson(${lesson.id})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteLesson(${lesson.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        }

        function deleteLesson(id) {
            if (confirm('هل أنت متأكد من حذف هذا الدرس؟')) {
                lessons = lessons.filter(lesson => lesson.id !== id);
                updateLessonsTable();
                showNotification('تم حذف الدرس بنجاح', 'success');
            }
        }

        // Quiz Management
        function addQuestion() {
            questionCounter++;
            const questionsContainer = document.getElementById('questionsContainer');
            
            if (questionsContainer.querySelector('.text-center')) {
                questionsContainer.innerHTML = '';
            }
            
            const questionHtml = `
                <div class="card mb-3" id="question-${questionCounter}">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">السؤال ${questionCounter}</h6>
                            <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeQuestion(${questionCounter})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label class="form-label">نص السؤال</label>
                            <textarea class="form-control" name="question_${questionCounter}" rows="2" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">نوع السؤال</label>
                            <select class="form-select" name="questionType_${questionCounter}" onchange="toggleAnswerOptions(${questionCounter}, this.value)">
                                <option value="multiple">اختيار متعدد</option>
                                <option value="truefalse">صح أم خطأ</option>
                                <option value="text">إجابة نصية</option>
                            </select>
                        </div>
                        <div id="answers_${questionCounter}">
                            <label class="form-label">الخيارات</label>
                            <div class="mb-2">
                                <div class="input-group">
                                    <div class="input-group-text">
                                        <input type="radio" name="correct_${questionCounter}" value="0">
                                    </div>
                                    <input type="text" class="form-control" name="option_${questionCounter}_0" placeholder="الخيار الأول">
                                </div>
                            </div>
                            <div class="mb-2">
                                <div class="input-group">
                                    <div class="input-group-text">
                                        <input type="radio" name="correct_${questionCounter}" value="1">
                                    </div>
                                    <input type="text" class="form-control" name="option_${questionCounter}_1" placeholder="الخيار الثاني">
                                </div>
                            </div>
                            <div class="mb-2">
                                <div class="input-group">
                                    <div class="input-group-text">
                                        <input type="radio" name="correct_${questionCounter}" value="2">
                                    </div>
                                    <input type="text" class="form-control" name="option_${questionCounter}_2" placeholder="الخيار الثالث">
                                </div>
                            </div>
                            <div class="mb-2">
                                <div class="input-group">
                                    <div class="input-group-text">
                                        <input type="radio" name="correct_${questionCounter}" value="3">
                                    </div>
                                    <input type="text" class="form-control" name="option_${questionCounter}_3" placeholder="الخيار الرابع">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            questionsContainer.insertAdjacentHTML('beforeend', questionHtml);
        }

        function removeQuestion(id) {
            document.getElementById(`question-${id}`).remove();
            
            const questionsContainer = document.getElementById('questionsContainer');
            if (questionsContainer.children.length === 0) {
                questionsContainer.innerHTML = `
                    <div class="text-center text-muted py-4">
                        <i class="bi bi-question-circle fs-1"></i>
                        <p>لم يتم إضافة أسئلة بعد</p>
                    </div>
                `;
            }
        }

        function toggleAnswerOptions(questionId, type) {
            const answersDiv = document.getElementById(`answers_${questionId}`);
            
            if (type === 'truefalse') {
                answersDiv.innerHTML = `
                    <label class="form-label">الإجابة الصحيحة</label>
                    <div class="mb-2">
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="correct_${questionId}" value="true" id="true_${questionId}">
                            <label class="form-check-label" for="true_${questionId}">صح</label>
                        </div>
                    </div>
                    <div class="mb-2">
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="correct_${questionId}" value="false" id="false_${questionId}">
                            <label class="form-check-label" for="false_${questionId}">خطأ</label>
                        </div>
                    </div>
                `;
            } else if (type === 'text') {
                answersDiv.innerHTML = `
                    <label class="form-label">الإجابة النموذجية</label>
                    <textarea class="form-control" name="textAnswer_${questionId}" rows="2" placeholder="اكتب الإجابة النموذجية هنا..."></textarea>
                `;
            } else {
                // Multiple choice - restore original options
                answersDiv.innerHTML = `
                    <label class="form-label">الخيارات</label>
                    <div class="mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionId}" value="0">
                            </div>
                            <input type="text" class="form-control" name="option_${questionId}_0" placeholder="الخيار الأول">
                        </div>
                    </div>
                    <div class="mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionId}" value="1">
                            </div>
                            <input type="text" class="form-control" name="option_${questionId}_1" placeholder="الخيار الثاني">
                        </div>
                    </div>
                    <div class="mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionId}" value="2">
                            </div>
                            <input type="text" class="form-control" name="option_${questionId}_2" placeholder="الخيار الثالث">
                        </div>
                    </div>
                    <div class="mb-2">
                        <div class="input-group">
                            <div class="input-group-text">
                                <input type="radio" name="correct_${questionId}" value="3">
                            </div>
                            <input type="text" class="form-control" name="option_${questionId}_3" placeholder="الخيار الرابع">
                        </div>
                    </div>
                `;
            }
        }

        function addQuiz() {
            const form = document.getElementById('addQuizForm');
            const formData = new FormData(form);
            
            const quiz = {
                id: Date.now(),
                title: formData.get('quizTitle'),
                courseId: formData.get('courseId'),
                courseName: courses.find(c => c.id == formData.get('courseId'))?.name || 'غير محدد',
                description: formData.get('description'),
                timeLimit: formData.get('timeLimit'),
                passingScore: formData.get('passingScore'),
                attempts: formData.get('attempts'),
                questions: questionCounter,
                status: 'نشط',
                createdAt: new Date().toLocaleDateString('ar-SA')
            };
            
            quizzes.push(quiz);
            updateQuizzesTable();
            
            // Close modal and reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById('addQuizModal'));
            modal.hide();
            form.reset();
            document.getElementById('questionsContainer').innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-question-circle fs-1"></i>
                    <p>لم يتم إضافة أسئلة بعد</p>
                </div>
            `;
            questionCounter = 0;
            
            showNotification('تم إنشاء الاختبار بنجاح', 'success');
        }

        function updateQuizzesTable() {
            const tbody = document.getElementById('quizzesTableBody');
            
            if (quizzes.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center py-4">
                            <div class="empty-state">
                                <i class="bi bi-question-circle"></i>
                                <p class="mb-0">لا توجد اختبارات متاحة حالياً</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = quizzes.map(quiz => `
                <tr>
                    <td>${quiz.title}</td>
                    <td>${quiz.courseName}</td>
                    <td>${quiz.questions}</td>
                    <td>${quiz.timeLimit} دقيقة</td>
                    <td><span class="badge bg-success">${quiz.status}</span></td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editQuiz(${quiz.id})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteQuiz(${quiz.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        }

        function deleteQuiz(id) {
            if (confirm('هل أنت متأكد من حذف هذا الاختبار؟')) {
                quizzes = quizzes.filter(quiz => quiz.id !== id);
                updateQuizzesTable();
                showNotification('تم حذف الاختبار بنجاح', 'success');
            }
        }

        // Student Management
        function addStudent() {
            const form = document.getElementById('addStudentForm');
            const formData = new FormData(form);
            
            const student = {
                id: Date.now(),
                name: formData.get('studentName'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                enrolledCourses: Array.from(formData.getAll('enrolledCourses')),
                progress: Math.floor(Math.random() * 100),
                registrationDate: new Date().toLocaleDateString('ar-SA'),
                status: 'نشط'
            };
            
            students.push(student);
            updateStudentsTable();
            
            // Close modal and reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById('addStudentModal'));
            modal.hide();
            form.reset();
            
            showNotification('تم إضافة الطالب بنجاح', 'success');
        }

        function updateStudentsTable() {
            const tbody = document.getElementById('studentsTableBody');
            
            if (students.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center py-4">
                            <div class="empty-state">
                                <i class="bi bi-people"></i>
                                <p class="mb-0">لا يوجد طلاب مسجلين حالياً</p>
                            </div>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = students.map(student => `
                <tr>
                    <td>${student.name}</td>
                    <td>${student.email}</td>
                    <td>${student.enrolledCourses.length}</td>
                    <td>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar" style="width: ${student.progress}%">${student.progress}%</div>
                        </div>
                    </td>
                    <td>${student.registrationDate}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editStudent(${student.id})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteStudent(${student.id})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        }

        function deleteStudent(id) {
            if (confirm('هل أنت متأكد من حذف هذا الطالب؟')) {
                students = students.filter(student => student.id !== id);
                updateStudentsTable();
                showNotification('تم حذف الطالب بنجاح', 'success');
            }
        }

        // Notification System
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            notification.style.cssText = 'top: 20px; left: 20px; z-index: 9999; min-width: 300px;';
            notification.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        }

        // Update current date and time
        function updateDateTime() {
            const now = new Date();
            const options = {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            
            const dateTimeElement = document.getElementById('currentDateTime');
            if (dateTimeElement) {
                dateTimeElement.textContent = now.toLocaleDateString('ar-SA', options);
            }
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            updateDateTime();
            setInterval(updateDateTime, 60000); // Update every minute
            
            // Initialize empty tables
            updateCoursesTable();
            updateLessonsTable();
            updateQuizzesTable();
            updateStudentsTable();
        });

        // Handle modal events to update course selects
        document.addEventListener('shown.bs.modal', function(e) {
            if (e.target.id === 'addLessonModal' || e.target.id === 'addQuizModal' || e.target.id === 'addStudentModal') {
                updateCourseSelects();
            }
        });
