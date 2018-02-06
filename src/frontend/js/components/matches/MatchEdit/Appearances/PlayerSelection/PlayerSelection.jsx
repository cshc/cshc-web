import React from 'react';
import PropTypes from 'prop-types';
import FlipMove from 'react-flip-move';
import some from 'lodash/some';
import { SelectValueLabelOptionsPropType } from 'components/common/PropTypes';
import { CustomScrollbar } from 'components/Unify';
import { AppearancePropType } from '../Appearance/Appearance';
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

class PlayerSelection extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      playerFilter: undefined,
      filteredPlayerOptions: filterPlayerOptions(props.playerOptions, props.appearances, undefined),
    };
    this.updateFilter = this.updateFilter.bind(this);
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

  updateFilter(ev) {
    const playerFilter = ev.target.value.toLowerCase();
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
    const { onAddAppearance, onPlayerNotFound } = this.props;
    const { filteredPlayerOptions } = this.state;
    return (
      <div className="card rounded-0">
        <div className="card-header rounded-0">Select players...</div>
        <div className="card-body">
          <div className="input-group g-brd-primary--focus">
            <input
              className="form-control form-control-md border-right-0 rounded-0 pr-0"
              type="text"
              placeholder="Search for player..."
              onChange={this.updateFilter}
            />
            <div className="input-group-addon d-flex align-items-center g-bg-white g-color-gray-light-v1 rounded-0">
              <i className="fa fa-search" />
            </div>
          </div>
          <div className="g-my-20">
            {filteredPlayerOptions.length ? (
              <CustomScrollbar maxHeight="200px" className={styles.appearancesScrollbox}>
                <FlipMove
                  duration={500}
                  enterAnimation="accordionVertical"
                  leaveAnimation="accordionVertical"
                >
                  {filteredPlayerOptions.map(p => (
                    <div
                      className="g-py-4 g-cursor-pointer"
                      role="link"
                      tabIndex="0"
                      title="Add player"
                      key={p.value}
                      onClick={() => {
                        onAddAppearance(p.value.split(':')[0], p.label);
                      }}
                    >
                      {p.label}
                    </div>
                  ))}
                </FlipMove>
              </CustomScrollbar>
            ) : (
              <a className="g-cursor-pointer" tabIndex="0" role="link" onClick={onPlayerNotFound}>
                Player not found?
              </a>
            )}
          </div>
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
