import { CssBaseline } from '@mui/material';
import './App.css';
import PrimarySearchAppBar from './components/Titlebar';

function App() {
  return (
    <div>
    <CssBaseline />
    <PrimarySearchAppBar searchEnabled={false} />
    <div>
      <p>
        Here is my content.<br />
        Here is more of it.
      </p>
    </div>
    </div>
  );
}

export default App;
