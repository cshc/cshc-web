import React from 'react';
import PropTypes from 'prop-types';
import format from 'date-fns/format';
import { NetworkStatus as NS } from 'apollo-client';
import Loading from 'components/common/Loading';
import ErrorDisplay from 'components/common/ErrorDisplay';
import MatchTime from 'components/matches/MatchTime';
import { Timeline2, TimelineBigItem } from 'components/Unify';
import Urls from 'util/urls';
import MatchAvailabilityForm from './MatchAvailabilityForm';
import { MemberPropType } from '../PropTypes';

/**
 * Renders a list of matches for which a member's availability has been requested. 
 * 
 * For each match, the user can edit/update their availability. 
 */
const MemberAvailability = ({
  networkStatus,
  error,
  member,
  availabilityType,
  matchAvailabilities,
}) => {
  if (error) {
    return <ErrorDisplay errorMessage="Could not fetch match availabilities." />;
  } else if (networkStatus === NS.loading) {
    return <Loading message="Fetching data..." />;
  } else if (matchAvailabilities.length === 0) {
    return <p className="lead text-center g-font-style-italic">No upcoming matches</p>;
  }
  return (
    <Timeline2>
      {matchAvailabilities.map(a => (
        <TimelineBigItem
          id={`ma-${a.match.id}`}
          highlighted={!!Urls.getParameterByName(`${a.match.id}`)}
          key={a.match.id}
          dateSmall={<MatchTime match={a.match} />}
          dateLarge={format(a.match.date, 'DD-MMM')}
        >
          <header className="g-brd-bottom g-brd-gray-light-v4 g-pb-10 g-mb-25">
            <h3>
              <a
                className="g-font-weight-600"
                href={Urls.match_detail(a.match.id)}
                title="Match details"
              >
                {a.match.ourTeam.shortName} vs {a.match.oppTeam.name}
              </a>
              <span className="float-right g-font-size-80x">
                {a.match.venue ? (
                  <a title={a.match.venue.name} href={Urls.venue_detail(a.match.venue.slug)}>
                    {a.match.isHome ? 'Home' : 'Away'}
                  </a>
                ) : (
                  <span>Venue TBD</span>
                )}
              </span>
            </h3>
          </header>
          <MatchAvailabilityForm
            member={member}
            availabilityType={availabilityType}
            availability={a}
          />
        </TimelineBigItem>
      ))}
    </Timeline2>
  );
};

MemberAvailability.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.oneOfType([PropTypes.bool, PropTypes.instanceOf(Error)]),
  member: MemberPropType.isRequired,
  availabilityType: PropTypes.string.isRequired,
  matchAvailabilities: PropTypes.arrayOf(PropTypes.shape()),
};

MemberAvailability.defaultProps = {
  error: false,
  matchAvailabilities: null,
};

export default MemberAvailability;
