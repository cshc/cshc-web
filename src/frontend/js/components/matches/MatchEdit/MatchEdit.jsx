import React from 'react';
import PropTypes from 'prop-types';
import MultiStepForm from 'components/common/MultiStepForm';
import MutationButton from 'components/common/MutationButton';
import Appearance from 'models/appearance';
import MatchAwardWinner from 'models/matchAwardWinner';
import Match from 'models/match';
import Urls from 'util/urls';
import Result from './Result';
import Appearances from './Appearances';
import AwardWinners from './AwardWinners';
import Report from './Report';
import AppearancesTitle from './Appearances/AppearancesTitle';
import {
  ResultNavigationNode,
  AppearancesNavigationNode,
  AwardsNavigationNode,
  ReportNavigationNode,
} from './NavigationNodes';
import styles from './style.scss';

const slides = [
  {
    label: 'Result',
    navigationNode: ResultNavigationNode,
  },
  {
    label: 'Players',
    title: <AppearancesTitle />,
    navigationNode: AppearancesNavigationNode,
  },
  {
    label: 'Awards',
    navigationNode: AwardsNavigationNode,
  },
  {
    label: 'Report',
    navigationNode: ReportNavigationNode,
  },
];

/**
 *  The top-level component for the Match Edit app.
 * 
 *  This component works as a 'progressive form', with each
 *  section implemented as a carousel page.
 * 
 */
class MatchEdit extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      currentSlideIndex: 0,
    };
    this.getMutationInput = this.getMutationInput.bind(this);
    this.saveMatchDetails = this.saveMatchDetails.bind(this);

    // Warn the user if they leave this page when there is unsaved data.
    window.addEventListener('beforeunload', (e) => {
      if (!this.props.isDirty) {
        return undefined;
      }
      const confirmationMessage =
        'It looks like you have been editing something. ' +
        'If you leave before saving, your changes will be lost.';

      (e || window.event).returnValue = confirmationMessage; // Gecko + IE
      return confirmationMessage; // Gecko + Webkit, Safari, Chrome etc.
    });
  }

  componentDidMount() {
    // When we first display the form, skip ahead to the first incomplete
    // section of the form.
    let slideIndex = 0;
    if (Match.resultIsComplete(this.props.matchState)) {
      slideIndex = 1;
      if (Match.appearancesIsComplete(this.props.matchState)) {
        slideIndex = 2;
        if (Match.awardsIsComplete(this.props.matchState)) {
          slideIndex = 3;
        }
        if (Match.reportIsComplete(this.props.matchState)) {
          slideIndex = 0;
        }
      }
    }

    if (slideIndex > 0) {
      window.setTimeout(() => {
        this.form.goToSlide(slideIndex);
      }, 500);
    }
  }

  /**
   * This method is passed to the 'Publish' MutationButton component to provide
   * the input for the updateMatch mutation.
   */
  getMutationInput() {
    const { matchId, matchState } = this.props;

    return {
      matchId: parseInt(matchId, 10),
      ourScore: parseInt(matchState.result.ourScore, 10),
      oppScore: parseInt(matchState.result.oppScore, 10),
      ourHtScore: parseInt(matchState.result.ourHtScore, 10),
      oppHtScore: parseInt(matchState.result.oppHtScore, 10),
      altOutcome: matchState.result.altOutcome,
      appearances: Appearance.toAppearanceInputArray(
        matchState.appearances,
        matchState.result.altOutcome,
      ),
      awardWinners: MatchAwardWinner.toAwardWinnerInputList(matchState.awardWinners),
      reportAuthorId: matchState.report.author
        ? parseInt(matchState.report.author.split(':')[0], 10)
        : undefined,
      reportTitle: matchState.report.title,
      reportContent: matchState.report.content,
    };
  }

  saveMatchDetails() {
    // When the match data is successfully saved, update the cached form data to
    // match the current matchState. This has the effect of resetting the 'isDirty' prop.
    this.props.onMatchDetailsSaved(this.props.matchState);
  }

  render() {
    const { matchId, ourTeam, oppTeam, ourTeamGender, onUpdateMatch } = this.props;
    return (
      <div>
        <a href={Urls.match_detail(matchId)} title="Match Details">
          <i className="fa fa-chevron-left g-mr-5 g-mb-20" />Back to match
        </a>
        <MultiStepForm
          ref={(c) => {
            this.form = c;
          }}
          slides={slides}
          bottomBarActions={
            <MutationButton
              label="Publish"
              mutate={onUpdateMatch}
              onSuccess={this.saveMatchDetails}
              getMutationInput={this.getMutationInput}
              buttonClass="btn u-btn-primary"
            />
          }
          panelClass={styles.formPanel}
        >
          <Result matchId={matchId} ourTeam={ourTeam} oppTeam={oppTeam} />
          <Appearances ourTeamGender={ourTeamGender} />
          <AwardWinners />
          <Report />
        </MultiStepForm>
      </div>
    );
  }
}

MatchEdit.propTypes = {
  matchId: PropTypes.number.isRequired,
  matchState: PropTypes.shape().isRequired,
  isDirty: PropTypes.bool.isRequired,
  ourTeamGender: PropTypes.string.isRequired,
  ourTeam: PropTypes.string.isRequired,
  oppTeam: PropTypes.string.isRequired,
  onUpdateMatch: PropTypes.func.isRequired,
  onMatchDetailsSaved: PropTypes.func.isRequired,
};

MatchEdit.defaultProps = {};

export default MatchEdit;
