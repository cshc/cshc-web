import React from 'react';
import PropTypes from 'prop-types';
import UrlSyncedReactTable from 'components/common/UrlSyncedReactTable';
import Urls from 'util/urls';
import Venue from 'models/venue';
import commonStyles from 'components/common/style.scss';

const VenueTable = ({ venues, page, pageSize, onChangePage, onChangeUrlQueryParams }) => (
  <div className={commonStyles.reactTable}>
    <UrlSyncedReactTable
      className="-highlight"
      data={venues || []}
      page={page}
      pageSize={pageSize}
      onChangePage={onChangePage}
      onChangeUrlQueryParams={onChangeUrlQueryParams}
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
  pageSize: PropTypes.number,
  page: PropTypes.number,
  onChangePage: PropTypes.func.isRequired,
  onChangeUrlQueryParams: PropTypes.func.isRequired,
};

VenueTable.defaultProps = {
  pageSize: 20,
  page: 1,
};

export default VenueTable;
