import './App.css'
import axios from 'axios'
import LeducPokerComponent from './LeducPokerComponent'

function App() {

  async function getState() {
    const response = await axios.post('http://localhost:5000/state', {id: 0})
    console.log(response)
  }

  return (
    <>
      <div>
        <LeducPokerComponent />
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
