import React from 'react';
import PropTypes from 'prop-types';
import { InfoWindow } from 'react-google-maps';
import Urls from 'util/urls';

const VenueInfoWindow = ({ onCloseClick, venue }) => (
  <InfoWindow onCloseClick={() => onCloseClick(null)}>
    <div>
      <h6>{venue.name}</h6>
      <p>
        {venue.addr1 ? (
          <span>
            {venue.addr1}
            <br />
          </span>
        ) : null}
        {venue.addr2 ? (
          <span>
            {venue.addr2}
            <br />
          </span>
        ) : null}
        {venue.addr3 ? (
          <span>
            {venue.addr3}
            <br />
          </span>
        ) : null}
        {venue.addrCity ? (
          <span>
            {venue.addrCity}
            <br />
          </span>
        ) : null}
        {venue.addrPostcode ? (
          <span>
            {venue.addrPostcode}
            <br />
          </span>
        ) : null}
      </p>
      {venue.phone ? (
        <div className="g-mb-10">
          <i className="fas fa-phone g-mr-5" />
          {venue.phone}
          <br />
        </div>
      ) : null}
      {venue.url ? (
        <div>
          <i className="fas fa-globe g-mr-5" />
          <a href={venue.url}>{venue.url}</a>
          <br />
        </div>
      ) : null}
      <a href={Urls.venue_detail(venue.slug)} className="btn u-btn-primary" title="Venue Details">
        Details...
      </a>
    </div>
  </InfoWindow>
);

VenueInfoWindow.propTypes = {
  venue: PropTypes.shape({}).isRequired,
  onCloseClick: PropTypes.func.isRequired,
};

export default VenueInfoWindow;
