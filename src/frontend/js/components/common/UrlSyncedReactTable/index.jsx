import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import { numPages } from 'util/cshc';
import { DefaultPageSizeOptions } from 'util/constants';

/**
 * A wrapper around ReactTable that ensures the pagination is 
 * reflected in the URL query params.
 */
class UrlSyncedReactTable extends React.Component {
  constructor(props) {
    super(props);
    this.onPageSizeChange = this.onPageSizeChange.bind(this);
  }

  onPageSizeChange(newSize) {
    // Reset the page to the first page when the page size changes
    this.props.onChangeUrlQueryParams({
      pageSize: newSize,
      page: 1,
    });
  }

  render() {
    const { manual, page, pageSize, totalCount, onChangePage, ...props } = this.props;
    return (
      <ReactTable
        showPageJump={false}
        manual={manual}
        page={page - 1}
        pages={manual ? numPages(totalCount, pageSize) : undefined}
        onPageChange={p => onChangePage(p + 1)}
        onPageSizeChange={this.onPageSizeChange}
        defaultPageSize={pageSize}
        pageSizeOptions={DefaultPageSizeOptions}
        {...props}
      />
    );
  }
}

UrlSyncedReactTable.propTypes = {
  manual: PropTypes.bool,
  totalCount: PropTypes.number,
  pageSize: PropTypes.number.isRequired,
  page: PropTypes.number.isRequired,
  onChangePage: PropTypes.func.isRequired,
  onChangeUrlQueryParams: PropTypes.func.isRequired,
};

UrlSyncedReactTable.defaultProps = {
  manual: false,
  totalCount: 0,
};

export default UrlSyncedReactTable;
