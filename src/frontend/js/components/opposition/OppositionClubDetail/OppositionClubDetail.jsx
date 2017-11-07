import React from 'react';
import PropTypes from 'prop-types';
import reduce from 'lodash/reduce';
import sortBy from 'lodash/sortBy';
import { NetworkStatus as NS } from 'apollo-client';
import { MatchItem } from 'util/constants';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import Subheading from 'components/common/Subheading';
import MatchList from 'components/matches/MatchList';
import Match from 'models/match';
import Accordion from 'components/common/Accordion';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import ClubStatsSummary from '../ClubStatsSummary';

/**
 * Wrapper component for components relating to a particular opposition club.
 * 
 * Includes:
 * - Previous results against this opposition club (organised by our team)
 * - Upcoming fixtures against this opposition club (organised by our team)
 */
const OppositionClubDetail = ({
  networkStatus,
  error,
  matches,
  clubName,
  matchFilters: { oppTeam_Club_Slug },
}) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load matches" />;
  if (!matches && networkStatus === NS.loading) return <Loading message="Loading matches..." />;

  const matchStructure = {
    results: [],
    fixtures: [],
  };
  // Sort by past results vs future fixtures and by team
  reduce(
    matches.edges,
    (acc, matchEdge) => {
      const list = Match.isPast(matchEdge.node) ? acc.results : acc.fixtures;
      let teamMatches = list.find(md => md.team.id === matchEdge.node.ourTeam.id);
      if (!teamMatches) {
        teamMatches = { team: matchEdge.node.ourTeam, matches: [] };
        list.push(teamMatches);
      }
      teamMatches.matches.push(matchEdge.node);
      return acc;
    },
    matchStructure,
  );
  // Sort by team position
  matchStructure.results = sortBy(matchStructure.results, ['team.position']);
  matchStructure.fixtures = sortBy(matchStructure.fixtures, ['team.position']);

  return (
    <div>
      <div className="card g-brd-primary rounded-0 g-mt-40">
        <h3 className="card-header g-bg-primary g-brd-transparent g-color-white g-font-size-16 rounded-0 mb-0">
          <i className="fa fa-table g-mr-5" />Playing Records
        </h3>

        <div className="card-block g-pa-15">
          <p className="card-text">
            This table summarises Cambridge South performances against {clubName}.
          </p>
        </div>

        <ClubStatsSummary clubSlug={oppTeam_Club_Slug} />
      </div>
      <Subheading>Past results against {clubName}</Subheading>
      {matchStructure.results.length > 0 ? (
        <Accordion accordionId="results">
          {matchStructure.results.map(m => (
            <AccordionCard
              key={m.team.id}
              cardId={m.team.id}
              accordionId="results"
              title={m.team.longName}
            >
              <MatchList
                matches={m.matches}
                exclude={[MatchItem.opposition]}
                dateFormat="Do MMM YY"
              />
            </AccordionCard>
          ))}
        </Accordion>
      ) : (
        <p className="lead">No previous matches against {clubName}</p>
      )}
      <Subheading>Upcoming fixtures against {clubName}</Subheading>
      {matchStructure.fixtures.length > 0 ? (
        <Accordion accordionId="fixtures">
          {matchStructure.fixtures.map(m => (
            <AccordionCard
              key={m.team.id}
              cardId={m.team.id}
              accordionId="fixtures"
              title={m.team.longName}
            >
              <MatchList
                matches={m.matches}
                exclude={[
                  MatchItem.opposition,
                  MatchItem.result,
                  MatchItem.scorers,
                  MatchItem.awards,
                ]}
                priorities={{ [MatchItem.time]: 1, [MatchItem.venue]: 1 }}
              />
            </AccordionCard>
          ))}
        </Accordion>
      ) : (
        <p className="lead">No upcoming fixtures against {clubName}</p>
      )}
    </div>
  );
};

OppositionClubDetail.propTypes = {
  clubName: PropTypes.string.isRequired,
  networkStatus: PropTypes.number.isRequired,
  matchFilters: PropTypes.shape({
    oppTeam_Club_Slug: PropTypes.string,
  }).isRequired,
  error: PropTypes.instanceOf(Error),
  matches: PropTypes.shape(),
};

OppositionClubDetail.defaultProps = {
  error: undefined,
  matches: undefined,
};

export default OppositionClubDetail;
