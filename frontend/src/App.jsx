//import './App.css'
import axios from 'axios'
import LeducPokerComponent from './LeducPokerComponent'

function App() {

  async function getState() {
    const response = await axios.post('http://localhost:5000/state', {id: 0})
    console.log(response)
  }

  return (
    <div>
      <LeducPokerComponent />
    </div>
  )
}

export default App
