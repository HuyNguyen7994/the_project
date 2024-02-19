import { useState } from 'react'
import './App.css'
import GaugeChart from './GaugeChart';


const FormComponent: React.FC = () => {
  const url = import.meta.env.VITE_BACKEND_URL;
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [airQualityValues, setAirQualityValues] = useState([]);

  const handleLatitudeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Allow only numeric input for latitude
    const numericValue = e.target.value.replace(/[^0-9.-]/g, '');
    setLatitude(numericValue);
  };

  const handleLongitudeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Allow only numeric input for longitude
    const numericValue = e.target.value.replace(/[^0-9.-]/g, '');
    setLongitude(numericValue);
  };

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
    setAirQualityValues(responseData);
  }

  return (
    <div>
      <form>
        <label htmlFor="latitude">Latitude:</label>
        <input
          type="text"
          id="latitude"
          value={latitude}
          onChange={handleLatitudeChange}
          required
        />
        <br />
        <label htmlFor="longitude">Longitude:</label>
        <input
          type="text"
          id="longitude"
          value={longitude}
          onChange={handleLongitudeChange}
          required
        />
        <br />
        <button type="button" onClick={submitForm}>
          Submit Coordinate
        </button>
        <button type="button" onClick={refreshChart}>
          Refresh Chart
        </button>
      </form>
      <p>{responseMessage}</p>
      <div style={{ display: 'flex' , flexDirection: 'column', flex: 1}}>
        {airQualityValues.map((value, index) => (
          <GaugeChart key={index} label={value[0]} value={value[1]} />
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