import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import commonStyles from 'components/common/style.scss';
import MemberAvatar from 'components/members/MemberAvatar';
import Member from 'models/member';
import { PositionValue } from 'util/constants';
import Urls from 'util/urls';
import styles from './style.scss';

/**
 * Tabular representation of a Squad Roster. Each member is a row on the table.
 */
const SquadRosterTable = ({ squadStats: { squad } }) => (
  <div>
    <div className={commonStyles.reactTable}>
      <ReactTable
        className="-highlight"
        showPageJump={false}
        columns={[
          {
            Header: '',
            id: 'profilePic',
            accessor: 'member',
            sortable: false,
            width: 70,
            className:
              'g-hidden-md-down text-center align-self-center d-flex align-items-center justify-content-center',
            headerClassName: 'g-hidden-md-down',
            Cell: row => <MemberAvatar member={row.value} className="g-width-50 g-py-5" />,
          },
          {
            Header: 'Name',
            id: 'name',
            accessor: memberStats => memberStats,
            className: `${styles.name} align-self-center`,
            headerClassName: `${styles.name} text-left`,
            Cell: row => (
              <a href={Urls.member_detail(row.value.member.id)} title="View Profile">
                {Member.fullName(row.value.member)}
                {row.value.isCaptain && <span> (C)</span>}
                {row.value.isViceCaptain && <span> (VC)</span>}
              </a>
            ),
            sortMethod: (a, b) => {
              const fullNameA = Member.fullName(a.member).trim();
              const fullNameB = Member.fullName(b.member).trim();
              if (fullNameA === fullNameB) return 0;
              return fullNameA < fullNameB ? -1 : 1;
            },
          },
          {
            Header: 'Shirt #',
            id: 'shirt',
            width: 70,
            accessor: 'member.shirtNumber',
            className: 'g-hidden-sm-down text-center align-self-center',
            headerClassName: 'g-hidden-sm-down',
            sortMethod: (a, b) => {
              if (a === b) return 0;
              else if (!a) return 1;
              else if (!b) return -1;
              else if (a === 'GK') return -1;
              else if (b === 'GK') return 1;
              return parseInt(a, 10) < parseInt(b, 10) ? -1 : 1;
            },
          },
          {
            Header: 'Position',
            id: 'position',
            width: 200,
            accessor: 'member.prefPosition',
            className: 'g-hidden-sm-down text-center align-self-center',
            headerClassName: 'g-hidden-sm-down',
            sortMethod: (a, b) => {
              if (a === b) return 0;
              else if (!a) return 1;
              else if (!b) return -1;
              return PositionValue[a] < PositionValue[b] ? -1 : 1;
            },
          },
          {
            Header: 'Played',
            id: 'played',
            width: 60,
            accessor: 'played',
            className: 'text-center align-self-center',
          },
          {
            Header: 'Goals',
            id: 'goals',
            width: 60,
            accessor: 'goals',
            className: 'text-center align-self-center',
            Cell: row => (row.value > 0 ? row.value : ''),
          },
          {
            Header: () => (
              <span>
                <i className="fas fa-star g-mr-5" />
                <abbr title="Man of the Match">MOM</abbr>
              </span>
            ),
            id: 'mom',
            width: 70,
            accessor: 'mom',
            className: 'g-hidden-sm-down text-center align-self-center',
            headerClassName: 'g-hidden-sm-down',
            Cell: row => (row.value > 0 ? row.value : ''),
          },
          {
            Header: () => (
              <span>
                <i className="fas fa-lemon g-mr-5" />
                <abbr title="Lemon of the Match">LOM</abbr>
              </span>
            ),
            id: 'lom',
            width: 70,
            accessor: 'lom',
            className: 'g-hidden-sm-down text-center align-self-center',
            headerClassName: 'g-hidden-sm-down',
            Cell: row => (row.value > 0 ? row.value : ''),
          },
        ]}
        defaultPageSize={50}
        minRows={0}
        data={squad}
      />
    </div>
  </div>
);

SquadRosterTable.propTypes = {
  squadStats: PropTypes.shape({
    totals: PropTypes.shape(),
    squad: PropTypes.arrayOf(PropTypes.shape()),
  }),
};

SquadRosterTable.defaultProps = {
  squadStats: undefined,
};

export default SquadRosterTable;
