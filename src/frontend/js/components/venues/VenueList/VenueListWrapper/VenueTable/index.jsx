import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import Urls from 'util/urls';
import Venue from 'models/venue';
import commonStyles from 'components/common/style.scss';

const VenueTable = ({ venues }) => (
  <div className={commonStyles.reactTable}>
    <ReactTable
      className="-highlight"
      showPageJump={false}
      defaultPageSize={20}
      data={venues}
      columns={[
        {
          Header: 'Venue',
          id: 'name',
          accessor: venue => venue,
          headerClassName: 'text-left',
          Cell: row => (
            <a href={Urls.venue_detail(row.value.slug)} title="Venue Details">
              {row.value.name}
              {row.value.isHome && <i className="g-ml-5 fas fa-home" title="Home venue" />}
            </a>
          ),
          sortMethod: (a, b) => a.name.trim().localeCompare(b.name.trim()),
        },
        {
          Header: 'Address',
          id: 'address',
          accessor: venue => venue,
          headerClassName: 'text-left',
          Cell: row => Venue.full_address(row.value),
          sortMethod: (a, b) => {
            const addressA = Venue.full_address(a);
            const addressB = Venue.full_address(b);
            return addressA.trim().localeCompare(addressB.trim());
          },
        },
        {
          Header: () => <abbr title="Distance in miles from Cambridge">Distance</abbr>,
          id: 'distance',
          accessor: 'distance',
          className: 'text-center',
          width: 70,
          headerClassName: 'text-center',
        },
      ]}
    />
  </div>
);

VenueTable.propTypes = {
  venues: PropTypes.arrayOf(PropTypes.shape()).isRequired,
};

export default VenueTable;
