import axios from 'axios'
let baseURL;


// 检查是否存在非标准端口
const origin = window.location.origin;
if (origin.includes(':')) {
    // 包含非标准端口
    baseURL = origin.replace(/(:\d+)+$/, '') + ':5050';
} else {
    baseURL = origin + ':5050';
}
console.log('baseURL:', baseURL);
// 创建可一个新的axios对象
const request = axios.create({
    // baseURL: 'http://localhost:5050',   // 后端的接口地址  ip:port
    baseURL: baseURL,   // 后端的接口地址  ip:port
    timeout: 100000,
    withCredentials: true  // this will include cookies in requests
})

// request 拦截器
// 可以自请求发送前对请求做一些处理
// 比如统一加token，对请求参数统一加密
request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8';
    // let user = localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : null
    // config.headers['token'] = 'token'  // 设置请求头

    return config
}, error => {
    console.error('request error: ' + error) // for debug
    return Promise.reject(error)
});

// response 拦截器
// 可以在接口响应后统一处理结果
request.interceptors.response.use(
    response => {
        let res = response;
        // res.status = response.status;

        // 兼容服务端返回的字符串数据
        if (typeof res === 'string') {
            res = res ? JSON.parse(res) : res
        }
        return res;
    },
    error => {
        console.error('response error: ' + error) // for debug
        return Promise.reject(error)
    }
)


export default request