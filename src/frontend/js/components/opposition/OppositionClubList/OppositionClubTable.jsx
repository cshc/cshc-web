import React from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import Urls from 'util/urls';
import commonStyles from 'components/common/style.scss';
import styles from './OppositionClubTable.scss';

// eslint-disable-next-line no-nested-ternary
const avg = row => `${row.value === 0 ? '' : (row.value < 0 ? '+' : '-')}${row.value.toFixed(1)}`;

const OppositionClubList = ({ data }) => (
  <div className={commonStyles.reactTable}>
    <ReactTable
      className={classNames(styles.clubTable, '-highlight')}
      showPagination={false}
      data={data.results || []}
      pageSize={data.results ? data.results.length : 0}
      columns={[
        {
          Header: 'Club',
          id: 'name',
          accessor: c => c,
          headerClassName: classNames('text-left'),
          Cell: row => (
            <a href={Urls.opposition_club_detail(row.value.club.slug)} title="Club Details">
              {row.value.club.name}
            </a>
          ),
          sortMethod: (a, b) => a.club.name.trim().localeCompare(b.club.name.trim()),
        },
        {
          Header: <abbr title="Played">P</abbr>,
          id: 'played',
          className: 'text-center',
          width: 50,
          accessor: c => c.totalPlayed,
        },
        {
          Header: <abbr title="Won">W</abbr>,
          id: 'won',
          className: 'text-center',
          width: 50,
          accessor: c => c.totalWon,
        },
        {
          Header: <abbr title="Drawn">D</abbr>,
          id: 'drawn',
          className: 'text-center',
          width: 50,
          accessor: c => c.totalDrawn,
        },
        {
          Header: <abbr title="Lost">L</abbr>,
          id: 'lost',
          className: 'text-center',
          width: 50,
          accessor: c => c.totalLost,
        },
        {
          Header: <abbr title="Average Goals per Game">Avg Goals</abbr>,
          columns: [
            {
              Header: <abbr title="Average Goals For">GF</abbr>,
              id: 'avgGf',
              className: 'text-center',
              width: 70,
              accessor: c => c.avgGf,
              Cell: avg,
            },
            {
              Header: <abbr title="Average Goals Against">GA</abbr>,
              id: 'avgGa',
              className: 'text-center',
              width: 70,
              accessor: c => c.avgGa,
              Cell: avg,
            },
            {
              Header: <abbr title="Average Goal Difference">GD</abbr>,
              id: 'avgGd',
              className: 'text-center',
              width: 70,
              accessor: c => c.avgGd,
              Cell: avg,
            },
          ],
        },
        {
          Header: <abbr title="Average Points per game">Avg Points</abbr>,
          id: 'avgPoints',
          className: 'text-center',
          width: 90,
          accessor: c => c.avgPoints,
          Cell: avg,
        },
      ]}
    />
  </div>
);

OppositionClubList.propTypes = {
  data: PropTypes.shape(),
};

OppositionClubList.defaultProps = {
  data: undefined,
};

export default OppositionClubList;

// {
//   Header: 'Address',
//   id: 'address',
//   accessor: venue => venue,
//   headerClassName: 'text-left',
//   Cell: row => Venue.full_address(row.value),
//   sortMethod: (a, b) => {
//     const addressA = Venue.full_address(a);
//     const addressB = Venue.full_address(b);
//     return addressA.trim().localeCompare(addressB.trim());
//   },
// },
// {
//   Header: () => <abbr title="Distance in miles from Cambridge">Distance</abbr>,
//   id: 'distance',
//   accessor: 'distance',
//   className: 'text-center',
//   width: 70,
//   headerClassName: 'text-center',
// },
