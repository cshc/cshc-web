import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import { NetworkStatus as NS } from 'apollo-client';
import Match from 'models/match';
import OurTeam from 'components/matches/OurTeam';
import FixtureTypeIcon from 'components/matches/FixtureTypeIcon';
import OppositionTeam from 'components/matches/OppositionTeam';
import MatchVenue from 'components/matches/MatchVenue';
import MatchDate from 'components/matches/MatchDate';
import MatchLink from 'components/matches/MatchLink';
import commonStyles from 'components/common/style.scss';

class MatchListDisplay extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: !this.props.matches && this.props.networkStatus === NS.loading,
    };
    this.onSortedChange = this.onSortedChange.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ loading: !nextProps.matches && nextProps.networkStatus === NS.loading });
  }

  onSortedChange(newSorted) {
    const orderBy = newSorted.map(i => (i.desc ? '-' : '') + i.id).join(',');
    this.props.onChangeOrderBy(orderBy);
  }

  render() {
    const { matches, queryVariables: { pageSize }, onChangePage, onChangePageSize } = this.props;
    const { loading } = this.state;
    return (
      <div className={commonStyles.reactTable}>
        <ReactTable
          className="-highlight"
          showPageJump={false}
          columns={[
            {
              Header: '',
              id: 'fixtureType',
              accessor: 'fixtureType',
              width: 30,
              sortable: false,
              className: 'text-center align-self-center',
              Cell: row => <FixtureTypeIcon fixtureType={row.value} />,
            },
            {
              Header: 'Date',
              id: 'date',
              className: 'align-self-center',
              accessor: 'date',
              headerClassName: 'text-left',
              width: 90,
              Cell: row => <MatchDate date={row.value} format="Do MMM YY" />,
            },
            {
              Header: 'Team',
              id: 'ourTeam',
              accessor: 'ourTeam',
              className: 'align-self-center',
              headerClassName: 'text-left',
              width: 70,
              Cell: row => <OurTeam team={row.value} />,
            },
            {
              Header: 'Score',
              id: 'score',
              maxWidth: 80,
              className: 'text-center align-self-center',
              accessor: match => Match.scoreDisplay(match),
            },
            {
              Header: 'Opposition',
              id: 'oppTeam',
              accessor: 'oppTeam',
              className: 'align-self-center',
              headerClassName: 'text-left',
              Cell: row => <OppositionTeam team={row.value} />,
            },
            {
              Header: 'Venue',
              id: 'venue',
              accessor: match => match,
              className: 'align-self-center',
              headerClassName: 'text-left',
              Cell: row => <MatchVenue match={row.value} simple={false} />,
            },
            {
              Header: '',
              id: 'report',
              accessor: match => match,
              className: 'text-center align-self-center',
              width: 45,
              sortable: false,
              Cell: row => <MatchLink match={row.value} />,
            },
          ]}
          data={matches ? matches.results : []}
          loading={loading}
          manual
          onPageChange={page => onChangePage(page + 1)}
          onPageSizeChange={onChangePageSize}
          defaultPageSize={pageSize}
          onSortedChange={this.onSortedChange}
          pages={matches ? Math.ceil(matches.totalCount / pageSize) : 0}
        />
        {matches && <div className="g-py-20">{matches.totalCount} matches</div>}
      </div>
    );
  }
}

MatchListDisplay.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  queryVariables: PropTypes.shape({
    pageSize: PropTypes.number,
  }).isRequired,
  matches: PropTypes.shape(),
  onChangePage: PropTypes.func.isRequired,
  onChangePageSize: PropTypes.func.isRequired,
  onChangeOrderBy: PropTypes.func.isRequired,
};

MatchListDisplay.defaultProps = {
  matches: undefined,
};

export default MatchListDisplay;
