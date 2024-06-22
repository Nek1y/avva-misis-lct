import axios from "axios";

const getPublicContent = () => {
    return axios.get("/api/all");
};

const getUserBoard = () => {
    return axios.get("/api/user");
};

const getModeratorBoard = () => {
    return axios.get("/api/mod");
};

const getAdminBoard = () => {
    return axios.get("/api/admin");
};

const getCurrentUser = async () => {
    return (await axios.get('/api/users/me')).data
  };
  

const UserService = {
    getPublicContent,
    getUserBoard,
    getModeratorBoard,
    getAdminBoard,
    getCurrentUser,
}

export default UserService;

