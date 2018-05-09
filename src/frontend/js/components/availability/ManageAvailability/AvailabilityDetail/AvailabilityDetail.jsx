import React from 'react';
import PropTypes from 'prop-types';
import FlipMove from 'react-flip-move';
import Select from 'react-select';
import Availability from 'models/availability';
import Member from 'models/member';
import MutationButton from 'components/common/MutationButton';
import MemberLink from 'components/members/MemberLink';
import MemberAvailabilityLabel from 'components/availability/MemberAvailabilityLabel';
import { MatchAvailability, MatchAvailabilityAction } from 'util/constants';
import styles from './style.scss';

class AvailabilityDetail extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      playerToAdd: null,
      messageToAddedPlayer: '',
    };
    this.getDeleteMutationInput = this.getDeleteMutationInput.bind(this);
    this.getUpdateMutationInput = this.getUpdateMutationInput.bind(this);
    this.onPlayerAdded = this.onPlayerAdded.bind(this);
  }

  onPlayerAdded(data) {
    this.setState({
      playerToAdd: null,
      messageToAddedPlayer: '',
    });
    this.props.onMatchAvailabilityAdded(
      this.props.matchId,
      data.updateMatchAvailability.availability,
    );
  }

  getDeleteMutationInput(memberId) {
    return {
      matchId: parseInt(this.props.matchId, 10),
      memberId,
      availabilityType: this.props.availabilityType,
      action: MatchAvailabilityAction.Delete,
    };
  }

  getUpdateMutationInput() {
    return {
      matchId: parseInt(this.props.matchId, 10),
      memberId: Member.decode(this.state.playerToAdd).id,
      availabilityType: this.props.availabilityType,
      availability: MatchAvailability.AwaitingResponse.toLowerCase(),
      message: this.state.messageToAddedPlayer || undefined,
    };
  }

  render() {
    const {
      matchId,
      playerOptions,
      availabilities,
      availabilityType,
      onUpdateAvailability,
      onActionAvailability,
      onMatchAvailabilityRemoved,
    } = this.props;
    const { playerToAdd, messageToAddedPlayer } = this.state;
    const availabilityMemberIds = availabilities.map(a => a.member.id);
    const filteredPlayerOptions = playerOptions.filter(p => !availabilityMemberIds.includes(p.id));
    return (
      <div className="row g-pa-0 g-pa-15--md">
        <div className="col-12 col-md-6 g-mb-20">
          <div className={styles.header}>
            <div className={styles.name}>Name</div>
            <div className={styles.availabilities}>
              Can {Availability.context(availabilityType)}?
            </div>
            <div className={styles.action} />
          </div>
          <FlipMove
            duration={200}
            enterAnimation="accordionVertical"
            leaveAnimation="accordionVertical"
          >
            {availabilities.map(a => (
              <div key={a.id} className={styles.memberAvailabilityRow}>
                <div className={styles.name}>
                  <MemberLink member={a.member} useFullName />
                </div>
                <div className={styles.availabilities}>
                  <MemberAvailabilityLabel availability={a.availability} />
                </div>
                <div className={styles.action}>
                  <MutationButton
                    buttonClass="btn btn-link g-color-gray-light-v4 g-color-gray-light-v1--hover"
                    title="Remove this player"
                    icon="fas fa-times"
                    getMutationInput={() => this.getDeleteMutationInput(a.member.id)}
                    inProgressLabel={null}
                    successLabel={null}
                    failLabel={null}
                    mutate={onActionAvailability}
                    onSuccess={() => {
                      onMatchAvailabilityRemoved(matchId, a);
                    }}
                  />
                </div>
              </div>
            ))}
          </FlipMove>
        </div>
        <div className="col-12 col-md-6 g-mb-20">
          <div className="d-flex flex-wrap align-items-center">
            <span className="flex-0 text-nowrap g-mr-10 g-mb-10">Add a player:</span>
            <Select
              className="flex-1 g-mb-10"
              placeholder="Select player..."
              options={filteredPlayerOptions}
              simpleValue
              clearable
              searchable
              name={`${matchId}-add-member-select`}
              value={playerToAdd}
              onChange={(player) => {
                this.setState({ playerToAdd: player });
              }}
            />
          </div>
          <textarea
            name={`${matchId}-add-member-comment`}
            className="g-pt-10 form-control form-control-md g-resize-none rounded-0 g-mb-10"
            rows="3"
            placeholder="Optional message"
            value={messageToAddedPlayer}
            onChange={(ev) => {
              this.setState({ messageToAddedPlayer: ev.target.value });
            }}
          />
          <MutationButton
            disabled={!playerToAdd}
            buttonClass="float-right btn u-btn-outline-primary"
            label="Request availability"
            getMutationInput={this.getUpdateMutationInput}
            mutate={onUpdateAvailability}
            onSuccess={this.onPlayerAdded}
            inProgressLabel="Requesting..."
            successLabel="Email sent!"
            failLabel="Request failed"
          />
        </div>
      </div>
    );
  }
}

AvailabilityDetail.propTypes = {
  matchId: PropTypes.string.isRequired,
  playerOptions: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string,
      label: PropTypes.string,
    }),
  ).isRequired,
  availabilities: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  availabilityType: PropTypes.string.isRequired,
  onUpdateAvailability: PropTypes.func.isRequired,
  onActionAvailability: PropTypes.func.isRequired,
  onMatchAvailabilityRemoved: PropTypes.func.isRequired,
  onMatchAvailabilityAdded: PropTypes.func.isRequired,
};

export default AvailabilityDetail;
