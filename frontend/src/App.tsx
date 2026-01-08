
import Box from '@mui/material/Box';
import './App.css';
import AppHeader from './components/app-header/AppHeader';
import PullRequestInput from './components/pull-request-input/PullRequestInput';
import { Container } from '@mui/material';

function App() {

  return (
    <>
      <Box sx={{flexGrow: 1}}>
        <AppHeader />
      </Box>
      <Container maxWidth="md">
      <PullRequestInput/>
      </Container>
    </>
  )
}

export default App
