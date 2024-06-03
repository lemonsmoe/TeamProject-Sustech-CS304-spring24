function collectData() {
    const excludedTime = {"点": []};
    const selectedCells = document.querySelectorAll('.schedule-cell.selected');
    selectedCells.forEach(function (cell) {
        // Times are converted into intervals, adjust the logic as needed
        excludedTime["点"].push([parseInt(cell.dataset.day), parseInt(cell.dataset.period)]);
    });

    const formData = {
        "password": document.getElementById('password').value,
        "student_name": document.getElementById('username').value,
        // 将course处的字符串以空格分隔，然后转换成数组
        "keywords": document.getElementById('course').value.split(' '),
        "badwords": document.getElementById('exclude').value.split(' '),


        "excluded_time": excludedTime,
    };
    return formData;
}

document.addEventListener('DOMContentLoaded', function () {
    const scheduleGrid = document.getElementById('schedule-grid');
    function build_select_table() {
        // 左上角加一个空的格子
        const empty = document.createElement('div');
        empty.classList.add('schedule-cell-row-header');
        empty.textContent = '';
        empty.addEventListener('click', function () {
            empty.classList.toggle('selected');
            // 先判断自己是否被选中，如果没有，则选中全部格子
            if (empty.classList.contains('selected')) {
                const cells = document.querySelectorAll(`.schedule-cell`);
                cells.forEach(function (cell) {
                    cell.classList.add('selected');
                });
            }
            // 如果自己已经被选中，则取消全部格子的选中状态
            else {
                const cells = document.querySelectorAll(`.schedule-cell`);
                cells.forEach(function (cell) {
                    cell.classList.remove('selected');
                });
            }

        });
        scheduleGrid.appendChild(empty);
        // const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        for (let i = 0; i < days.length; i++) {
            const day = document.createElement('div');
            day.classList.add('schedule-cell-column-header');
            day.textContent = days[i];
            day.addEventListener('click', function () {
                day.classList.toggle('selected');
                // 将周一的格子都选中
                const cells = document.querySelectorAll(`.schedule-cell[data-day="${i + 1}"]`);
                cells.forEach(function (cell) {
                    cell.classList.toggle('selected');
                });
            });
            scheduleGrid.appendChild(day);
        }

        for (let j = 0; j < 6; j++) {
            // 写第一节到第五节
            const period = document.createElement('div');
            period.classList.add('schedule-cell-row-header');
            period.textContent = `${j + 1}`;
            period.addEventListener('click', function () {
                period.classList.toggle('selected');
                // 将第一节的格子都选中
                const cells = document.querySelectorAll(`.schedule-cell[data-period="${j + 1}"]`);
                cells.forEach(function (cell) {
                    cell.classList.toggle('selected');
                });
            });
            scheduleGrid.appendChild(period);

            for (let i = 0; i < 7; i++) {
                const cell = document.createElement('div');
                cell.classList.add('schedule-cell');
                // Store day and period info in the dataset for easy retrieval
                cell.dataset.day = i + 1;
                cell.dataset.period = j + 1;

                // Add event listener to toggle the selected state
                cell.addEventListener('click', function () {
                    cell.classList.toggle('selected');
                    // Custom logic to update the excluded time JSON object
                    // will be handled during form submission
                });
                scheduleGrid.appendChild(cell);
            }
        }
    }

    build_select_table();

    const showGrid = document.getElementById('output-grid');
    function build_show_table() {
        // 左上角加一个空的格子
        const empty = document.createElement('div');
        empty.classList.add('output-schedule-cell-row-header');
        empty.textContent = '';
        showGrid.appendChild(empty);
        // const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        for (let i = 0; i < days.length; i++) {
            const day = document.createElement('div');
            day.classList.add('output-schedule-cell-column-header');
            day.textContent = days[i];
            showGrid.appendChild(day);
        }

        for (let j = 0; j < 6; j++) {
            // 写第一节到第五节
            const period = document.createElement('div');
            period.classList.add('output-schedule-cell-row-header');
            period.textContent = `${j + 1}`;
            showGrid.appendChild(period);

            for (let i = 0; i < 7; i++) {
                const cell = document.createElement('div');
                cell.classList.add('output-schedule-cell');
                cell.dataset.day = i + 1;
                cell.dataset.period = j + 1;
                showGrid.appendChild(cell);
            }
        }
    }

    // build_show_table();
    //
    document.getElementById('submit-button').addEventListener('click', function () {
        const formData = collectData();
        sendDataToBackend(formData);
    });

    //监测键盘是否按下ctrl+enter
    document.addEventListener('keydown', function (event) {
        if (event.ctrlKey && event.key === 'Enter') {
            const formData = collectData();
            sendDataToBackend(formData);
        }
    });

    document.getElementById('build-excel-button').addEventListener('click', function () {
        sendBuildExcelRequest();
    });
});

function sendBuildExcelRequest() {
    fetch('/build_excel', {
        method: 'POST'
    })
}

function sendDataToBackend(payload) {
    // console.log(payload); // For demo, outputs to console; Replace with actual backend call
    // Use Fetch API or XMLHttpRequest to send data to your backend
    // fetch('/submit', {...});

    function extracted(data) {
        if ('solution_count' in data) {
            console.log('solution_count in data');
            document.getElementById('solution-count').textContent = data['solution_count'];
            document.getElementById('time-estimate').textContent = (data['solution_count'] * 0.004338).toPrecision(4) + 's';
            if (data['solution_count'] > 0) {
                document.getElementById('solution-count').style.color = 'green';
                document.getElementById('time-estimate').style.color = 'green';
            } else {
                document.getElementById('solution-count').style.color = 'red';
                document.getElementById('time-estimate').style.color = 'red';
            }

        } else {
            console.log('solution_count not in data');
            document.getElementById('solution-count').style.color = 'red';
            document.getElementById('solution-count').textContent = '0';
            document.getElementById('time-estimate').style.color = 'red';
            document.getElementById('time-estimate').textContent = '0s';
        }
    }

    function getinfo(data) {
        if ('info' in data) {
            course = data['info'];
            // course是一个json对象，key是课程名，value是一个数组，数组里面是一个个课程信息
            // 将course的信息显示在页面上
            var course_info = document.getElementById('info');
            course_info.innerHTML = '';
            for (var key in course) {
                var course_name = document.createElement('div');
                course_name.classList.add('course-name');
                course_name.textContent = key;
                course_info.appendChild(course_name);
                for (var i = 0; i < course[key].length; i++) {
                    var course_detail = document.createElement('div');
                    course_detail.classList.add('course-detail');
                    course_detail.textContent = course[key][i];
                    course_info.appendChild(course_detail);
                }
                course_info.appendChild(document.createElement('br'));
            }



        } else {
            console.log('info not in data');
        }
    }

    fetch('/submit_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // 判断key是否存在
            extracted(data);
            getinfo(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}