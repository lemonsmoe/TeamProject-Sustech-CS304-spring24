var current_page = 1;
var current_sheme = {};
var all_colors = [
    '#FFCC99', '#FFCCCC', '#CCFF99', '#CCCCFF', '#FF99CC', '#99CCFF', '#CCFFFF', '#FFFFCC',
    '#f3ad45', '#b5f851', '#49b1f6', '#ef42a8', '#FFE5CC', '#CCE5FF', '#abfd59', '#45f19b'
];
function update_table(key) {
    // 清空原来的课表
    const cells = document.querySelectorAll(`.output-cell`);
    cells.forEach(function (cell) {
        cell.textContent = '';
        cell.style.backgroundColor = '#FFFDD1BF'
    });
    // 改变page-count的元素，显示当前是第几个方案
    const page_count = document.getElementById('page-count');
    page_count.textContent = key;
    // 将data里面的课程显示在课表上,data是一个json，key是第几个方案，value是一个数组，数组里面是一个个课程
    //     console.log(key);
        key = key-1;
        // console.log(current_sheme[key]);
        course_list = current_sheme[key];
        total_credit = 0;
        for (var i = 0; i < course_list.length; i++) {
            // console.log(course_list[i]);
            course_times = course_list[i]['上课时间'];
            course_name = course_list[i]['教学班'];
            course_credit = course_list[i]['学分'];
            total_credit = total_credit + course_credit;
            // console.log(course_times);
            // course_times是一个数组，数组里面是一个个上课时间,类似[1, 1, 2, true, true]代表周一的第一节课到第二节课
            // 在grid中找到对应位置，将课程名显示在上面
            for (var j = 0; j < course_times.length; j++) {
                day = course_times[j][0];
                period_start = course_times[j][1];
                period_end = course_times[j][2];
                odd = course_times[j][3];
                even = course_times[j][4];
                // 找到对应的格子
                for (var k = period_start; k <= period_end; k++) {
                    const cell = document.querySelector(`.output-cell[data-day="${day}"][data-period="${k}"]`);
                    cell.textContent += course_name;
                    if (odd == true && even == false) {
                        cell.textContent += '(单)';
                    }
                    if (even == true && odd == false) {
                        cell.textContent += '(双)';
                    }
                    if (even == true && odd == true) {
                        cell.textContent += '(全)';
                    }
                    cell.textContent += '\n';
                    // 将格子的颜色改变
                    cell.style.backgroundColor = all_colors[i % all_colors.length];
                }
            }

        }
        // 显示总学分
    const cell = document.querySelector(`.output-cell[data-day="${7}"][data-period="${1}"]`);
    cell.textContent = `总学分：${total_credit}`;
}

document.addEventListener('DOMContentLoaded', function () {
    const outputGrid = document.getElementById('output-grid');
    function build_output_table() {
        // 左上角加一个空的格子
        const empty = document.createElement('div');
        empty.classList.add('output-cell-row-header');
        empty.textContent = '';
        outputGrid.appendChild(empty);
        // const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        for (let i = 0; i < days.length; i++) {
            const day = document.createElement('div');
            day.classList.add('output-cell-column-header');
            day.textContent = days[i];
            outputGrid.appendChild(day);
        }

        for (let j = 0; j < 6; j++) {
            // 写第一节到第五节
            const period = document.createElement('div');
            period.classList.add('output-cell-row-header');
            period.textContent = `${j + 1}`;
            outputGrid.appendChild(period);

            for (let i = 0; i < 7; i++) {
                const cell = document.createElement('div');
                cell.classList.add('output-cell');
                // Store day and period info in the dataset for easy retrieval
                cell.dataset.day = i + 1;
                cell.dataset.period = j + 1;
                outputGrid.appendChild(cell);
            }
        }
    }

    build_output_table();




    function getJsonfromBackend() {
        fetch('/get_scheme', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // 判断data是否为空
            if (data.length == 0) {
                console.log('data is empty');
            }
            else{
                // 更新课表
                current_sheme = data;
                console.log(Object.keys(current_sheme).length);
                current_page = 1;
                update_table(current_page);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    //
    document.getElementById('get-scheme-button').addEventListener('click', function () {
        getJsonfromBackend();
    });

    document.getElementById('next-page-button').addEventListener('click', function () {
        if (current_page < Object.keys(current_sheme).length) {
            current_page = current_page + 1;
            update_table(current_page);
        }
    });

    document.getElementById('previous-page-button').addEventListener('click', function () {
        if (current_page > 1) {
            current_page = current_page - 1;
            update_table(current_page);
        }
    });

    //检测键盘事件
    document.onkeydown = function (event) {
        var e = event || window.event || arguments.callee.caller.arguments[0];
        // 按下右键
        if (e && e.keyCode == 39) {
            if (current_page < Object.keys(current_sheme).length) {
                current_page = current_page + 1;
                update_table(current_page);
            }
        }
        // 按下左键
        if (e && e.keyCode == 37) {
            if (current_page > 1) {
                current_page = current_page - 1;
                update_table(current_page);
            }
        }
    };
});