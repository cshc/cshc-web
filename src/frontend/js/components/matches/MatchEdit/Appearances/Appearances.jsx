import React from 'react';
import PropTypes from 'prop-types';
import FlipMove from 'react-flip-move';
import { SelectValueLabelOptionsPropType } from 'components/common/PropTypes';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import Appearance from './Appearance';
import { AccordionId } from '../util';
import StatusIcon from '../StatusIcon';
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

class Appearances extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      uiState: UiState.PlayerSearch,
    };
  }

  render() {
    const { uiState } = this.state;
    const { playerOptions, appearances, ourTeamGender } = this.props;
    return (
      <AccordionCard
        cardId="appearances"
        isOpen
        title="Players"
        accordionId={AccordionId}
        rightIcon={<StatusIcon error={appearances.length < 11} />}
      >
        <div className="card-deck">
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
          <div className="card g-brd-primary rounded-0">
            <div className="card-header text-white g-bg-primary g-brd-transparent rounded-0">
              Team List {appearances.length ? <span>&nbsp;({appearances.length})</span> : null}
            </div>
            <div className="card-body g-pa-0">
              <div className={styles.teamListHeader}>
                <div className={appearanceStyles.name}>Name</div>
                <div className={appearanceStyles.goals}>Goals</div>
                <div className={appearanceStyles.cards}>Cards</div>
                <div className={appearanceStyles.remove} />
              </div>
              {appearances.length ? (
                <FlipMove
                  duration={500}
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
          </div>
        </div>
      </AccordionCard>
    );
  }
}

Appearances.propTypes = {
  playerOptions: SelectValueLabelOptionsPropType.isRequired,
  appearances: PropTypes.arrayOf(AppearancePropType).isRequired,
  ourTeamGender: PropTypes.string.isRequired,
};

Appearances.defaultProps = {};

export default Appearances;
