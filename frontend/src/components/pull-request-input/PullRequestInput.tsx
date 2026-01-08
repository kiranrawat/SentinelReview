import { TextField, Button, Grid, CircularProgress, Box, Snackbar } from '@mui/material';
import axios from 'axios';
import React from 'react';

function PullRequestInput() {
  const [prUrl, setPRUrl] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const prReviewerApi = import.meta.env.VITE_API_URL + '/review-pr'
  const handleButtonClick = async () => {
    try {
        setLoading(true);
        const response = await axios.post(prReviewerApi, {pr_url: prUrl });
        console.log(response.data);
    } catch(e) {
        console.error(e);
        setError('We are facing some issues. Try again later.');
    } finally {
        setLoading(false);
    }
    
  }
  const handleClose = () => {
    setError('');
  }
  return (
    <>
    <Grid container spacing={2} sx={{mt: 2}}>
        <Grid size={{xs:6, md:8}}>
            <TextField 
                onChange={(e) => setPRUrl(e.target.value)} 
                fullWidth 
                id="outlined-basic" 
                label="Enter Github Url" 
                variant="outlined" />
        </Grid>
        
        <Grid alignItems={'center'} >
            <Button onClick={handleButtonClick} variant="outlined" sx={{width:'100%', height: '100%'}}>Get Review</Button>
        </Grid>
        <Grid alignItems={'center'} size={12} >
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <CircularProgress sx={{display: loading?'block':'none'}} />
            </Box>
        </Grid>
    </Grid>
    <Snackbar
        open={error!=''}
        onClose={handleClose}
        message={error}
        autoHideDuration={1200}
    />
    </>
  )
}

export default PullRequestInput