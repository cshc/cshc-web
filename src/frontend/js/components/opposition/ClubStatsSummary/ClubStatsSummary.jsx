import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import ClubStatsSummaryRow from './ClubStatsSummaryRow';

const ClubStatsSummary = ({ networkStatus, error, oppositionClubStats }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load playing records" />;
  if (!oppositionClubStats || networkStatus === NS.loading) {
    return <Loading message="Fetching playing records..." />;
  }
  const totalsClass = 'g-font-weight-600 text-right';
  const haClass = 'priority3 text-right';
  return (
    <div className="table-responsive">
      <table className="table table-sm table-hover">
        <thead>
          <tr>
            <th rowSpan="2">Team</th>
            <th className="text-center g-font-weight-600" colSpan="6">
              All
            </th>
            <th className="text-center priority3" colSpan="6">
              Home
            </th>
            <th className="text-center priority3" colSpan="6">
              Away
            </th>
          </tr>
          <tr>
            <th className={totalsClass}>
              <abbr title="Played">P</abbr>
            </th>
            <th className={totalsClass}>
              <abbr title="Won">W</abbr>
            </th>
            <th className={totalsClass}>
              <abbr title="Drawn">D</abbr>
            </th>
            <th className={totalsClass}>
              <abbr title="Lost">L</abbr>
            </th>
            <th className={totalsClass}>
              <abbr title="Goals For">GF</abbr>
            </th>
            <th className={totalsClass}>
              <abbr title="Goals Against">GA</abbr>
            </th>

            <th className={haClass}>
              <abbr title="Played">P</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Won">W</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Drawn">D</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Lost">L</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Goals For">GF</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Goals Against">GA</abbr>
            </th>

            <th className={haClass}>
              <abbr title="Played">P</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Won">W</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Drawn">D</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Lost">L</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Goals For">GF</abbr>
            </th>
            <th className={haClass}>
              <abbr title="Goals Against">GA</abbr>
            </th>
          </tr>
        </thead>
        <tbody>
          {oppositionClubStats.edges
            .filter(stats => stats.node.team)
            .map(stats => <ClubStatsSummaryRow key={stats.node.team.slug} stats={stats.node} />)}
          {oppositionClubStats.edges
            .filter(stats => !stats.node.team)
            .map(stats => <ClubStatsSummaryRow key="All" stats={stats.node} isTotal />)}
        </tbody>
      </table>
    </div>
  );
};

ClubStatsSummary.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  oppositionClubStats: PropTypes.shape(),
};

ClubStatsSummary.defaultProps = {
  error: undefined,
  oppositionClubStats: undefined,
};

export default ClubStatsSummary;
