import { createPortal } from 'react-dom'
import './App.css'
import Head from './Head'
import Body from './Body'

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
