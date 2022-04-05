import { CssBaseline } from '@mui/material';
import './App.css';
import PrimarySearchAppBar from './components/Titlebar';
import ItemCard from './components/ItemCard';

function App() {
  return (
    <div>
    <CssBaseline />
    <PrimarySearchAppBar searchEnabled={false} />
    <div>
      <ItemCard title="My Title" description="This is a longer description\nmaybe with two lines??" />
    </div>
    </div>
  );
}

export default App;
