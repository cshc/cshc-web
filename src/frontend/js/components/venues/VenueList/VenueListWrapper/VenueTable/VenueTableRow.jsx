import React from 'react';
import PropTypes from 'prop-types';
import Urls from 'util/urls';
import Venue from 'models/venue';

const VenueTableRow = ({ venue }) => (
  <tr>
    <td>
      <a href={Urls.venue_detail(venue.slug)} title="Venue Details">
        {venue.name}
      </a>
      {venue.isHome && <i className="g-ml-5 fas fa-home" title="Home venue" />}
    </td>
    <td>{Venue.full_address(venue)}</td>
    <td>{venue.distance}</td>
  </tr>
);

VenueTableRow.propTypes = {
  venue: PropTypes.shape({
    name: PropTypes.string,
  }).isRequired,
};

export default VenueTableRow;
