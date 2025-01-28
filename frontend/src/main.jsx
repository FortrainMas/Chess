import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import WaitPage from './pages/waitPage/waitPage.jsx'

import { BrowserRouter, Routes, Route } from "react-router";
import { Provider } from 'react-redux';
import store from './redux/store.js'
import GamePage from './pages/gamePage/gamePage.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/wait/:id" element={<WaitPage />} />
          <Route path="game" element={<GamePage />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  </StrictMode>,
)
