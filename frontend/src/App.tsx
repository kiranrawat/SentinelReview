
import Box from '@mui/material/Box';
import './App.css';
import AppHeader from './components/app-header/AppHeader';
import PullRequestReviewer from './components/pull-request-reviewer/PullRequestReviewer';
import { Container } from '@mui/material';

function App() {

  return (
    <>
      <Box sx={{flexGrow: 1}}>
        <AppHeader />
      </Box>
      <Container maxWidth="md">
      <PullRequestReviewer/>
      </Container>
    </>
  )
}

export default App
