// Check if the user is logged in
$.ajax({
    url: '/check_login',
    type: 'GET',
    success: function(response) {
        if (response.logged_in) {
            loadSchedule();
        } else {
            loadLoginForm();
        }
    },
    error: function(error) {
        console.error('Error checking login status:', error);
    }
});

function loadLoginForm() {
    $('#app').empty();
    $('#app').append(`
        <h2>Login</h2>
        <form id="loginForm">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <br>
            <button type="button" onclick="login()">Login</button>
        </form>
    `);
}

function loadSchedule() {
    // Load and display the schedule based on user role
    $.ajax({
        url: '/schedule',
        type: 'GET',
        success: function(response) {
            $('#app').empty();
            response.forEach(function(lesson) {
                $('#app').append(`
                    <div class="lesson">
                        <p><strong>Teacher:</strong> ${lesson.teacher}</p>
                        <p><strong>Academic Group:</strong> ${lesson.academic_group}</p>
                        <p><strong>Subject:</strong> ${lesson.subject}</p>
                        <p><strong>Day:</strong> ${lesson.day}</p>
                        <p><strong>Class Order:</strong> ${lesson.class_order}</p>
                    </div>
                `);
            });
        },
        error: function(error) {
            console.error('Error loading schedule:', error);
        }
    });
}

function login() {
    // Submit login form
    var username = $('#username').val();
    var password = $('#password').val();

    $.ajax({
        url: '/login',
        type: 'POST',
        data: { username: username, password: password },
        success: function(response) {
            loadSchedule();
        },
        error: function(error) {
            console.error('Login error:', error);
        }
    });
}

$(document).ajaxError(function(event, jqxhr, settings, thrownError) {
    if (jqxhr.status === 401) {
        // Unauthorized, redirect to login
        loadLoginForm();
    }
});
