import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import NavigationBar from './components/NavigationBar';
import Card from './components/Card';
import './App.css'

function App() {

  return (
    <>
      <p className='font-[cursive] text-2xl mt-10 -mb-5 sm:mt-2 sm:-mb-5'>Random NFT Arts' Collection (Showcase)</p>
      <br />
      <br />
      <NavigationBar />
      <Card />
      <br />
      <br />
    </>
  )
}

export default App
