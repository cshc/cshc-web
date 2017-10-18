import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import Match from 'models/match';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import MatchList from 'components/matches/MatchList';
import LeagueTable from 'components/competitions/LeagueTable';
import Accordion from 'components/common/Accordion';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import SquadRoster from '../SquadRoster';

const TeamDetail = ({ networkStatus, error, matches, division, teamId, seasonId }) => {
  if (networkStatus === NS.loading) return <Loading message="Loading team details..." />;
  if (error) return <ErrorDisplay errorMessage="Failed to load team details" />;
  const results = [];
  const fixtures = [];
  matches.edges.forEach((match) => {
    if (Match.isPast(match.node)) results.push(match.node);
    else fixtures.push(match.node);
  });
  return (
    <Accordion accordionId="team-details">
      <AccordionCard cardId="results" accordionId="team-details" title="Results">
        <MatchList matches={results} />
      </AccordionCard>
      <AccordionCard cardId="fixtures" accordionId="team-details" title="Fixtures">
        <MatchList
          matches={fixtures}
          exclude={['result', 'scorers', 'awards']}
          priorities={{ time: 1 }}
        />
      </AccordionCard>
      <AccordionCard cardId="league-table" accordionId="team-details" title="League Table">
        <LeagueTable divisionId={division.id} />
      </AccordionCard>
      <AccordionCard cardId="squad-roster" accordionId="team-details" title="Squad Roster">
        <SquadRoster teamId={teamId} seasonId={seasonId} />
      </AccordionCard>
    </Accordion>
  );
};

TeamDetail.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  matches: PropTypes.shape(),
  teamId: PropTypes.number.isRequired,
  seasonId: PropTypes.number.isRequired,
  division: PropTypes.shape({
    id: PropTypes.string,
    name: PropTypes.string,
    fixturesUrl: PropTypes.string,
    leagueTableUrl: PropTypes.string,
  }).isRequired,
};

TeamDetail.defaultProps = {
  error: undefined,
  matches: undefined,
};

export default TeamDetail;
