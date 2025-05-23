import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import "./index.scss"
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import { HelmetProvider } from 'react-helmet-async';
import { AuthProvider } from './context/AuthContext';
import { MainProvider } from './context/MainContext';
import PrivateRoute from './utils/PrivateRoute';
import Header from './components/Header';
import Footer from './components/Footer';
import PrivacyPage from './pages/PrivacyPage';
import TosPage from './pages/TosPage';
import { ToastContainer } from 'react-toastify';
import HomePage from './pages/HomePage';
import ExamplePage from './pages/ExamplePage';
import { useEffect, useContext } from 'react';
import ProfilPage from './pages/ProfilPage';
import IgLoginPage from './pages/IgLoginPage';
import UploadPage from './pages/UploadPage';


function App() {

  return (
    <div className="App">
      <Router>
        <HelmetProvider>
          <AuthProvider>
            <MainProvider>
              <Header />
              <ToastContainer
                position="bottom-right"
                autoClose={3000}
                hideProgressBar={false}
                closeOnClick={true}
                pauseOnHover={false}
                draggable={true}
                progress={undefined}
                theme="dark"
              />
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/main" element={<PrivateRoute element={MainPage} />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/profil" element={<PrivateRoute element={ProfilPage} />} />
                <Route path="/iglogin" element={<PrivateRoute element={IgLoginPage} />} />
                <Route path="/privacy" element={<PrivacyPage />} />
                <Route path="/tos" element={<TosPage />} />
                <Route path="/examples" element={<ExamplePage />}/>
                <Route path="/upload" element={<UploadPage />} />

              </Routes>
              <Footer />
            </MainProvider>
          </AuthProvider>
        </HelmetProvider>
      </Router>
    </div >
  );
}

export default App;
