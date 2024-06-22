import axios from "axios";

const register = (username, email, password) => {
  return axios.post('/api/registration', {
    username,
    email,
    password,
  },
  {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Bearer '
    }
  }
);
};

const login = (username, password) => {
  return axios
    .post(
      "/api/login",
      {
        username,
        password,
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      }
    )
    .then((response) => {
      console.log(response)
      if (response.data.access_token) {
        localStorage.setItem("access_token",response.data.access_token);
      }

      return response.data;
    });
};


const logout = () => {
  localStorage.removeItem("user");
  localStorage.removeItem("access_token");
  return axios.post("/api/signout").then((response) => {
    return response.data;
  });
};


const AuthService = {
  register,
  login,
  logout,
}

export default AuthService;
