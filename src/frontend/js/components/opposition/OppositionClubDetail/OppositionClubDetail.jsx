import React from 'react';
import PropTypes from 'prop-types';
import { MatchItem } from 'util/constants';
import MatchList from 'components/matches/MatchList';
import Match from 'models/match';
import Accordion from 'components/common/Accordion';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import { Panel, Subheading } from 'components/Unify';
import ClubStatsSummary from './ClubStatsSummary';

/**
 * Wrapper component for components relating to a particular opposition club.
 * 
 * Includes:
 * - Previous results against this opposition club (organised by our team)
 * - Upcoming fixtures against this opposition club (organised by our team)
 */
const OppositionClubDetail = ({ data, clubName, matchFilters: { oppTeam_Club_Slug } }) => {
  const matchStructure = Match.toResultsAndFixtures(data);

  return (
    <div>
      <Panel
        outlineColor="primary"
        headerColor="primary"
        icon="fa fa-table"
        title="Playing Records"
      >
        <div className="card-block g-pa-15">
          <p className="card-text">
            This table summarises Cambridge South performances against {clubName}.
          </p>
        </div>

        <ClubStatsSummary clubSlug={oppTeam_Club_Slug} />
      </Panel>
      <Subheading text={`Past results against ${clubName}`} />
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
      <Subheading text={`Upcoming fixtures against ${clubName}`} />
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
  matchFilters: PropTypes.shape({
    oppTeam_Club_Slug: PropTypes.string,
  }).isRequired,
  data: PropTypes.shape(),
};

OppositionClubDetail.defaultProps = {
  data: undefined,
};

export default OppositionClubDetail;
