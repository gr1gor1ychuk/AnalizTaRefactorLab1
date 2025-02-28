function getTeacherOptions() {
    fetch('/teachers')  // Замініть '/teachers' на URL вашого сервера, який повертає вчителів
        .then(response => response.json())
        .then(data => {
            var teacherSelect = document.getElementById('teacher-input');
            teacherSelect.innerHTML = "";  // Очистити попередні опції

            data.forEach(teacher => {
                var option = document.createElement("option");
                option.value = teacher;
                option.textContent = teacher;
                teacherSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

function addLesson() {
    var teacher = document.getElementById('teacher-input').value;
    var academicGroup = document.getElementById('academic-group-input').value;
    var subject = document.getElementById('subject-input').value;
    var day = document.getElementById('day-input').value;
    var classOrder = document.getElementById('class-order-input').value;

    var formData = new FormData();
    formData.append('teacher', teacher);
    formData.append('academic_group', academicGroup);
    formData.append('subject', subject);
    formData.append('day', day);
    formData.append('class_order', classOrder);

    fetch('/lessons/add', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Оновити розклад після успішного додавання
            getLessons();
        } else {
            console.error('Error:', response.statusText);
        }
    })
    .catch(error => console.error('Error:', error));
}
