import React from 'react';
import PropTypes from 'prop-types';
import StickyBar from 'components/common/StickyBar';
import Urls from 'util/urls';
import Appearance from 'models/appearance';
import MatchAwardWinner from 'models/matchAwardWinner';

/**
 *  The sticky bar at the top of the match edit form that contains the 
 *  Save and Cancel buttons.
 * 
 *  Note: The Save button is disabled unless the form data is 'dirty' (has changed).
 */
class MatchEditTopBar extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      updating: false,
    };
    this.updateMatch = this.updateMatch.bind(this);
    this.returnToMatchDetails = this.returnToMatchDetails.bind(this);
  }

  updateMatch() {
    const { matchId, matchState, onUpdateMatch } = this.props;

    this.setState({ updating: true }, () => {
      const editMatchInput = {
        matchId: parseInt(matchId, 10),
        ourScore: parseInt(matchState.result.ourScore, 10),
        oppScore: parseInt(matchState.result.oppScore, 10),
        ourHtScore: parseInt(matchState.result.ourHtScore, 10),
        oppHtScore: parseInt(matchState.result.oppHtScore, 10),
        altOutcome: matchState.result.altOutcome,
        appearances: Appearance.toAppearanceInputArray(matchState.appearances),
        awardWinners: MatchAwardWinner.toAwardWinnerInputList(matchState.awardWinners),
        reportAuthorId: matchState.report.author
          ? parseInt(matchState.report.author.split(':')[0], 10)
          : undefined,
        reportTitle: matchState.report.title,
        reportContent: matchState.report.content,
      };
      onUpdateMatch(editMatchInput)
        .then(({ data }) => {
          console.log(data);
          this.setState({ updating: false });
          if (!data.errors.length) {
            // this.returnToMatchDetails();
          }
        })
        .catch((error) => {
          console.log(error);
          this.setState({ updating: false });
        });
    });
  }

  returnToMatchDetails() {
    window.location = Urls.match_detail(this.props.matchId);
  }

  render() {
    const { matchState } = this.props;
    const { updating } = this.state;
    return (
      <StickyBar className="container g-z-index-99 d-flex g-bg-gray-light-v4 justify-content-between g-py-10">
        <button onClick={this.returnToMatchDetails} className="btn u-btn-outline-darkgray">
          Cancel
        </button>
        <button
          disabled={!matchState.dirty || updating}
          onClick={this.updateMatch}
          className="btn u-btn-primary"
        >
          {updating ? <i className="fa fa-spinner fa-spin g-mr-5" /> : null}
          Save
        </button>
      </StickyBar>
    );
  }
}

MatchEditTopBar.propTypes = {
  matchId: PropTypes.number.isRequired,
  matchState: PropTypes.shape().isRequired,
  onUpdateMatch: PropTypes.func.isRequired,
};

export default MatchEditTopBar;
