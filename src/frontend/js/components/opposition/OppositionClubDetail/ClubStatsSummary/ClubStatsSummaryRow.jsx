import React from 'react';
import PropTypes from 'prop-types';

const ClubStatsSummaryRow = ({ isTotal, stats }) => {
  const totalsClass = 'g-font-weight-600 text-right';
  const haClass = 'priority3 text-right';
  return (
    <tr className={isTotal ? 'table-secondary' : ''}>
      <td>{isTotal ? 'All' : stats.team.shortName}</td>

      <td className={totalsClass}>{stats.totalPlayed}</td>
      <td className={totalsClass}>{stats.totalWon}</td>
      <td className={totalsClass}>{stats.totalDrawn}</td>
      <td className={totalsClass}>{stats.totalLost}</td>
      <td className={totalsClass}>{stats.totalGf}</td>
      <td className={totalsClass}>{stats.totalGa}</td>

      <td className={haClass}>{stats.homePlayed}</td>
      <td className={haClass}>{stats.homeWon}</td>
      <td className={haClass}>{stats.homeDrawn}</td>
      <td className={haClass}>{stats.homeLost}</td>
      <td className={haClass}>{stats.homeGf}</td>
      <td className={haClass}>{stats.homeGa}</td>

      <td className={haClass}>{stats.awayPlayed}</td>
      <td className={haClass}>{stats.awayWon}</td>
      <td className={haClass}>{stats.awayDrawn}</td>
      <td className={haClass}>{stats.awayLost}</td>
      <td className={haClass}>{stats.awayGf}</td>
      <td className={haClass}>{stats.awayGa}</td>
    </tr>
  );
};

ClubStatsSummaryRow.propTypes = {
  isTotal: PropTypes.bool,
  stats: PropTypes.shape().isRequired,
};

ClubStatsSummaryRow.defaultProps = {
  isTotal: false,
};

export default ClubStatsSummaryRow;
