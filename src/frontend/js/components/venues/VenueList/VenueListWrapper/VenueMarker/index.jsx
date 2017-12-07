import React from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-google-maps';
import { getPosition } from 'util/cshc';
import VenueInfoWindow from './VenueInfoWindow';

const VenueMarker = ({ venue, isOpen, onClick }) => (
  <Marker position={getPosition(venue.position)} title={venue.name} onClick={onClick}>
    {isOpen && <VenueInfoWindow venue={venue} onCloseClick={onClick} />}
  </Marker>
);

// Note: isOpen and onClick should be set by the GoogleMap parent component.
VenueMarker.propTypes = {
  venue: PropTypes.shape().isRequired,
  isOpen: PropTypes.bool,
  onClick: PropTypes.func,
};

VenueMarker.defaultProps = {
  isOpen: false,
  onClick: () => {},
};

export default VenueMarker;
