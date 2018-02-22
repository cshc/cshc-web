import React from 'react';
import PropTypes from 'prop-types';
import FilterableList from 'components/common/FilterableList';
import EoSFilterSet from './EosFilterSet';
import EosListDisplay from './EosListDisplay';

const EndOfSeasonAwardWinnerList = props => (
  <FilterableList filterSet={<EoSFilterSet {...props} />} listWrapper={<EosListDisplay />} />
);

EndOfSeasonAwardWinnerList.propTypes = {
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  awards: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
  awardees: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  ).isRequired,
};

EndOfSeasonAwardWinnerList.defaultProps = {};

export default EndOfSeasonAwardWinnerList;
