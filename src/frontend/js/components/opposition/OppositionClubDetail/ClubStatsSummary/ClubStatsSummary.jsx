import React from 'react';
import PropTypes from 'prop-types';
import ClubStatsSummaryRow from './ClubStatsSummaryRow';

const ClubStatsSummary = ({ data }) => {
  const totalsClass = 'g-font-weight-600 text-right';
  const haClass = 'priority3 text-right';
  return (
    <div className="table-responsive g-pt-15 g-px-15">
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
          {data.results
            .filter(stats => stats.team)
            .map(stats => <ClubStatsSummaryRow key={stats.team.slug} stats={stats} />)}
          {data.results
            .filter(stats => !stats.team)
            .map(stats => <ClubStatsSummaryRow key="All" stats={stats} isTotal />)}
        </tbody>
      </table>
    </div>
  );
};

ClubStatsSummary.propTypes = {
  data: PropTypes.shape(),
};

ClubStatsSummary.defaultProps = {
  data: undefined,
};

export default ClubStatsSummary;
