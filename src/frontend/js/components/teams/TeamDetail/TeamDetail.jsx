import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import Match from 'models/match';
import { MatchItem } from 'util/constants';
import { toGraphQLId } from 'util/cshc';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import MatchList from 'components/matches/MatchList';
import LeagueTable from 'components/competitions/LeagueTable';
import Accordion from 'components/common/Accordion';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import SquadRoster from '../SquadRoster';

/**
 * Wrapper component for various components displayed for a particular club team (in a particular season).
 * 
 * Includes:
 * - Results
 * - Fixtures
 * - League Table
 * - Squad Roster
 */
const TeamDetail = ({
  networkStatus,
  error,
  matches,
  division,
  teamId,
  teamGenderlessName,
  seasonId,
}) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load team details" />;
  if (!matches && networkStatus === NS.loading) {
    return <Loading message="Loading team details..." />;
  }
  const results = [];
  const fixtures = [];
  matches.edges.forEach((match) => {
    if (Match.isPast(match.node)) results.push(match.node);
    else fixtures.push(match.node);
  });
  return (
    <Accordion accordionId="team-details">
      {results.length > 0 ? (
        <AccordionCard cardId="results" accordionId="team-details" title="Results">
          <MatchList matches={results} />
        </AccordionCard>
      ) : null}
      {fixtures.length > 0 ? (
        <AccordionCard cardId="fixtures" accordionId="team-details" title="Fixtures">
          <MatchList
            matches={fixtures}
            exclude={[MatchItem.result, MatchItem.scorers, MatchItem.awards]}
            priorities={{ [MatchItem.time]: 1 }}
          />
        </AccordionCard>
      ) : null}
      <AccordionCard cardId="league-table" accordionId="team-details" title="League Table">
        <LeagueTable
          divisionId={toGraphQLId('Division', division.id)}
          seasonId={toGraphQLId('Season', seasonId)}
          teamName={teamGenderlessName}
        />
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
  error: undefined,
  matches: undefined,
};

export default TeamDetail;
