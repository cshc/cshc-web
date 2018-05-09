import React from 'react';
import PropTypes from 'prop-types';
import reduce from 'lodash/reduce';
import values from 'lodash/values';
import MutationButton from 'components/common/MutationButton';
import { MatchAvailability, MatchAvailabilityAction } from 'util/constants';
import { initStickyDropdown } from 'util/ui';
import styles from './style.scss';

class AvailabilitySummary extends React.PureComponent {
  constructor(props) {
    super(props);
    this.awaitingResponseDropdownId = `sticky-dropdown-${props.matchId}`;
  }

  componentDidMount() {
    initStickyDropdown(`#${this.awaitingResponseDropdownId}`);
  }

  render() {
    const { matchId, availabilityType, availabilities, onActionAvailability } = this.props;
    const getReminderMutationInput = () => ({
      matchId,
      availabilityType,
      availability: MatchAvailability.AwaitingResponse.toLowerCase(),
      action: MatchAvailabilityAction.SendReminder,
    });
    // Initialize a dictionary of counts for each availability type
    const counts = reduce(
      values(MatchAvailability),
      (acc, a) => {
        acc[a] = 0;
        return acc;
      },
      {},
    );
    // Iterate through the availabilities, incrementing the appropriate count each time
    reduce(
      availabilities,
      (acc, a) => {
        acc[a.availability] += 1;
        return acc;
      },
      counts,
    );
    return (
      <div className="">
        <button disabled className="btn btn-sm g-bg-green g-color-white g-mr-10" title="Available">
          <i className="fas fa-check g-mr-5" />
          {counts[MatchAvailability.Available]}
        </button>
        <button
          disabled
          className="btn btn-sm g-bg-red g-color-white g-mr-10"
          title="Not available"
        >
          <i className="fas fa-times g-mr-5" />
          {counts[MatchAvailability.NotAvailable]}
        </button>
        <button
          disabled
          className="btn btn-sm g-bg-gray-dark-v4 g-color-white g-mr-10"
          title="Not sure"
        >
          <i className="fas fa-question g-mr-5" />
          {counts[MatchAvailability.Unsure]}
        </button>
        <div id={this.awaitingResponseDropdownId} className="btn-group g-mr-10">
          <button
            className="btn btn-sm dropdown-toggle g-bg-secondary g-color-black"
            title="Awaiting response"
            aria-haspopup="true"
            aria-expanded="false"
          >
            <i className="fas fa-ellipsis-h g-mr-5" />
            {counts[MatchAvailability.AwaitingResponse]}
          </button>
          <div className={`${styles.dropdownMenu} dropdown-menu`}>
            <MutationButton
              buttonClass="dropdown-item g-cursor-pointer"
              title="Send a reminder email to all players who haven't responded yet"
              label="Send reminder"
              getMutationInput={getReminderMutationInput}
              mutate={onActionAvailability}
              inProgressLabel="Sending..."
              successLabel="Emails sent!"
              failLabel="Send failed"
            />
          </div>
        </div>
      </div>
    );
  }
}

AvailabilitySummary.propTypes = {
  matchId: PropTypes.string.isRequired,
  availabilityType: PropTypes.string.isRequired,
  availabilities: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  onActionAvailability: PropTypes.func.isRequired,
};

AvailabilitySummary.defaultProps = {};

export default AvailabilitySummary;
