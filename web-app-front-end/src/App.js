import React, { useState } from "react"
import "./App.css"

function App() {
  const [antenna, setAntenna] = useState("")
  const [beam, setBeam] = useState("")
  const [latitude, setLat] = useState("")

  
  const handleAntChange = e => {
    setAntenna(e.target.value)
  }

  const handleBeamChange = e => {
    setBeam(e.target.value)
  }

  const handleLatChange = e => {
    setLat(e.target.value)
  }

  return (
    <div>
      <h1>Basic Input Form</h1>
      <form>
        <label>
          Antenna Measurement:{" "} 
          <input type="text" value={antenna} onChange={handleAntChange} />
        </label>
      </form>
      <h5>Antenna: {antenna}</h5>
      <label>
          Beam Measurement:{" "} 
          <input type="text" value={beam} onChange={handleBeamChange} />
        </label>
      <h5>Beam: {beam}</h5>
        <label>
          Latitute Measurement:{" "} 
          <input type="text" value={latitude} onChange={handleLatChange} />
      </label>
      <h5>Latitude: {latitude}</h5>
    </div>
  )
}

export default App
