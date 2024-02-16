import { useState } from 'react'
import './App.css'

import { LineChart, Line, CartesianGrid, XAxis, YAxis } from 'recharts';
const data = [
  { name: 'Page A', uv: 400, pv: 2400, amt: 2400 },
  { name: 'Page B', uv: 600, pv: 2200, amt: 2600 },
  { name: 'Page C', uv: 800, pv: 2000, amt: 2800 },
]

const FormComponent: React.FC = () => {
  const url = import.meta.env.VITE_BACKEND_URL
  const [inputData, setInputData] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const submitForm = async () => {
    try {
      const dataToSend = { "content": inputData };
      console.log(dataToSend);
      console.log(JSON.stringify(dataToSend));
      const response = await fetch(url + "message/Tester", {
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
        method: 'POST',
        body: JSON.stringify(dataToSend)
      });
      console.log(response);
      if (!response.ok) {
        throw new Error(`Expect 200. Got ${response.status}`)
      }
      const data = await response.json();
      console.log(data);
      setResponseMessage('We sent your message to the organizer: ' + JSON.stringify(data.content));
    } catch (error) {
      console.error('Error:', error);
      setResponseMessage('Error occurred while processing the request.');
    }
  };

  return (
    <div>
      <form>
        <label htmlFor="inputData">Your Message to Organizer:</label>
        <br />
        <input
          type="text"
          id="inputData"
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          required
        />
        <br />
        <button type="button" onClick={submitForm}>
          Submit
        </button>
      </form>

      <p>{responseMessage}</p>
      <LineChart width={400} height={400} data={data}>
        <Line type="monotone" dataKey="uv" stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="name" />
        <YAxis />
      </LineChart>
    </div>
  );
};

function App() {
  return (
    <>
      <div>
      </div>
      <h1>Let's Practice Together</h1>
      <div className="card">
        <FormComponent />
      </div>
    </>
  )
}

export default App
