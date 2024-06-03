// 将 Sun, 26 May 2024 15:50:00 GMT 转换为 2024-05-26 15:50:00
export function formatDate(date) {
    if (!date) {
        return ''
    }
    const d = new Date(date)
    const year = d.getUTCFullYear()
    const month = d.getUTCMonth() + 1
    const day = d.getUTCDate()
    const hour = d.getUTCHours()
    const minute = d.getUTCMinutes()
    const second = d.getUTCSeconds()
    return year + '-' + pad(month) + '-' + pad(day) + ' ' + pad(hour) + ':' + pad(minute) + ':' + pad(second)
}

export function formatTime(date) {
    if (!date) {
        return ''
    }
    const d = new Date(date)
    const hour = d.getUTCHours()
    const minute = d.getUTCMinutes()
    const second = d.getUTCSeconds()
    return pad(hour) + ':' + pad(minute) + ':' + pad(second)
}

function pad(val) {
    return val < 10 ? '0' + val : val
}

// export function formatDates(jsonArray, key) {
//     for (let item of jsonArray) {
//       let date = new Date(item[key]);
//       date.setHours(date.getHours() - 8);
//       item[key] = date.toLocaleString();
//     }
//   }