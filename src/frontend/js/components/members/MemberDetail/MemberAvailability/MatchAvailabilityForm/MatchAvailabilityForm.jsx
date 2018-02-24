import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import FlipMove from 'react-flip-move';
import { MatchAvailability } from 'util/constants';
import MutationButton from 'components/common/MutationButton';
import styles from './style.scss';

/** 
 * This component handles the setting of availability for a particular member and match.
 * The user can select their availability ("I can play", "I can't play", "Not sure")
 * and add an optional comment. Changes are immediately saved to the server via the 
 * matchAvailabilityMutation.
*/
class MatchAvailabilityForm extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      availability: props.umpiring
        ? props.availability.umpiringAvailability
        : props.availability.playingAvailability,
      comment: props.availability.comment,
      commentExpanded: !!props.availability.comment,
    };
    this.onKeyPress = this.onKeyPress.bind(this);
    this.setAvailability = this.setAvailability.bind(this);
    this.updateComment = this.updateComment.bind(this);
    this.toggleComment = this.toggleComment.bind(this);
    this.getMutationInput = this.getMutationInput.bind(this);
    this.commitComment = this.commitComment.bind(this);
  }

  componentDidMount() {
    window.jQuery('.comment-btn').tooltip();
  }

  onKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      this.commitComment();
      e.preventDefault();
    }
  }

  setAvailability(availability) {
    this.setState({ availability }, () => {
      this.mutationButton.mutate();
    });
  }

  getMutationInput() {
    return {
      matchId: parseInt(this.props.availability.match.id, 10),
      memberId: this.props.member.id,
      playingAvailability: this.props.umpiring ? null : this.state.availability.toLowerCase(),
      umpiringAvailability: this.props.umpiring ? this.state.availability.toLowerCase() : null,
      comment: this.state.comment,
    };
  }

  toggleComment() {
    if (this.state.commentExpanded && this.state.comment) {
      this.setState(
        {
          comment: undefined,
          commentExpanded: false,
        },
        () => {
          this.mutationButton.mutate();
        },
      );
    } else {
      this.setState({
        commentExpanded: !this.state.commentExpanded,
      });
    }
  }

  updateComment(ev) {
    this.setState({ comment: ev.target.value });
  }

  commitComment() {
    this.mutationButton.mutate();
  }

  render() {
    const { umpiring, onUpdateAvailability } = this.props;
    const { availability, comment, commentExpanded } = this.state;
    return (
      <div className="">
        <div className="d-flex flex-wrap">
          <button
            className={classnames('g-mr-10 g-mb-10 btn', {
              'btn-success': availability === MatchAvailability.Available,
              'btn-outline-success': availability !== MatchAvailability.Available,
            })}
            onClick={() => {
              this.setAvailability(MatchAvailability.Available);
            }}
          >
            <i className="fas fa-check" />
            <span className="g-hidden-sm-down g-ml-5">I can {umpiring ? 'umpire' : 'play'}</span>
          </button>
          <button
            className={classnames('g-mr-10 g-mb-10 btn', {
              'btn-danger': availability === MatchAvailability.NotAvailable,
              'btn-outline-danger': availability !== MatchAvailability.NotAvailable,
            })}
            onClick={() => {
              this.setAvailability(MatchAvailability.NotAvailable);
            }}
          >
            <i className="fas fa-times" />
            <span className="g-hidden-sm-down g-ml-5">
              I can&#39;t {umpiring ? 'umpire' : 'play'}
            </span>
          </button>
          <button
            className={classnames('g-mr-10 g-mb-10 btn', {
              'btn-secondary': availability === MatchAvailability.Unsure,
              'btn-outline-secondary': availability !== MatchAvailability.Unsure,
            })}
            onClick={() => {
              this.setAvailability(MatchAvailability.Unsure);
            }}
          >
            <i className="fas fa-question" />
            <span className="g-hidden-sm-down g-ml-5">Not sure</span>
          </button>
          <button
            data-toggle="tooltip"
            data-placement="top"
            data-trigger="hover"
            title=""
            data-original-title={commentExpanded ? 'Remove comment' : 'Add comment'}
            className="comment-btn g-mr-10 g-mb-10 btn btn-link g-color-gray-light-v2 g-color-gray-light-v1--hover"
            onClick={this.toggleComment}
          >
            <span className="fa-stack">
              <i className="g-mt-1 fas fa-comment fa-stack-2x" />
              <i
                className={classnames('g-ml-2 g-mb-1 fas fa-stack-1x fa-inverse', {
                  'fa-plus': !commentExpanded,
                  'fa-minus': commentExpanded,
                })}
              />
            </span>
          </button>
          <MutationButton
            ref={(c) => {
              this.mutationButton = c;
            }}
            buttonClass="btn btn-link g-mb-10"
            passive
            inProgressLabel={null}
            successLabel={null}
            failLabel={null}
            mutate={onUpdateAvailability}
            getMutationInput={this.getMutationInput}
          />
        </div>
        <div>
          <FlipMove
            duration={200}
            enterAnimation="accordionVertical"
            leaveAnimation="accordionVertical"
          >
            {commentExpanded ? (
              <textarea
                className={`form-control form-control-md rounded-0 ${styles.comment}`}
                rows={2}
                placeholder="Any comments?"
                value={comment}
                onChange={this.updateComment}
                onBlur={this.commitComment}
                onKeyPress={this.onKeyPress}
              />
            ) : null}
          </FlipMove>
        </div>
      </div>
    );
  }
}

MatchAvailabilityForm.propTypes = {
  member: PropTypes.shape({
    id: PropTypes.number,
  }).isRequired,
  availability: PropTypes.shape({
    match: PropTypes.shape({
      id: PropTypes.string,
    }).isRequired,
    playingAvailability: PropTypes.string,
    umpiringAvailability: PropTypes.string,
    comment: PropTypes.string,
  }).isRequired,
  umpiring: PropTypes.bool,
  onUpdateAvailability: PropTypes.func.isRequired,
};

MatchAvailabilityForm.defaultProps = {
  umpiring: false,
};

export default MatchAvailabilityForm;
