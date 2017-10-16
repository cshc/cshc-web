import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import Match from 'models/match';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import MatchList from 'components/matches/MatchList';
import LeagueTable from 'components/competitions/LeagueTable';
import SquadRoster from '../SquadRoster';
import Accordion from 'components/common/Accordion';
import AccordionCard from 'components/common/Accordion/AccordionCard';

const TeamDetail = ({ networkStatus, error, matches, division, teamId, seasonId }) => {
  if (networkStatus === NS.loading) return <Loading message="Loading team details..." />;
  if (error) return <ErrorDisplay errorMessage="Failed to load team details" />;
  const results = [];
  const fixtures = [];
  matches.edges.forEach((match) => {
    if (Match.isPast(match.node)) results.push(match.node);
    else fixtures.push(match.node);
  });
  const goToUrl = (e, url) => {
    const win = window.open(url, '_blank');
    win.focus();
    e.stopPropagation();
    e.preventDefault();
    return false;
  };
  const fixturesLink = division.fixturesUrl ? (
    <a
      role="link"
      tabIndex="0"
      onClick={e => goToUrl(e, division.fixturesUrl)}
      title={`${division.name} reuslts/fixtures`}
    >
      <i className="fa fa-lg fa-external-link" />
    </a>
  ) : null;
  const leagueTableLink = division.leagueTableUrl ? (
    <a
      role="link"
      tabIndex="0"
      onClick={e => goToUrl(e, division.leagueTableUrl)}
      title={`${division.name} league table`}
    >
      <i className="fa fa-lg fa-external-link" />
    </a>
  ) : null;
  return (
    <Accordion accordionId="team-details">
      <AccordionCard
        cardId="results"
        accordionId="team-details"
        title="Results"
        rightIcon={fixturesLink}
      >
        <MatchList matches={results} />
      </AccordionCard>
      <AccordionCard
        cardId="fixtures"
        accordionId="team-details"
        title="Fixtures"
        rightIcon={fixturesLink}
      >
        <MatchList matches={fixtures} exclude={['result', 'scorers', 'awards']} />
      </AccordionCard>
      <AccordionCard
        cardId="league-table"
        accordionId="team-details"
        title="League Table"
        rightIcon={leagueTableLink}
      >
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
