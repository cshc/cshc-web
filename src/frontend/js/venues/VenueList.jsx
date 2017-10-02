import React from 'react';
import render from '../ReactRenderer';
import style from './VenueList.scss';

const VenueList = () => <h1 className={style.list}>All Venues</h1>;

render(VenueList);

/* eslint-disable global-require */
// Hot Module Replacement API
// if (module.hot) {
//   module.hot.accept('./Temp', () => {
//     const NextApp = require('./Temp').default;
//     render(NextApp);
//   });
// }
/* eslint-enable global-require */
