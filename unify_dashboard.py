
import os

path_student = 'dashboard/templates/dashboard/studentDashboard/studentDashboard.html'
path_staff = 'dashboard/templates/dashboard/staffDashboard/staffDashboard.html'

with open(path_student, 'r', encoding='utf-8') as f:
    content = f.read()

# Split at Sidebar Start
sidebar_marker = '<!-- Start Dashboard Sidebar  -->'
parts = content.split(sidebar_marker)
header_part = parts[0]
remaining = parts[1]

# Split remaining at Content Start
# content_marker = '<div class="col-lg-9">' 
# Actually, let's find where sidebar ends and content starts.
# In studentDashboard:
# <!-- End Dashboard Sidebar -->
# </div>
# <div class="col-lg-9">

middle_marker = '<div class="col-lg-9">'
parts2 = remaining.split(middle_marker)
# parts2[0] contains the old sidebar and closing col-lg-3 div.
# parts2[1] contains the dashboard content.

# We will ignore parts2[0] (old sidebar) and construct new sidebar.
# We will ignore parts2[1] (old content) up to footer?
# No, we need the end of the file.

# Let's find end of content.
content_end_marker = '<!-- End Card Style -->'
parts3 = parts2[1].split(content_end_marker)
footer_part = content_end_marker + parts3[1]

# New Sidebar HTML
new_sidebar = """<!-- Start Dashboard Sidebar  -->
                            <div class="rbt-default-sidebar sticky-top rbt-shadow-box rbt-gradient-border">
                                <div class="inner">
                                    <div class="content-item-content">

                                        <div class="rbt-default-sidebar-wrapper">
                                            <div class="section-title mb--20">
                                                <h6 class="rbt-title-style-2">Welcome, {{ request.user.first_name|default:"Instructor" }} {{ request.user.last_name }}</h6>
                                            </div>
                                            <nav class="mainmenu-nav">
                                                <ul class="dashboard-mainmenu rbt-default-sidebar-list">
                                                    <li><a href="{% url 'instructorDashboard' %}"><i class="feather-home"></i><span>Dashboard</span></a></li>
                                                    <li><a href="{% url 'instructorProfile' %}"><i class="feather-user"></i><span>My Profile</span></a></li>
                                                    <li><a href="{% url 'instructorEnrolledCourses' %}"><i class="feather-book-open"></i><span>Enrolled Courses</span></a></li>
                                                    <li><a href="{% url 'instructorWishlist' %}"><i class="feather-bookmark"></i><span>Wishlist</span></a></li>
                                                    <li><a href="{% url 'instructorReviews' %}"><i class="feather-star"></i><span>Reviews</span></a></li>
                                                    <li><a href="{% url 'instructorMyQuizAttempts' %}"><i class="feather-help-circle"></i><span>My Quiz Attempts</span></a></li>
                                                    <li><a href="{% url 'instructorOrderHistory' %}"><i class="feather-shopping-bag"></i><span>Order History</span></a></li>
                                                </ul>
                                            </nav>

                                            <div class="section-title mt--40 mb--20">
                                                <h6 class="rbt-title-style-2">Instructor</h6>
                                            </div>

                                            <nav class="mainmenu-nav">
                                                <ul class="dashboard-mainmenu rbt-default-sidebar-list">
                                                    <li><a href="{% url 'instructorCourse' %}"><i class="feather-monitor"></i><span>My Courses</span></a></li>
                                                    <li><a href="{% url 'instructorAnnouncements' %}"><i class="feather-volume-2"></i><span>Announcements</span></a></li>
                                                    <li><a href="{% url 'instructorQuizAttempts' %}"><i class="feather-message-square"></i><span>Quiz Attempts</span></a></li>
                                                    <li><a href="{% url 'instructorAssignments' %}"><i class="feather-list"></i><span>Assignments</span></a></li>
                                                </ul>
                                            </nav>

                                            <div class="section-title mt--40 mb--20">
                                                <h6 class="rbt-title-style-2">User</h6>
                                            </div>

                                            <nav class="mainmenu-nav">
                                                <ul class="dashboard-mainmenu rbt-default-sidebar-list">
                                                    <li><a href="{% url 'instructorSettings' %}"><i class="feather-settings"></i><span>Settings</span></a></li>
                                                    <li><a href="#"><i class="feather-log-out"></i><span>Logout</span></a></li>
                                                </ul>
                                            </nav>
                                        </div>

                                    </div>
                                </div>
                            </div>
                            <!-- End Dashboard Sidebar  -->
                        </div>

                        """

