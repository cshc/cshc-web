import React from 'react';
import PropTypes from 'prop-types';
import FilterableList from 'components/common/FilterableList';
import VenueFilterSet from './VenueFilterSet';
import VenueListWrapper from './VenueListWrapper';

const VenueList = props => (
  <FilterableList filterSet={<VenueFilterSet {...props} />} listWrapper={<VenueListWrapper />} />
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
