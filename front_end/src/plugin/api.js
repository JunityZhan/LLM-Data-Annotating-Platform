import axios from 'axios'

// 请求拦截器
axios.interceptors.request.use(
    config => {
        // 如果存在token，请求携带这个token
        if (window.localStorage.getItem('Authorization')) {
            config.headers.Authorization = window.localStorage.getItem('Authorization')
        }
        return config
    },
    error => {
        console.log(error)
    }
)
// axios.interceptors.response.use(
//     success => {
//         console.log("响应拦截器")
//     },
//     error => {
//         console.log(error)
//     }
// )

const base = ''

// 传送json格式的post请求
export const postRequest = (url, params, config) => {
    return axios({
        method: 'post',
        url: `${base}${url}`,
        data: params,
        config,
        withCredentials: true
    })
}

// 传送json的put请求
export const putRequest = (url, params) => {
    return axios({
        method: 'put',
        url: `${base}${url}`,
        data: params,
    })
}

// 传送json的get请求
export const getRequest = (url, params) => {
    return axios({
        method: 'get',
        url: `${base}${url}`,
        data: params
    })
}

// 传送json的delete请求
export const deleteRequest = (url, params) => {
    return axios({
        method: 'delete',
        url: `${base}${url}`,
        data: params
    })
}