import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import SquadRosterCard from './SquadRosterCard';

const SquadRoster = ({ networkStatus, error, squadStats }) => {
  if (networkStatus === NS.loading) return <Loading message="Fetching squad roster..." />;
  if (error) return <ErrorDisplay errorMessage="Failed to load squad roster" />;
  return (
    <div className="row">
      {squadStats.squad.map(memberStats => (
        <SquadRosterCard
          key={memberStats.member.modelId}
          memberStats={memberStats}
          teamTotals={squadStats.totals}
        />
      ))}
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
};

SquadRoster.defaultProps = {
  error: undefined,
  squadStats: undefined,
};

export default SquadRoster;
