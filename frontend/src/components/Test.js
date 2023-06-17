import { useState, useEffect } from "react";
import axios from "axios";
import "./Test.css";
import { GrUpdate } from "react-icons/gr";
import { MdDelete } from "react-icons/md";
const Test = () => {
  const [tests, setTests] = useState([]);

  const getData = async () => {
    const res = await axios.get("http://localhost:5000/getAllTests");
    //console.log(res.data.tests);
    setTests(res.data.tests);
  };

  const handleUpdate = async (id) => {
    const selectElement = document.getElementById(id);
    const output = selectElement.value;
    console.log(id);
    if (output !== "Select") {
      const res = await axios.post(`http://localhost:5000/updateTest/${id}`, {
        testStatus: output,
      });
      alert("test updated successfully");
      getData();
    }
  };

  const handleDelete = async (id) => {
    const res = await axios.get(`http://localhost:5000/deleteTest/${id}`);
    getData();
  };
  useEffect(() => {
    getData();
  }, []);

  console.log(tests);
  return (
    <div className="containter">
      <h1 className="text-center m-2">Test Cases</h1>
      <div className="d-flex jusify-content-center m-5">
        <table className="border w-100 m-3">
          <thead>
            <tr>
              <th>Test Case Name</th>
              <th>Estimate Time ( in minutes )</th>
              <th>Module</th>
              <th>Priority</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody className="table-no-border">
            {tests.map((test) => {
              return (
                <tr className="m-2">
                  <td className="m-3">
                    <div className="d-flex flex-column">
                      <span>{test.testName}</span>
                      <span>{test.createdAt}</span>
                    </div>
                  </td>
                  <td className="m-3">{test.testTime} Minutes</td>
                  <td className="m-3">{test.testModule}</td>
                  <td className="m-3">{test.testPriority}</td>
                  <td className="m-2">
                    <div className="d-flex flex-row justify-content-center ">
                      <select className="rounded m-2" id={test.testId}>
                        <option selected>Select</option>
                        <option value="PASS">PASS</option>
                        <option value="FAIL">FAIL</option>
                      </select>

                      <div className="d-flex flex-row justify-content-center">
                        <GrUpdate
                          size="15"
                          className="d-flex m-2 justify-content-start"
                          onClick={() => handleUpdate(test.testId)}
                        />
                        <MdDelete
                          size="20"
                          className="d-flex m-2 justify-content-end"
                          onClick={() => handleDelete(test.testId)}
                        />
                      </div>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Test;
