import axios from 'axios'

const getGeneralReport = () => {
  return axios.get('/api/general/report')
} 

const ReportService = {
  getGeneralReport,
}

export default ReportService;

