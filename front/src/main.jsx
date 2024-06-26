import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider} from "react-router-dom";
import { AuthProvider } from './hoc/PrivateRoute';
import { PrivateRoute } from './hoc/PrivateRoute.jsx';
import LoginPage from './pages/Login/LoginPage.jsx';
import CreateReportPage from './pages/CreateReportPage/CreateReportPage.jsx';
import MyReportPage from './pages/MyReportsPage/MyReportPage.jsx';
import MyTemplatePage from './pages/MyTemplatePage/MyTemplatePage.jsx';
import ProfilePage from './pages/ProfilePage/ProfilePage.jsx';
import FaqPage from './pages/FaqPage/FaqPage.jsx';

const routes = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />
  },
  {
    path: '/createreport',
    element: <PrivateRoute><CreateReportPage/></PrivateRoute>
  },
  {
    path: '/myreports',
    element: <MyReportPage />
  },
  {
    path: '/templates',
    element: <MyTemplatePage />
  },
  {
    path: '/profile',
    element: <ProfilePage />
  },
  {
    path: '/faq',
    element: <FaqPage />
  },
  {
    path: '/report/:id',
    element: <PrivateRoute><CreateReportPage /></PrivateRoute>
  },
  {
    path: '/template/:id',
    element: <PrivateRoute><CreateReportPage /></PrivateRoute>
  }
  
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
     <AuthProvider>
      <RouterProvider router={routes}/>
     </AuthProvider>
  </React.StrictMode>,
)
