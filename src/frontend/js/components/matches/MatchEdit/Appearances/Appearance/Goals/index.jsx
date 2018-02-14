import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import NumberInput from 'components/common/NumberInput';
import appearanceStyles from '../style.scss';
import styles from './style.scss';

/**
 * A wrapper around the NumberInput for setting the number of goals for a player.
 */
const AppearanceGoals = ({ goals, onUpdateGoals }) => {
  const goalsClass = classnames(styles.goalScore, {
    'g-bg-primary g-color-white g-rounded-50x': goals,
  });
  return (
    <div className={appearanceStyles.goals}>
      <NumberInput
        horizontal
        upIcon="fa fa-plus"
        downIcon="fa fa-minus"
        iconClass="g-color-gray-light-v3 g-color-gray-light-v1--hover"
        value={goals}
        onChangeValue={onUpdateGoals}
        valueClass={goalsClass}
      />
    </div>
  );
};

AppearanceGoals.propTypes = {
  goals: PropTypes.number,
  onUpdateGoals: PropTypes.func.isRequired,
};

AppearanceGoals.defaultProps = {
  goals: undefined,
};

export default AppearanceGoals;
