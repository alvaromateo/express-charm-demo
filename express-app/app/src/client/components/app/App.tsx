import { createPortal } from 'react-dom'
import './App.css'
import Head from '../head/Head'
import Body from '../body/Body'

function App() {
  return (
    <>
      {createPortal(
        <Head/>,
        document.head
      )}
      <Body/>
    </>
  )
}

export default App
