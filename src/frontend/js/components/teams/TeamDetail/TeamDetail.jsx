import React from 'react';
import PropTypes from 'prop-types';
import Match from 'models/match';
import { MatchItem } from 'util/constants';
import MatchData from 'components/matches/MatchData';
import LeagueTable from 'components/competitions/LeagueTable';
import Accordion from 'components/common/Accordion';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import SquadRosterWrapper from './SquadRosterWrapper';

/**
 * Wrapper component for various components displayed for a particular club team (in a particular season).
 * 
 * Includes:
 * - Results/Fixtures
 * - League Table
 * - Squad Roster
 */
const TeamDetail = ({ data, division, teamId, teamGenderlessName, seasonId }) => (
  <Accordion multiselectable accordionId="team-details">
    <AccordionCard
      cardId="results_fixtures"
      accordionId="team-details"
      title="Results &amp; Fixtures"
    >
      {data.results.length > 0 ? (
        <MatchData matches={data.results} exclude={[MatchItem.ourTeam]} fillBlankSaturdays />
      ) : (
        <p className="lead g-font-style-italic">No matches</p>
      )}
    </AccordionCard>
    {division.id && (
      <AccordionCard cardId="league-table" accordionId="team-details" title="League Table">
        <LeagueTable divisionId={division.id} seasonId={seasonId} teamName={teamGenderlessName} />
      </AccordionCard>
    )}
    <AccordionCard cardId="squad-roster" accordionId="team-details" title="Squad Roster">
      <SquadRosterWrapper teamId={teamId} seasonId={seasonId} />
    </AccordionCard>
  </Accordion>
);

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
