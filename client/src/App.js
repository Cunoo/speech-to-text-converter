import './App.css';
import { Routes, Route } from "react-router-dom";
import Header from './components/Header/Header';
import Login from './pages/Login/Login';

function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/login" element={<Login />} />
        {/* Add your other pages here */}
      </Routes>
    </div>
  );
}

export default App;
