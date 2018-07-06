import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
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
      loading: !nextProps.endOfSeasonAwardWinners && nextProps.networkStatus === NS.loading,
    });
  }

  onSortedChange(newSorted) {
    const orderBy = newSorted.map(i => (i.desc ? '-' : '') + i.id).join(',');
    this.props.onChangeOrderBy(orderBy);
  }

  render() {
    const { endOfSeasonAwardWinners, page, pageSize, onChangePage, onChangePageSize } = this.props;
    const { loading } = this.state;
    return (
      <div className={commonStyles.reactTable}>
        <ReactTable
          className="-highlight"
          showPageJump={false}
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
          manual
          page={page - 1}
          onPageChange={p => onChangePage(p + 1)}
          onPageSizeChange={onChangePageSize}
          defaultPageSize={pageSize}
          onSortedChange={this.onSortedChange}
          pages={
            endOfSeasonAwardWinners ? Math.ceil(endOfSeasonAwardWinners.totalCount / pageSize) : 0
          }
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
  error: PropTypes.instanceOf(Error),
  endOfSeasonAwardWinners: PropTypes.shape(),
  pageSize: PropTypes.number.isRequired,
  page: PropTypes.number.isRequired,
  onChangePage: PropTypes.func.isRequired,
  onChangePageSize: PropTypes.func.isRequired,
  onChangeOrderBy: PropTypes.func.isRequired,
};

EosListDisplay.defaultProps = {
  error: undefined,
  endOfSeasonAwardWinners: undefined,
};

export default EosListDisplay;
