import React from 'react';
import PropTypes from 'prop-types';
import { MatchItem } from 'util/constants';
import { Subheading } from 'components/Unify';
import MatchData from 'components/matches/MatchData';
import Match from 'models/match';
import Accordion from 'components/common/Accordion';
import AccordionCard from 'components/common/Accordion/AccordionCard';

/**
 * Wrapper component for components relating to a particular venue.
 * 
 * Includes:
 * - Previous results at this venue (organised by our team)
 * - Upcoming fixtures at this venue (organised by our team)
 */
const VenueDetail = ({ data, venueName }) => {
  const matchStructure = Match.toResultsAndFixtures(data);

  return (
    <div>
      <Subheading text={`Past results at ${venueName}`} />
      {matchStructure.results.length > 0 ? (
        <Accordion accordionId="results">
          {matchStructure.results.map(m => (
            <AccordionCard
              key={m.team.id}
              cardId={m.team.id}
              accordionId="results"
              title={m.team.longName}
            >
              <MatchData
                matches={m.matches}
                exclude={[MatchItem.ourTeam, MatchItem.venue]}
                dateFormat="Do MMM YY"
              />
            </AccordionCard>
          ))}
        </Accordion>
      ) : (
        <p className="lead">No previous matches at this venue</p>
      )}
      <Subheading text={`Upcoming fixtures at ${venueName}`} />
      {matchStructure.fixtures.length > 0 ? (
        <Accordion accordionId="fixtures">
          {matchStructure.fixtures.map(m => (
            <AccordionCard
              key={m.team.id}
              cardId={m.team.id}
              accordionId="fixtures"
              title={m.team.longName}
            >
              <MatchData
                matches={m.matches}
                exclude={[
                  MatchItem.ourTeam,
                  MatchItem.venue,
                  MatchItem.result,
                  MatchItem.scorers,
                  MatchItem.awards,
                ]}
              />
            </AccordionCard>
          ))}
        </Accordion>
      ) : (
        <p className="lead">No upcoming fixtures at this venue</p>
      )}
    </div>
  );
};

VenueDetail.propTypes = {
  venueName: PropTypes.string.isRequired,
  data: PropTypes.shape(),
};

VenueDetail.defaultProps = {
  data: undefined,
};

export default VenueDetail;
