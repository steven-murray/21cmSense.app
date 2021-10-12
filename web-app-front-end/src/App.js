import React, { useState } from "react"
import "./App.css"

function App() {
  const [firstmeasurment, setFmeasure] = useState("")
  
  const handleChange = e => {
    setFmeasure(e.target.value)
  }

  return (
    <div>
      <h1>Basic Input Form</h1>
      <form>
        <label>
          Measurement:{" "} 
          <input type="text" value={firstmeasurment} onChange={handleChange} />
        </label>
      </form>
      <h5>Measurement: {firstmeasurment}</h5>
    </div>
  )
}

export default App
