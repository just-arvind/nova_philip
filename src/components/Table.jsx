import React, { useEffect, useState } from "react";
import { Table } from "antd";
import axios from "axios";
import { Button } from 'antd';
import '../styles/Styles.css'

const TableData = () => {
  const [allData, setAllData] = useState([]);
  const [value, setValue] = useState(allData)

  useEffect(() => {
    axios.get('http://localhost:5080/get_data')
      .then(function (response) {
        setAllData(response.data?.phillip_nova);
        console.log(response.data?.phillip_nova)
      }
        , error => {
          console.log(error);
        });
    handleData2()
  }, []);

  const handleData = async () => {
    await axios.get('http://localhost:5080/get_data')
      .then(function (response) {
        setAllData(response.data?.phillip_nova);
        setValue(response.data?.phillip_nova)
        console.log(response.data?.phillip_nova)
      }
        , error => {
          console.log(error);
        });
  }

  const handleData2 = async () => {
    setInterval(() => {
      axios.get('http://localhost:5080/get_data')
        .then(function (response) {
          setAllData(response.data?.phillip_nova);
          setValue(response.data?.phillip_nova)
          console.log(response.data?.phillip_nova)
        }
          , error => {
            console.log(error);
          });
    }, 10000);

  }


  const columns = [
    {
      title: "Name",
      dataIndex: "id",
      key: "name",
    },
    {
      title: "BID",
      dataIndex: "bp",
      key: "bid",
    },
    {
      title: "ASK",
      dataIndex: "ap",
      key: "ask",
    },
    {
      title: "LAST",
      dataIndex: "p",
      key: "last",
    }
  ];

  return (
    <div>
      <div style={{ display: "flex", justifyContent: 'end' }}><Button onClick={handleData} type="primary" style={{ margin: 16 }}>Refresh</Button></div>
      <Table
        dataSource={allData}
        columns={columns}>
      </Table>
    </div>


  );
};

export default TableData;
