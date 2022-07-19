import React,{useEffect, useState} from 'react'
import Data from "./overall_data.json";

import Table from "./components/Table";
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'
// import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Login from './components/login.component';
import SignUp from './components/signup.component';
import Order from './components/Order';



const App = () => {

  return (
    <div>
      <Table/>
      </div>
  )
}

export default App
