import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import "./index.scss"
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import { HelmetProvider } from 'react-helmet-async';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './utils/PrivateRoute';
import Header from './components/Header';
import Footer from './components/Footer';
import ContactPage from './pages/ContactPage';
import PrivacyPage from './pages/PrivacyPage';
import TosPage from './pages/TosPage';
import { ToastContainer } from 'react-toastify';
import HomePage from './pages/HomePage';

function App() {
  return (
    <div className="App">
      <Router>
        <HelmetProvider>
          <AuthProvider>
            <Header/>
            <ToastContainer />
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/main" element={<PrivateRoute element={MainPage} />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/contact" element={<ContactPage />} />
                <Route path="/privacy" element={<PrivacyPage />} />
                <Route path="/tos" element={<TosPage />} />
              </Routes>
              <Footer/>
          </AuthProvider>
        </HelmetProvider>
      </Router>
    </div >
  );
}

export default App;
