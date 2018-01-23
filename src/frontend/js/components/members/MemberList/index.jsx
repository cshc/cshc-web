import React from 'react';
import PropTypes from 'prop-types';
import FilterableList from 'components/common/FilterableList';
import MemberFilterSet from './MemberFilterSet';
import MemberListWrapper from './MemberListWrapper';

const MemberList = ({ canViewMap, currentSeason, teams }) => {
  const filterSet = <MemberFilterSet teams={teams} />;
  const listWrapper = <MemberListWrapper currentSeason={currentSeason} canViewMap={canViewMap} />;
  return <FilterableList filterSet={filterSet} listWrapper={listWrapper} />;
};

MemberList.propTypes = {
  canViewMap: PropTypes.bool.isRequired,
  currentSeason: PropTypes.string.isRequired,
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
};

export default MemberList;
