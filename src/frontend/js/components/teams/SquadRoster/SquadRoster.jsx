import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import { ViewType } from 'util/constants';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import SquadRosterCard from '../SquadRosterCard';
import SquadRosterTable from '../SquadRosterTable';

/**
 * Represents a list of club members (typically this is filtered by season and team). 
 * 
 * The list of club members can be represented in a table or 'cards' - with a view switcher
 * to switch between these views.
 */
const SquadRoster = ({ networkStatus, error, squadStats, viewType }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load squad roster" />;
  if (!squadStats && networkStatus === NS.loading) {
    return <Loading message="Fetching squad roster..." />;
  }
  return (
    <div>
      {viewType === ViewType.Cards ? (
        <div className="row">
          {squadStats.squad.map(memberStats => (
            <SquadRosterCard
              key={memberStats.member.modelId}
              memberStats={memberStats}
              teamTotals={squadStats.totals}
            />
          ))}
        </div>
      ) : (
        <SquadRosterTable squadStats={squadStats} />
      )}
    </div>
  );
};

SquadRoster.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  squadStats: PropTypes.shape({
    totals: PropTypes.shape(),
    squad: PropTypes.arrayOf(PropTypes.shape()),
  }),
  viewType: PropTypes.string.isRequired,
};

SquadRoster.defaultProps = {
  error: undefined,
  squadStats: undefined,
};

export default SquadRoster;
