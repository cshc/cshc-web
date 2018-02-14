import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import sumBy from 'lodash/sumBy';
import FlipMove from 'react-flip-move';
import { SelectValueLabelOptionsPropType } from 'components/common/PropTypes';
import Match from 'models/match';
import { ResultPropType } from '../Result/Result';
import Appearance from './Appearance';
import appearanceStyles from './Appearance/style.scss';
import styles from './style.scss';
import PlayerSelection from './PlayerSelection';
import AddMember from './AddMember';
import { AppearancePropType } from './Appearance/Appearance';

const UiState = {
  PlayerSearch: 'Player Search',
  AddMember: 'Add Member',
  SavingNewMember: 'Saving new member',
};

/**
 * The 2nd step of the Match Editing form. 
 * 
 * Provides the UI for adding/editing/removing match appearances (i.e. 
 * the team sheet). 
 * 
 * For each appearance, goals and cards can be easily set.
 * 
 * If the user searches for a player and they can't find them, they are
 * presented with the option of adding a new member.
 */
class Appearances extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      uiState: UiState.PlayerSearch,
    };
  }

  render() {
    const { uiState } = this.state;
    const { playerOptions, appearances, ourTeamGender, result, teamGoals } = this.props;
    const totalGoals = sumBy(appearances, 'goals');
    const goalsClass = classnames('u-label', {
      'u-label-danger': totalGoals > teamGoals,
      'u-label-success': totalGoals === teamGoals,
      'g-color-black': totalGoals < teamGoals,
    });
    return (
      <div className="card-block g-pa-0 g-pa-15--md">
        {!Match.wasPlayed(result) ? (
          <p className="text-center g-py-40 g-font-style-italic">
            {result.altOutcome} matches should not have any players listed.
          </p>
        ) : (
          <div className="row">
            <div className="col-12 col-md-6 g-mb-20">
              <div className={styles.teamListHeader}>
                <div className={appearanceStyles.name}>Name</div>
                <div className={appearanceStyles.goals}>
                  <span className={goalsClass}>
                    Goals ({totalGoals}/{teamGoals})
                  </span>
                </div>
                <div className={appearanceStyles.cards}>Cards</div>
                <div className={appearanceStyles.remove} />
              </div>
              {appearances.length ? (
                <FlipMove
                  duration={200}
                  enterAnimation="accordionVertical"
                  leaveAnimation="accordionVertical"
                >
                  {appearances.map((a, index) => (
                    <Appearance key={a.id} index={index} appearance={a} />
                  ))}
                </FlipMove>
              ) : (
                <div className="g-font-style-italic text-center g-pa-20">
                  Select players to add them to the team list
                </div>
              )}
            </div>
            <div className="col-12 col-md-6">
              {uiState === UiState.PlayerSearch ? (
                <PlayerSelection
                  playerOptions={playerOptions}
                  appearances={appearances}
                  onPlayerNotFound={() => {
                    this.setState({ uiState: UiState.AddMember });
                  }}
                />
              ) : (
                <AddMember
                  ourTeamGender={ourTeamGender}
                  onCancel={() => {
                    this.setState({ uiState: UiState.PlayerSearch });
                  }}
                />
              )}
            </div>
          </div>
        )}
      </div>
    );
  }
}

Appearances.propTypes = {
  playerOptions: SelectValueLabelOptionsPropType.isRequired,
  appearances: PropTypes.arrayOf(AppearancePropType).isRequired,
  ourTeamGender: PropTypes.string.isRequired,
  result: ResultPropType.isRequired,
  teamGoals: PropTypes.number,
};

Appearances.defaultProps = {
  teamGoals: 0,
};

export default Appearances;
