import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import commonStyles from 'components/common/style.scss';
import Urls from 'util/urls';
import styles from './style.scss';

const MemberTable = ({ members }) => (
  <div className={commonStyles.reactTable}>
    <ReactTable
      className="-highlight"
      showPageJump={false}
      columns={[
        {
          Header: 'First Name',
          id: 'firstName',
          accessor: 'firstName',
          className: styles.name,
          headerClassName: `${styles.name} text-left`,
        },
        {
          Header: 'Last Name',
          id: 'lastName',
          accessor: 'lastName',
          className: styles.name,
          headerClassName: `${styles.name} text-left`,
        },
        {
          Header: <abbr title="Male/Female">M/F</abbr>,
          id: 'gender',
          accessor: 'gender',
          className: 'g-hidden-sm-down text-center',
          headerClassName: 'g-hidden-sm-down',
          Cell: row => row.value[0],
          width: 40,
        },
        {
          Header: 'Position',
          id: 'position',
          accessor: 'prefPosition',
          className: 'g-hidden-sm-down text-center',
          headerClassName: 'g-hidden-sm-down',
          Cell: row => (row.value !== 'Not known' ? row.value : null),
        },
        {
          Header: 'Shirt #',
          id: 'shirtNumber',
          accessor: 'shirtNumber',
          className: 'g-hidden-sm-down text-center',
          headerClassName: 'g-hidden-sm-down',
          width: 60,
        },
        {
          Header: <abbr title="Appearances">Apps</abbr>,
          id: 'appearances',
          accessor: 'numAppearances',
          className: 'text-center',
          width: 60,
        },
        {
          Header: 'Goals',
          id: 'goals',
          accessor: 'goals',
          className: 'text-center',
          width: 60,
        },
      ]}
      data={members || []}
      getTdProps={(state, rowInfo) => ({
        onClick: () => {
          window.location = Urls.member_detail(rowInfo.original.id);
        },
        className: 'g-cursor-pointer',
        title: 'View member details',
      })}
    />
    {members && <div className="g-py-20">{members.length} members</div>}
  </div>
);

MemberTable.propTypes = {
  members: PropTypes.arrayOf(PropTypes.shape()).isRequired,
};

export default MemberTable;
