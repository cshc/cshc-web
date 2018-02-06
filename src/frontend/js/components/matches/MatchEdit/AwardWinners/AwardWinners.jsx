import React from 'react';
import PropTypes from 'prop-types';
import FlipMove from 'react-flip-move';
import some from 'lodash/some';
import { SelectValueLabelOptionsPropType } from 'components/common/PropTypes';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import MatchAwardWinner from 'models/matchAwardWinner';
import { AccordionId } from '../util';
import { AwardWinnerPropType } from './AwardWinner/AwardWinner';
import StatusIcon from '../StatusIcon';
import AwardWinner from './AwardWinner';

const AwardWinners = ({ memberOptions, awardWinners, onAddAwardWinner }) => (
  <AccordionCard
    cardId="awards"
    isOpen
    title="Awards"
    accordionId={AccordionId}
    rightIcon={
      <StatusIcon
        error={awardWinners.length < 2 || some(awardWinners, a => !MatchAwardWinner.isValid(a))}
      />
    }
  >
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
  </AccordionCard>
);

AwardWinners.propTypes = {
  memberOptions: SelectValueLabelOptionsPropType.isRequired,
  awardWinners: PropTypes.arrayOf(AwardWinnerPropType).isRequired,
  onAddAwardWinner: PropTypes.func.isRequired,
};

export default AwardWinners;
