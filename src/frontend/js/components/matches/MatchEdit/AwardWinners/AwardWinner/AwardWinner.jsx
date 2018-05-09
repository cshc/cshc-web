import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Select from 'react-select';
import { SelectValueLabelOptionsPropType } from 'components/common/PropTypes';
import { MatchAward } from 'util/constants';
import Member from 'models/member';
import MatchAwardWinner from 'models/matchAwardWinner';
import styles from './style.scss';

export const AwardWinnerPropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  member: PropTypes.string,
  awardee: PropTypes.string,
  comment: PropTypes.string,
  award: PropTypes.oneOf([MatchAward.MOM, MatchAward.LOM]).isRequired,
});

/**
 * The card for editing the details of a particular award winner.
 * 
 * The user can toggle the award type (Man of the Match/Lemon of the Match),
 * select a member or enter the name of a non-member as the award winner,
 * and enter a comment about why the person won the award.
 */
class AwardWinner extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      selectingMember: !props.awardWinner.awardee,
      comment: props.awardWinner.comment,
    };
    this.toggleAwardRecipientType = this.toggleAwardRecipientType.bind(this);
    this.updateMember = this.updateMember.bind(this);
    this.updateAwardee = this.updateAwardee.bind(this);
    this.updateAwardType = this.updateAwardType.bind(this);
    this.updateComment = this.updateComment.bind(this);
  }

  toggleAwardRecipientType() {
    if (this.state.selectingMember) {
      this.setState({ selectingMember: false });
      this.updateAwardee('');
    } else {
      this.setState({ selectingMember: true });
      this.updateMember(undefined);
    }
  }

  updateMember(member) {
    this.props.onUpdateAwardWinner(
      {
        ...this.props.awardWinner,
        awardee: undefined,
        member,
      },
      this.props.index,
    );
  }

  updateAwardee(awardee) {
    this.props.onUpdateAwardWinner(
      {
        ...this.props.awardWinner,
        member: undefined,
        awardee,
      },
      this.props.index,
    );
  }

  updateComment(ev) {
    this.props.onUpdateAwardWinner(
      {
        ...this.props.awardWinner,
        comment: ev.target.value,
      },
      this.props.index,
    );
  }

  updateAwardType(awardName) {
    this.props.onUpdateAwardWinner(
      {
        ...this.props.awardWinner,
        award: awardName,
      },
      this.props.index,
    );
  }

  render() {
    const { index, awardWinner, memberOptions, onRemoveAwardWinner } = this.props;
    const { selectingMember, comment } = this.state;
    const isMom = awardWinner.award === MatchAward.MOM;
    const momClass = classnames('btn g-mr-10', {
      'u-btn-primary': isMom,
      'btn-link': !isMom,
    });
    const lomClass = classnames('btn g-mr-10', {
      'u-btn-yellow': !isMom,
      'btn-link': isMom,
    });
    const selectId = `select-award-member-${awardWinner.member || 'new'}`;
    const textAreaId = `ta-award-member-${awardWinner.member || 'new'}`;
    return (
      <div className="u-shadow-v3 g-bg-secondary g-brd-around g-brd-gray-light-v4 g-line-height-2 g-pa-10 g-pa-20--md g-mb-30">
        <div className="d-flex justify-content-between">
          <div className="d-flex align-items-center">
            <button
              className={momClass}
              title={MatchAward.MOM}
              onClick={() => {
                this.updateAwardType(MatchAward.MOM);
              }}
            >
              <i className="fas fa-star" />
            </button>
            <button
              className={lomClass}
              title={MatchAward.LOM}
              onClick={() => {
                this.updateAwardType(MatchAward.LOM);
              }}
            >
              <i className="fas fa-lemon" />
            </button>
            <div className="">{awardWinner.award}</div>
            {MatchAwardWinner.isValid(awardWinner) ? (
              <i className="fas fa-lg fa-check-square g-color-green g-ml-10" />
            ) : null}
          </div>
          <div>
            <button
              onClick={() => {
                onRemoveAwardWinner(index);
              }}
              className="btn btn-link g-color-gray-light-v1 g-color-gray-dark-v4--hover"
              title="Delete this award winner"
            >
              <i className="far fa-lg fa-trash-alt" />
            </button>
          </div>
        </div>
        <div className={styles.recipient}>
          {selectingMember ? (
            <Select
              id={selectId}
              className="flex-1 g-max-width-400--md"
              placeholder="Select member..."
              options={memberOptions}
              simpleValue
              clearable
              searchable
              name={selectId}
              value={Member.toSelectOption(awardWinner.member)}
              onChange={this.updateMember}
            />
          ) : (
            <input
              type="flex-1 text"
              value={awardWinner.awardee}
              onChange={(ev) => {
                this.updateAwardee(ev.target.value);
              }}
              className="form-control form-control-md rounded-0"
              placeholder="Name (not a member)"
            />
          )}
          <button
            className="flex-0-auto btn btn-link"
            title={selectingMember ? "Enter a non-member's name" : 'Select a member instead'}
            onClick={this.toggleAwardRecipientType}
          >
            {selectingMember ? 'Not a member?' : 'Select a member'}
          </button>
        </div>
        <textarea
          id={textAreaId}
          name={textAreaId}
          className="g-pt-10 form-control form-control-md g-resize-none rounded-0"
          rows="3"
          placeholder="Why did this person win this award?"
          value={comment}
          onChange={(ev) => {
            this.setState({ comment: ev.target.value });
          }}
          onBlur={this.updateComment}
        />
      </div>
    );
  }
}

AwardWinner.propTypes = {
  index: PropTypes.number.isRequired,
  awardWinner: AwardWinnerPropType.isRequired,
  memberOptions: SelectValueLabelOptionsPropType.isRequired,
  onUpdateAwardWinner: PropTypes.func.isRequired,
  onRemoveAwardWinner: PropTypes.func.isRequired,
};

export default AwardWinner;
