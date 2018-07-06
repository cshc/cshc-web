import React from 'react';
import PropTypes from 'prop-types';
import UrlSyncedReactTable from 'components/common/UrlSyncedReactTable';
import { NetworkStatus as NS } from 'apollo-client';
import MemberLink from 'components/members/MemberLink';
import commonStyles from 'components/common/style.scss';

class EosListDisplay extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: !this.props.endOfSeasonAwardWinners && this.props.networkStatus === NS.loading,
    };
    this.onSortedChange = this.onSortedChange.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      loading: nextProps.networkStatus === NS.loading,
    });
  }

  onSortedChange(newSorted) {
    const orderBy = newSorted.map(i => (i.desc ? '-' : '') + i.id).join(',');
    this.props.onChangeOrderBy(orderBy);
  }

  render() {
    const {
      endOfSeasonAwardWinners,
      page,
      pageSize,
      onChangePage,
      onChangeUrlQueryParams,
    } = this.props;
    const { loading } = this.state;
    return (
      <div className={commonStyles.reactTable}>
        <UrlSyncedReactTable
          className="-highlight"
          manual
          columns={[
            {
              Header: 'Season',
              id: 'season',
              accessor: 'season.slug',
              headerClassName: 'text-left',
              width: 90,
            },
            {
              Header: 'Award',
              id: 'award',
              accessor: 'award.name',
            },
            {
              Header: 'Awardee',
              id: 'member_first_name',
              Cell: ({ original }) =>
                (original.member ? (
                  <MemberLink member={original.member} useFullName />
                ) : (
                  original.awardee
                )),
            },
          ]}
          data={endOfSeasonAwardWinners ? endOfSeasonAwardWinners.results : []}
          loading={loading}
          page={page}
          pageSize={pageSize}
          onChangePage={onChangePage}
          onChangeUrlQueryParams={onChangeUrlQueryParams}
          onSortedChange={this.onSortedChange}
          multiSort={false}
          totalCount={endOfSeasonAwardWinners ? endOfSeasonAwardWinners.totalCount : 0}
        />
        {endOfSeasonAwardWinners && (
          <div className="g-py-20">{endOfSeasonAwardWinners.totalCount} award winners</div>
        )}
      </div>
    );
  }
}

EosListDisplay.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  endOfSeasonAwardWinners: PropTypes.shape(),
  pageSize: PropTypes.number.isRequired,
  page: PropTypes.number.isRequired,
  onChangePage: PropTypes.func.isRequired,
  onChangeOrderBy: PropTypes.func.isRequired,
  onChangeUrlQueryParams: PropTypes.func.isRequired,
};

EosListDisplay.defaultProps = {
  error: undefined,
  endOfSeasonAwardWinners: undefined,
};

export default EosListDisplay;
