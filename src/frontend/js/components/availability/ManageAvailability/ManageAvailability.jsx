import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import dotProp from 'dot-prop-immutable';
import { NetworkStatus as NS } from 'apollo-client';
import MatchDate from 'components/matches/MatchDate';
import MatchTime from 'components/matches/MatchTime';
import MatchVenue from 'components/matches/MatchVenue';
import OppositionTeam from 'components/matches/OppositionTeam';
import MutationButton from 'components/common/MutationButton';
import ErrorDisplay from 'components/common/ErrorDisplay';
import commonStyles from 'components/common/style.scss';
import Member from 'models/member';
import AvailabilitySummary from './AvailabilitySummary';
import AvailabilityDetail from './AvailabilityDetail';
import styles from './style.scss';

class ManageAvailability extends React.PureComponent {
  constructor(props) {
    super(props);
    this.playerOptions = props.playerOptions.map(Member.toSelectOption);
    this.state = {
      availabilities: this.getAvailabilities(props, {}),
    };
    this.addMatchAvailability = this.addMatchAvailability.bind(this);
    this.removeMatchAvailability = this.removeMatchAvailability.bind(this);
    this.getCreateMutationInput = this.getCreateMutationInput.bind(this);
    this.addSquadAvailabilities = this.addSquadAvailabilities.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    // If the set of matches changes, assume the freshly fetched match
    // availabilities are the ones to use.
    if (this.props.matches !== nextProps.matches) {
      const newAvailabilities = this.getAvailabilities(nextProps, this.state.availabilities);
      this.setState({ availabilities: newAvailabilities });
    }
  }

  getAvailabilities(props, availabilities = {}) {
    let newAvailabilities = availabilities;
    if (props.matches && props.matches.results) {
      props.matches.results.forEach((match) => {
        newAvailabilities = dotProp.set(newAvailabilities, match.id, match.availabilities.results);
      });
    }
    return newAvailabilities;
  }

  getCreateMutationInput(matchId) {
    return {
      matchId: parseInt(matchId, 10),
      availabilityType: this.props.availabilityType,
    };
  }

  addSquadAvailabilities(matchId, availabilities) {
    const matchAvailabilities = this.state.availabilities[matchId];
    availabilities.forEach((availability) => {
      if (!matchAvailabilities.find(a => a.member.id === availability.member.id)) {
        matchAvailabilities.push(availability);
      }
    });
    this.setState({
      availabilities: dotProp.set(this.state.availabilities, matchId, matchAvailabilities),
    });
  }

  addMatchAvailability(matchId, availability) {
    const matchAvailabilities = this.state.availabilities[matchId].concat([availability]);
    this.setState({
      availabilities: dotProp.set(this.state.availabilities, matchId, matchAvailabilities),
    });
  }

  removeMatchAvailability(matchId, availability) {
    const matchAvailabilities = this.state.availabilities[matchId].filter(
      a => a.member.id !== availability.member.id,
    );
    this.setState({
      availabilities: dotProp.set(this.state.availabilities, matchId, matchAvailabilities),
    });
  }

  render() {
    const {
      availabilityType,
      networkStatus,
      error,
      matches,
      page,
      pageSize,
      onChangePage,
      onChangePageSize,
      onCreateAvailability,
      onActionAvailability,
    } = this.props;
    const { availabilities } = this.state;
    if (error) {
      return <ErrorDisplay errorMessage="Could not fetch match availabilities." />;
    }
    return (
      <div className={commonStyles.reactTable}>
        <ReactTable
          collapseOnDataChange={false}
          showPageJump={false}
          columns={[
            {
              Header: 'Date',
              id: 'date',
              accessor: 'date',
              headerClassName: 'text-left',
              width: 90,
              Cell: row => <MatchDate date={row.value} format="Do MMM YY" />,
            },
            {
              Header: 'Time',
              id: 'time',
              className: 'g-hidden-sm-down',
              headerClassName: 'text-left g-hidden-sm-down',
              width: 70,
              Cell: row => <MatchTime match={row.original} />,
            },
            {
              Header: 'Opposition',
              id: 'opposition',
              headerClassName: 'text-left',
              accessor: 'oppTeam',
              Cell: row => <OppositionTeam team={row.value} />,
            },
            {
              Header: 'Venue',
              id: 'venue',
              className: 'g-hidden-sm-down',
              headerClassName: 'text-left g-hidden-sm-down',
              Cell: row => <MatchVenue match={row.original} />,
            },
            {
              Header: 'Availability',
              id: 'availability',
              accessor: 'id',
              className: `${styles.availabilityCell} text-center`,
              Cell: (row) => {
                if (!availabilities[row.value] || !availabilities[row.value].length) {
                  return (
                    <MutationButton
                      buttonClass="btn u-btn-outline-primary"
                      label="Email squad for availabilities"
                      getMutationInput={() => this.getCreateMutationInput(row.value)}
                      mutate={onCreateAvailability}
                      onSuccess={data =>
                        this.addSquadAvailabilities(
                          row.value,
                          data.createMatchAvailability.matchAvailabilities,
                        )}
                      inProgressLabel="Requesting..."
                      successLabel="Emails sent!"
                      failLabel="Request failed"
                    />
                  );
                }
                return (
                  <AvailabilitySummary
                    matchId={row.value}
                    availabilityType={availabilityType}
                    availabilities={availabilities[row.value]}
                    onActionAvailability={onActionAvailability}
                  />
                );
              },
            },
          ]}
          noDataText="No upcoming matches"
          sortable={false}
          data={matches ? matches.results : []}
          loading={networkStatus === NS.loading}
          SubComponent={row =>
            (availabilities[row.original.id] ? (
              <AvailabilityDetail
                playerOptions={this.playerOptions}
                matchId={row.original.id}
                availabilities={availabilities[row.original.id]}
                availabilityType={availabilityType}
                onMatchAvailabilityRemoved={this.removeMatchAvailability}
                onMatchAvailabilityAdded={this.addMatchAvailability}
              />
            ) : (
              undefined
            ))}
          manual
          page={page - 1}
          onPageChange={p => onChangePage(p + 1)}
          onPageSizeChange={onChangePageSize}
          defaultPageSize={pageSize}
          pages={matches ? Math.ceil(matches.totalCount / pageSize) : 0}
        />
      </div>
    );
  }
}

ManageAvailability.propTypes = {
  playerOptions: PropTypes.arrayOf(PropTypes.string).isRequired,
  availabilityType: PropTypes.string.isRequired,
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  pageSize: PropTypes.number.isRequired,
  page: PropTypes.number.isRequired,
  matches: PropTypes.shape({
    results: PropTypes.arrayOf(PropTypes.shape()),
    totalCount: PropTypes.number,
  }),
  onChangePage: PropTypes.func.isRequired,
  onChangePageSize: PropTypes.func.isRequired,
  onCreateAvailability: PropTypes.func.isRequired,
  onActionAvailability: PropTypes.func.isRequired,
};

ManageAvailability.defaultProps = {
  error: undefined,
  matches: undefined,
};

export default ManageAvailability;
