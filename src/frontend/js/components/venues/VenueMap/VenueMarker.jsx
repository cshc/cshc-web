import React from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-google-maps';
import { getPosition } from 'util/cshc';
import VenueInfoWindow from './VenueInfoWindow';

const VenueMarker = ({ venue, isOpen, onToggleOpen }) => (
  <Marker
    position={getPosition(venue.position)}
    title={venue.name}
    onClick={() => onToggleOpen(venue)}
  >
    {isOpen && <VenueInfoWindow venue={venue} onCloseClick={onToggleOpen} />}
  </Marker>
);

VenueMarker.propTypes = {
  venue: PropTypes.shape().isRequired,
  isOpen: PropTypes.bool.isRequired,
  onToggleOpen: PropTypes.func.isRequired,
};

export default VenueMarker;
