import React from 'react';
import PropTypes from 'prop-types';
import { MatchItem } from 'util/constants';
import MatchData from 'components/matches/MatchData';
import LeagueTable from 'components/competitions/LeagueTable';
import Tabs from 'components/Unify/Tabs';
import SquadRosterWrapper from './SquadRosterWrapper';

/**
 * Wrapper component for various components displayed for a particular club team (in a particular season).
 * 
 * Includes:
 * - Results/Fixtures
 * - League Table
 * - Squad Roster
 */
const TeamDetail = ({ data, division, teamId, teamGenderlessName, seasonId }) => {
  const tabItems = [
    {
      tabId: 'matches',
      title: 'Results/Fixtures',
      active: true,
      content:
        data.results.length > 0 ? (
          <MatchData matches={data.results} exclude={[MatchItem.ourTeam]} fillBlankSaturdays />
        ) : (
          <p className="lead g-font-style-italic">No matches</p>
        ),
    },
  ];
  if (division.id) {
    tabItems.push({
      tabId: 'league-table',
      title: 'League Table',
      content: (
        <LeagueTable divisionId={division.id} seasonId={seasonId} teamName={teamGenderlessName} />
      ),
    });
  }
  tabItems.push({
    tabId: 'squad-roster',
    title: 'Squad Roster',
    content: <SquadRosterWrapper teamId={teamId} seasonId={seasonId} />,
  });
  return <Tabs items={tabItems} />;
};

TeamDetail.propTypes = {
  data: PropTypes.shape(),
  teamId: PropTypes.number.isRequired,
  teamGenderlessName: PropTypes.string.isRequired,
  seasonId: PropTypes.number.isRequired,
  division: PropTypes.shape({
    id: PropTypes.number,
    name: PropTypes.string,
    fixturesUrl: PropTypes.string,
    leagueTableUrl: PropTypes.string,
  }).isRequired,
};

TeamDetail.defaultProps = {
  data: undefined,
};

export default TeamDetail;
