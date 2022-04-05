import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
// import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

export default function ItemCard(props) {

  return (
    <Card>
      <CardActionArea>
        <CardContent sx={{ flexGrow: 1 }}>
          <Grid container spacing={1}>
            <Grid container item xs={0}>
                <div />
            </Grid>
            <Grid container item xs={12}>
              <Grid item xs={12}>
                  <Typography gutterBottom variant="h5" component="div">
                    {props.title}
                  </Typography>
              </Grid>
              <Grid item xs={12}>
                  <Typography variant="body2" color="text.secondary">
                    {props.description}
                  </Typography>
              </Grid>
            </Grid>
          </Grid>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}