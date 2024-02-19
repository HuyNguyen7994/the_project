import { useState } from 'react'
import './App.css'
import GaugeChart from './GaugeChart';

interface AirQualityRow {
  city_name: string;
  pm25_value: number
}

const FormComponent: React.FC = () => {
  const url = import.meta.env.VITE_BACKEND_URL;
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [airQualityValues, setAirQualityValues] = useState<AirQualityRow[]>([]);

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

  const refreshChart = async () => {
    const url = import.meta.env.VITE_BACKEND_URL;
    const numOfDataPoints = 100
    const response = await fetch(url + `/api/v1/aqicn/recent/${numOfDataPoints}`, {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      method: 'GET',
    });
    const responseData = await response.json();
    setAirQualityValues([responseData.airQualityValue]);
  }

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
      <div style={{ display: 'flex' }}>
        {airQualityValues.map((value, index) => (
          <GaugeChart key={index} label={value.city_name} value={value.pm25_value} />
        ))}
      </div>
    </div >
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