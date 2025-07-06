import './App.css';
import { Routes, Route } from "react-router-dom";
import Header from './components/Header/Header';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/login" element={<Login />} />
        {/* Add your other pages here */}
        <Route path="/register" element={<Register/>} />
      </Routes>
    </div>
  );
}

export default App;
