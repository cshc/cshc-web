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
  venue,
  players,
  mom,
  lom,
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
    venueId: venue,
    appearances_MemberId_In: players,
    date,
    reportAuthorId: reportAuthor,
    mom,
    lom,
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
  venue: PropTypes.string,
  players: PropTypes.string,
  mom: PropTypes.string,
  lom: PropTypes.string,
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
  venue: undefined,
  players: undefined,
  mom: undefined,
  lom: undefined,
  reportAuthor: undefined,
  date: undefined,
};

export default MatchListWrapper;
