import { TextField, Button, Grid, CircularProgress, Box, Snackbar, Typography } from '@mui/material';
import axios, { AxiosError } from 'axios';
import React from 'react';

interface APIResponse {
  pr_url: URL;
  review: string;
}

function PullRequestReviewer() {
  const [prUrl, setPRUrl] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const [apiResponse, setApiResponse] = React.useState<APIResponse|null>(null);

  const prReviewerApi = import.meta.env.VITE_API_URL + '/review-pr'
  const handleButtonClick = async () => {
    try {
        setLoading(true);
        setApiResponse(null);
        const response = await axios.post(prReviewerApi, {pr_url: prUrl });
        const data: APIResponse = {
          pr_url: new URL(response.data.pr_url),
          review: response.data.review
        }
        setApiResponse(data);
        console.log(data);
    } catch(e) {
        if (e instanceof AxiosError && e.status==422){
          setError('Invalid Input! Please end a valid github pull request.');
        } else {
          console.error(e);
          setError('We are facing some issues. Try again later.');
        }
        
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

        <Grid alignItems={'center'} size={12} sx={{display: loading?'block':'none'}}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <CircularProgress sx={{m:4}} />
            <Box>Loading...</Box>
          </Box>
        </Grid>

        <Grid>
          <Box sx={{mb: 4}}>
            <Typography variant='h5' component='a' href={apiResponse?.pr_url.href} > 
              {apiResponse?.pr_url.pathname} 
            </Typography>
          </Box>
          <Box sx={{whiteSpace: 'pre-wrap'}}>{apiResponse && apiResponse.review}</Box>
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

export default PullRequestReviewer