import React from 'react';
import PropTypes from 'prop-types';
import { SelectValueLabelOptionPropType } from 'components/common/PropTypes';

class PotentialPlayer extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      adding: false,
    };
    this.onAddAppearance = this.onAddAppearance.bind(this);
  }

  onAddAppearance() {
    // Prevent duplicate additions
    if (this.state.adding) {
      return;
    }

    const { player } = this.props;
    this.setState({ adding: true }, () => {
      this.props.onAddAppearance(player.value.split(':')[0], player.label);
    });
  }

  render() {
    const { player } = this.props;
    return (
      <div
        className="g-py-4 g-cursor-pointer"
        role="link"
        tabIndex="0"
        title="Add player"
        onClick={this.onAddAppearance}
      >
        {player.label}
      </div>
    );
  }
}

PotentialPlayer.propTypes = {
  player: SelectValueLabelOptionPropType.isRequired,
  onAddAppearance: PropTypes.func.isRequired,
};

PotentialPlayer.defaultProps = {};

export default PotentialPlayer;
