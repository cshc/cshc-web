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
 * - Results
 * - Fixtures
 * - League Table
 * - Squad Roster
 */
const TeamDetail = ({ data, division, teamId, teamGenderlessName, seasonId }) => {
  const results = [];
  const fixtures = [];
  data.results.forEach((match) => {
    if (Match.isPast(match)) results.push(match);
    else fixtures.push(match);
  });
  return (
    <Accordion multiselectable accordionId="team-details">
      <AccordionCard cardId="results" accordionId="team-details" title="Results">
        {results.length > 0 ? (
          <MatchData matches={results} fillBlankSaturdays />
        ) : (
          <p className="lead g-font-style-italic">No matches played</p>
        )}
      </AccordionCard>
      <AccordionCard cardId="fixtures" accordionId="team-details" title="Fixtures">
        {fixtures.length > 0 ? (
          <MatchData
            matches={fixtures}
            fillBlankSaturdays
            exclude={[MatchItem.result, MatchItem.scorers, MatchItem.awards]}
            priorities={{ [MatchItem.time]: 1 }}
          />
        ) : (
          <p className="lead g-font-style-italic">No upcoming fixtures</p>
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
