import React from 'react';
import PropTypes from 'prop-types';
import AppearanceCard from './Card';
import AppearanceGoals from './Goals';
import styles from './style.scss';

export const AppearancePropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  greenCard: PropTypes.bool.isRequired,
  yellowCard: PropTypes.bool.isRequired,
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
    this.toggleCard = this.toggleCard.bind(this);
    this.updateGoals = this.updateGoals.bind(this);
  }

  updateGoals(goals) {
    this.props.onUpdateAppearance(this.props.index, {
      ...this.props.appearance,
      goals,
    });
  }

  toggleCard(cardProp) {
    this.props.onUpdateAppearance(this.props.index, {
      ...this.props.appearance,
      [cardProp]: !this.props.appearance[cardProp],
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
            isSelected={appearance.greenCard}
            onClick={() => this.toggleCard('greenCard')}
          />
          <AppearanceCard
            color="Yellow"
            imagePath="img/yellow_card.png"
            isSelected={appearance.yellowCard}
            onClick={() => this.toggleCard('yellowCard')}
          />
          <AppearanceCard
            color="Red"
            imagePath="img/red_card.png"
            isSelected={appearance.redCard}
            onClick={() => this.toggleCard('redCard')}
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
