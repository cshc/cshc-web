import React from 'react';
import PropTypes from 'prop-types';
import MatchListDisplay from 'components/matches/MatchListDisplay';
import { DefaultPageSize } from 'util/constants';

const MatchListWrapper = ({
  page,
  pageSize,
  orderBy,
  gender,
  team,
  opposition,
  season,
  fixtureType,
  division,
  homeAway,
  venue,
  players,
  pom,
  lom,
  result,
  reportAuthor,
  date,
  ...props
}) => {
  const queryVariables = {
    page,
    pageSize,
    orderBy,
    ourTeam_Gender: gender,
    ourTeam_Slug: team,
    oppTeam_Club_Slug: opposition,
    season_Slug: season,
    fixtureType,
    homeAway,
    venueId: venue,
    appearances_MemberId_In: players,
    date,
    reportAuthorId: reportAuthor,
    pom,
    lom,
    result,
  };
  return <MatchListDisplay queryVariables={queryVariables} {...props} />;
};

MatchListWrapper.propTypes = {
  page: PropTypes.number,
  pageSize: PropTypes.number,
  orderBy: PropTypes.string,
  gender: PropTypes.string,
  team: PropTypes.string,
  opposition: PropTypes.string,
  season: PropTypes.string,
  fixtureType: PropTypes.string,
  division: PropTypes.string,
  homeAway: PropTypes.string,
  venue: PropTypes.string,
  players: PropTypes.string,
  pom: PropTypes.string,
  lom: PropTypes.string,
  result: PropTypes.string,
  reportAuthor: PropTypes.string,
  date: PropTypes.string,
};

MatchListWrapper.defaultProps = {
  pageSize: DefaultPageSize,
  page: 1,
  orderBy: undefined,
  gender: undefined,
  team: undefined,
  opposition: undefined,
  season: undefined,
  fixtureType: undefined,
  division: undefined,
  homeAway: undefined,
  venue: undefined,
  players: undefined,
  pom: undefined,
  lom: undefined,
  result: undefined,
  reportAuthor: undefined,
  date: undefined,
};

export default MatchListWrapper;
