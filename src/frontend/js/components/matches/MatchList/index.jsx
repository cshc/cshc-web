import React from 'react';
import PropTypes from 'prop-types';
import FilterableList from 'components/common/FilterableList';
import MatchFilterSet from './MatchFilterSet';
import MatchListWrapper from './MatchListWrapper';

const MatchList = props => (
  <FilterableList filterSet={<MatchFilterSet {...props} />} listWrapper={<MatchListWrapper />} />
);

MatchList.propTypes = {
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
  opposition_clubs: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  venues: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
  members: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number,
      name: PropTypes.string,
    }),
  ).isRequired,
};

MatchList.defaultProps = {};

export default MatchList;