# New Content HTML
new_content = """<div class="col-lg-9">
                            <div class="rbt-dashboard-content bg-color-white rbt-shadow-box mb--60">
                                <div class="content">
                                    <div class="section-title">
                                        <h4 class="rbt-title-style-3">Dashboard</h4>
                                    </div>
                                    <div class="row g-5">

                                        <!-- Start Single Card  -->
                                        <div class="col-lg-4 col-md-4 col-sm-6 col-12">
                                            <div class="rbt-counterup variation-01 rbt-hover-03 rbt-border-dashed bg-primary-opacity">
                                                <div class="inner">
                                                    <div class="rbt-round-icon bg-primary-opacity">
                                                        <i class="feather-book-open"></i>
                                                    </div>
                                                    <div class="content">
                                                        <h3 class="counter without-icon color-primary"><span class="odometer" data-count="30">00</span>
                                                        </h3>
                                                        <span class="rbt-title-style-2 d-block">Enrolled Courses</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- End Single Card  -->

                                        <!-- Start Single Card  -->
                                        <div class="col-lg-4 col-md-4 col-sm-6 col-12">
                                            <div class="rbt-counterup variation-01 rbt-hover-03 rbt-border-dashed bg-secondary-opacity">
                                                <div class="inner">
                                                    <div class="rbt-round-icon bg-secondary-opacity">
                                                        <i class="feather-monitor"></i>
                                                    </div>
                                                    <div class="content">
                                                        <h3 class="counter without-icon color-secondary"><span class="odometer" data-count="10">00</span>
                                                        </h3>
                                                        <span class="rbt-title-style-2 d-block">ACTIVE COURSES</span>
                                                    </div>
                                                </div>
                                            </div>

                                        </div>
                                        <!-- End Single Card  -->

                                        <!-- Start Single Card  -->
                                        <div class="col-lg-4 col-md-4 col-sm-6 col-12">
                                            <div class="rbt-counterup variation-01 rbt-hover-03 rbt-border-dashed bg-violet-opacity">
                                                <div class="inner">
                                                    <div class="rbt-round-icon bg-violet-opacity">
                                                        <i class="feather-award"></i>
                                                    </div>
                                                    <div class="content">
                                                        <h3 class="counter without-icon color-violet"><span class="odometer" data-count="7">00</span>
                                                        </h3>
                                                        <span class="rbt-title-style-2 d-block">Completed Courses</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- End Single Card  -->

                                        <!-- Start Single Card  -->
                                        <div class="col-lg-4 col-md-4 col-sm-6 col-12">
                                            <div class="rbt-counterup variation-01 rbt-hover-03 rbt-border-dashed bg-pink-opacity">
                                                <div class="inner">
                                                    <div class="rbt-round-icon bg-pink-opacity">
                                                        <i class="feather-users"></i>
                                                    </div>
                                                    <div class="content">
                                                        <h3 class="counter without-icon color-pink"><span class="odometer" data-count="160">00</span>
                                                        </h3>
                                                        <span class="rbt-title-style-2 d-block">Total Students</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- End Single Card  -->

                                        <!-- Start Single Card  -->
                                        <div class="col-lg-4 col-md-4 col-sm-6 col-12">
                                            <div class="rbt-counterup variation-01 rbt-hover-03 rbt-border-dashed bg-coral-opacity">
                                                <div class="inner">
                                                    <div class="rbt-round-icon bg-coral-opacity">
                                                        <i class="feather-gift"></i>
                                                    </div>
                                                    <div class="content">
                                                        <h3 class="counter without-icon color-coral"><span class="odometer" data-count="20">00</span>
                                                        </h3>
                                                        <span class="rbt-title-style-2 d-block">Total Courses</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- End Single Card  -->

                                        <!-- Start Single Card  -->
                                        <div class="col-lg-4 col-md-4 col-sm-6 col-12">
                                            <div class="rbt-counterup variation-01 rbt-hover-03 rbt-border-dashed bg-warning-opacity">
                                                <div class="inner">
                                                    <div class="rbt-round-icon bg-warning-opacity">
                                                        <i class="feather-dollar-sign"></i>
                                                    </div>
                                                    <div class="content">
                                                        <h3 class="counter color-warning"><span class="odometer" data-count="25000">00</span>
                                                        </h3>
                                                        <span class="rbt-title-style-2 d-block">Total Earnings</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!-- End Single Card  -->

                                    </div>
                                </div>
                            </div>
                            
                            <!-- Start My Courses Table Section -->
                            <div class="rbt-dashboard-content bg-color-white rbt-shadow-box mb--60">
                                <div class="content">
                                    <div class="row">
                                        <div class="col-lg-12">
                                            <div class="section-title">
                                                <h4 class="rbt-title-style-3">My Courses</h4>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="row gy-5">
                                        <div class="col-lg-12">
                                            <div class="rbt-dashboard-table table-responsive">
                                                <table class="rbt-table table table-borderless">
                                                    <thead>
                                                        <tr>
                                                            <th>Course Name</th>
                                                            <th>Enrolled</th>
                                                            <th>Rating</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr>
                                                            <th><a href="#">Accounting</a></th>
                                                            <td>50</td>
                                                            <td>
                                                                <div class="rating">
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <th><a href="#">Marketing</a></th>
                                                            <td>40</td>
                                                            <td>
                                                                <div class="rating">
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <th><a href="#">Web Design</a></th>
                                                            <td>75</td>
                                                            <td>
                                                                <div class="rating">
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <th><a href="#">Graphic</a></th>
                                                            <td>20</td>
                                                            <td>
                                                                <div class="rating">
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="fas fa-star"></i>
                                                                    <i class="off fas fa-star"></i>
                                                                    <i class="off fas fa-star"></i>
                                                                    <i class="off fas fa-star"></i>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>

                                            <div class="load-more-btn text-center">
                                                <a class="rbt-btn-link" href="#">Browse All Course<i class="feather-arrow-right"></i></a>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <!-- End My Courses Table Section -->

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

# Assemble Full Content
final_content = header_part + new_sidebar + new_content + footer_part

# Write to file
with open(path_staff, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Successfully created staffDashboard.html")
