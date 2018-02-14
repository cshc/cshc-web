import React from 'react';
import PropTypes from 'prop-types';
import FlipMove from 'react-flip-move';
import { SelectValueLabelOptionsPropType } from 'components/common/PropTypes';
import { AwardWinnerPropType } from './AwardWinner/AwardWinner';
import AwardWinner from './AwardWinner';

/**
 * The 3rd step of the Match Editing form.
 * 
 * Each award winner is represented as an editable card. A button is 
 * provided for adding a new (blank) award winner.
 */
const AwardWinners = ({ memberOptions, awardWinners, onAddAwardWinner }) => (
  <div className="card-block">
    <FlipMove className="row" enterAnimation="elevator" leaveAnimation="elevator">
      {awardWinners.map((awardWinner, index) => (
        <div className="col-12 col-md-6" key={awardWinner.id}>
          <AwardWinner awardWinner={awardWinner} index={index} memberOptions={memberOptions} />
        </div>
      ))}
    </FlipMove>
    <button
      className="btn u-btn-outline-primary"
      title="Add a match award winner"
      onClick={onAddAwardWinner}
    >
      <i className="fa fa-plus g-mr-5" />Add award winner
    </button>
  </div>
);

AwardWinners.propTypes = {
  memberOptions: SelectValueLabelOptionsPropType.isRequired,
  awardWinners: PropTypes.arrayOf(AwardWinnerPropType).isRequired,
  onAddAwardWinner: PropTypes.func.isRequired,
};

export default AwardWinners;
