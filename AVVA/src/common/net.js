import axios from 'axios'
axios.interceptors.request.use(function (config) {
  const token = localStorage.getItem('access_token')
  if (token){
    config.headers.Authorization = "Bearer " + token;
  }
  return config;
}, function (error) {
  return Promise.reject(error);
});

console.log('intercepter registrated')