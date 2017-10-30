import React from 'react';
import PropTypes from 'prop-types';
import VenueFilterSet from '../VenueFilterSet';
import VenueListWrapper from '../VenueListWrapper';

const VenueList = props => (
  <div className="row">
    <div className="col-12 col-lg-4">
      <VenueFilterSet {...props} />
    </div>
    <div className="col-12 col-lg-8">
      <VenueListWrapper />
    </div>
  </div>
);

VenueList.propTypes = {
  currentSeason: PropTypes.string.isRequired,
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
  divisions: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
};

VenueList.defaultProps = {};

export default VenueList;
