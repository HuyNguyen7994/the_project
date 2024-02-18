import { useState } from 'react'
import './App.css'

import { LineChart, Line, CartesianGrid, XAxis, YAxis } from 'recharts';
const data = [
  { name: 'Page A', uv: 400, pv: 2400, amt: 2400 },
  { name: 'Page B', uv: 600, pv: 2200, amt: 2600 },
  { name: 'Page C', uv: 800, pv: 2000, amt: 2800 },
]

const FormComponent: React.FC = () => {
  const url = import.meta.env.VITE_BACKEND_URL;
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const submitForm = async () => {
    try {
      const dataToSend = { latitude, longitude };
      const response = await fetch(url + `/api/v1/etl/run/aqicn/${latitude}/${longitude}`, {
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify(dataToSend),
      });

      if (!response.ok) {
        throw new Error(`Expect OK response. Got ${response.status}`);
      }

      setResponseMessage('ETL Job submitted. Please wait a while then refresh the page for latest result.');
    } catch (error) {
      console.error('Error:', error);
      setResponseMessage('Error occurred while processing the request.');
    }
  };

  return (
    <div>
      <form>
        <label htmlFor="latitude">Latitude:</label>
        <input
          type="text"
          id="latitude"
          value={latitude}
          onChange={(e) => setLatitude(e.target.value)}
          required
        />
        <br />
        <label htmlFor="longitude">Longitude:</label>
        <input
          type="text"
          id="longitude"
          value={longitude}
          onChange={(e) => setLongitude(e.target.value)}
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
      <h1>Check Area Air Quality</h1>
      <div className="card">
        <FormComponent />
      </div>
    </>
  );
}

export default App;