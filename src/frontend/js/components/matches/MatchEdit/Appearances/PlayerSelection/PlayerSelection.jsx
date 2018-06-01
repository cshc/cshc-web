import React from 'react';
import PropTypes from 'prop-types';
import FlipMove from 'react-flip-move';
import some from 'lodash/some';
import { SelectValueLabelOptionsPropType } from 'components/common/PropTypes';
import { CustomScrollbar } from 'components/Unify';
import { AppearancePropType } from '../Appearance/Appearance';
import PotentialPlayer from './PotentialPlayer';
import styles from './style.scss';

const filterPlayerOptions = (playerOptions, appearances, playerFilter) => {
  const appIds = appearances.map(app => app.id);
  return playerOptions.filter((p) => {
    const id = p.value.split(':')[0];
    if (appIds.includes(id)) return false;
    if (playerFilter) {
      const split = p.label.split(' ');
      return some(split, n => n.toLowerCase().startsWith(playerFilter));
    }
    return true;
  });
};

/**
 * Provides a list of potential players, as well as a search box for searching for players
 * by name (i.e. filtering). 
 * 
 * If no potential players match the filter text, a link to add a new member is displayed instead.
 */
class PlayerSelection extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      playerFilter: '',
      filteredPlayerOptions: filterPlayerOptions(props.playerOptions, props.appearances, undefined),
    };
    this.updateFilter = this.updateFilter.bind(this);
    this.onAddAppearance = this.onAddAppearance.bind(this);
  }

  componentDidMount() {
    window.jQuery.HSCore.helpers.HSFocusState.init();
  }

  componentWillReceiveProps(nextProps) {
    if (
      nextProps.appearances !== this.props.appearances ||
      nextProps.playerOptions !== this.props.playerOptions
    ) {
      this.setState({
        filteredPlayerOptions: filterPlayerOptions(
          nextProps.playerOptions,
          nextProps.appearances,
          this.state.playerFilter,
        ),
      });
    }
  }

  onAddAppearance(id, name) {
    this.updateFilter('');
    this.props.onAddAppearance(id, name);
  }

  updateFilter(filterText) {
    const playerFilter = filterText.toLowerCase();
    this.setState({
      playerFilter,
      filteredPlayerOptions: filterPlayerOptions(
        this.props.playerOptions,
        this.props.appearances,
        playerFilter,
      ),
    });
  }

  render() {
    const { onPlayerNotFound } = this.props;
    const { filteredPlayerOptions, playerFilter } = this.state;
    return (
      <div>
        <div className="input-group g-brd-primary--focus g-px-15 g-px-0--md">
          <input
            className="form-control form-control-md border-right-0 rounded-0 pr-0"
            type="text"
            placeholder="Search for player..."
            value={playerFilter}
            onChange={(ev) => {
              this.updateFilter(ev.target.value);
            }}
          />
          <div className="input-group-append">
            <span className="input-group-text rounded-0 g-color-gray-light-v1">
              <i className="fas fa-search" />
            </span>
          </div>
        </div>
        <div className="g-my-20">
          {filteredPlayerOptions.length ? (
            <CustomScrollbar maxHeight="340px" className={styles.appearancesScrollbox}>
              <FlipMove
                duration={500}
                enterAnimation="accordionVertical"
                leaveAnimation="accordionVertical"
              >
                {filteredPlayerOptions.map(p => (
                  <PotentialPlayer
                    key={p.value}
                    player={p}
                    onAddAppearance={this.onAddAppearance}
                  />
                ))}
              </FlipMove>
            </CustomScrollbar>
          ) : (
            <div>
              <a className="g-cursor-pointer" tabIndex="0" role="link" onClick={onPlayerNotFound}>
                Player not found?
              </a>
              <p>Make sure this person is not already on the team list!</p>
            </div>
          )}
        </div>
      </div>
    );
  }
}

PlayerSelection.propTypes = {
  playerOptions: SelectValueLabelOptionsPropType.isRequired,
  appearances: PropTypes.arrayOf(AppearancePropType).isRequired,
  onAddAppearance: PropTypes.func.isRequired,
  onPlayerNotFound: PropTypes.func.isRequired,
};

PlayerSelection.defaultProps = {};

export default PlayerSelection;
