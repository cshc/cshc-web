import React from 'react';
import PropTypes from 'prop-types';
import AppearanceCard from './Card';
import AppearanceGoals from './Goals';
import styles from './style.scss';

export const AppearancePropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  greenCardCount: PropTypes.number.isRequired,
  yellowCardCount: PropTypes.number.isRequired,
  redCard: PropTypes.bool.isRequired,
  goals: PropTypes.number.isRequired,
});

/**
 * Represents a single appearance in the table of players. Each appearance entry displays
 * the player's name, their goals and their cards. There's also a small 'X' used to remove 
 * this appearance.
 */
class Appearance extends React.PureComponent {
  constructor(props) {
    super(props);
    this.toggleCardCount = this.toggleCardCount.bind(this);
    this.toggleRedCard = this.toggleRedCard.bind(this);
    this.updateGoals = this.updateGoals.bind(this);
  }

  updateGoals(goals) {
    this.props.onUpdateAppearance(this.props.index, {
      ...this.props.appearance,
      goals,
    });
  }

  // TODO: Need to add support in the UI for multiple cards
  toggleCardCount(cardProp) {
    this.props.onUpdateAppearance(this.props.index, {
      ...this.props.appearance,
      [cardProp]: this.props.appearance[cardProp] ? 0 : 1,
    });
  }

  toggleRedCard() {
    this.props.onUpdateAppearance(this.props.index, {
      ...this.props.appearance,
      redCard: !this.props.appearance.redCard,
    });
  }

  render() {
    const { index, appearance, onRemoveAppearance } = this.props;

    return (
      <div className={styles.appearance}>
        <div className={styles.name}>{appearance.name}</div>
        <AppearanceGoals goals={appearance.goals} onUpdateGoals={this.updateGoals} />
        <div className={styles.cards}>
          <AppearanceCard
            color="Green"
            imagePath="img/green_card.png"
            isSelected={appearance.greenCardCount > 0}
            onClick={() => this.toggleCardCount('greenCardCount')}
          />
          <AppearanceCard
            color="Yellow"
            imagePath="img/yellow_card.png"
            isSelected={appearance.yellowCardCount > 0}
            onClick={() => this.toggleCardCount('yellowCardCount')}
          />
          <AppearanceCard
            color="Red"
            imagePath="img/red_card.png"
            isSelected={appearance.redCard}
            onClick={this.toggleRedCard}
          />
        </div>
        <div className={styles.remove}>
          <button
            title="Remove this appearance"
            className="btn btn-link g-color-gray-light-v4 g-color-gray-light-v1--hover"
            onClick={() => {
              onRemoveAppearance(index);
            }}
          >
            <i className="fas fa-times" />
          </button>
        </div>
      </div>
    );
  }
}

Appearance.propTypes = {
  index: PropTypes.number.isRequired,
  appearance: AppearancePropType.isRequired,
  onUpdateAppearance: PropTypes.func.isRequired,
  onRemoveAppearance: PropTypes.func.isRequired,
};

Appearance.defaultProps = {};

export default Appearance;
