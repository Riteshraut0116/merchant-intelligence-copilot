import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { UploadData } from './pages/UploadData';
import { Chat } from './pages/Chat';
import { WeeklyReport } from './pages/WeeklyReport';
import { About } from './pages/About';

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<UploadData />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/report" element={<WeeklyReport />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
