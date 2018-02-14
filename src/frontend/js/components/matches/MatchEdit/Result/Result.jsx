import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Select from 'react-select';
import keys from 'lodash/keys';
import NumberInput from 'components/common/NumberInput';
import Match from 'models/match';
import { AltOutcome } from 'util/constants';
import styles from './style.scss';

export const ResultPropType = PropTypes.shape({
  ourScore: PropTypes.number,
  oppScore: PropTypes.number,
  ourHtScore: PropTypes.number,
  oppHtScore: PropTypes.number,
  altOutcome: PropTypes.string,
});

const MatchOutcome = Object.freeze({
  Cancelled: 'Cancelled',
  Postponed: 'Postponed',
  Abandoned: 'Abandoned',
  BYE: 'BYE',
  WalkoverWin: 'WalkoverWin',
  WalkoverLoss: 'WalkoverLoss',
});

const MatchOutcomeUtil = {
  [MatchOutcome.Cancelled]: { label: 'Cancelled', altOutcome: AltOutcome.Cancelled },
  [MatchOutcome.Postponed]: { label: 'Postponed', altOutcome: AltOutcome.Postponed },
  [MatchOutcome.Abandoned]: { label: 'Abandoned', altOutcome: AltOutcome.Abandoned },
  [MatchOutcome.BYE]: { label: 'BYE', altOutcome: AltOutcome.BYE },
  [MatchOutcome.WalkoverWin]: { label: 'Walkover (win)', altOutcome: AltOutcome.Walkover },
  [MatchOutcome.WalkoverLoss]: { label: 'Walkover (loss)', altOutcome: AltOutcome.Walkover },
};

/**
 * The 1st step of the Match Editing form.
 * 
 * The full-time and half-time scores can be entered here. Or an alternative
 * outcome can be selected. 
 * 
 * Note: This component includes logic to ensure the result is always interally 
 * consistent. i.e. walkover scores are enforced, scores are nullified if the match 
 * is cancelled/postponed/BYE, half-time scores can never be higher than full-time 
 * scores, etc.
 */
class Result extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      matchOutcome: undefined,
    };
    this.onChangeOurScore = this.onChangeOurScore.bind(this);
    this.onChangeOppScore = this.onChangeOppScore.bind(this);
    this.onChangeOurHtScore = this.onChangeOurHtScore.bind(this);
    this.onChangeOppHtScore = this.onChangeOppHtScore.bind(this);
    this.onChangeAltOutcome = this.onChangeAltOutcome.bind(this);
  }

  onChangeAltOutcome(matchOutcome) {
    this.setState({ matchOutcome });

    const altOutcomeResult = {
      altOutcome: matchOutcome ? MatchOutcomeUtil[matchOutcome].altOutcome : undefined,
    };
    switch (matchOutcome) {
      case MatchOutcome.Postponed:
      case MatchOutcome.Cancelled:
      case MatchOutcome.BYE:
        altOutcomeResult.ourScore = undefined;
        altOutcomeResult.oppScore = undefined;
        altOutcomeResult.ourHtScore = undefined;
        altOutcomeResult.oppHtScore = undefined;
        break;
      case MatchOutcome.WalkoverWin:
        altOutcomeResult.ourScore = Match.WALKOVER_SCORE_W2;
        altOutcomeResult.oppScore = Match.WALKOVER_SCORE_L;
        altOutcomeResult.ourHtScore = undefined;
        altOutcomeResult.oppHtScore = undefined;
        break;
      case MatchOutcome.WalkoverLoss:
        altOutcomeResult.ourScore = Match.WALKOVER_SCORE_L;
        altOutcomeResult.oppScore = Match.WALKOVER_SCORE_W2;
        altOutcomeResult.ourHtScore = undefined;
        altOutcomeResult.oppHtScore = undefined;
        break;
      case MatchOutcome.Abandoned:
      default:
        altOutcomeResult.ourScore = altOutcomeResult.ourScore || 0;
        altOutcomeResult.oppScore = altOutcomeResult.oppScore || 0;
        altOutcomeResult.ourHtScore = altOutcomeResult.ourHtScore || 0;
        altOutcomeResult.oppHtScore = altOutcomeResult.oppHtScore || 0;
        break;
    }
    this.props.onUpdateResult({
      ...this.props.result,
      ...altOutcomeResult,
    });
  }

  onChangeOurScore(ourScore) {
    if (ourScore === undefined) return;
    this.props.onUpdateResult({
      ...this.props.result,
      ourScore,
      ourHtScore: Math.min(this.props.result.ourHtScore, ourScore),
    });
  }

  onChangeOppScore(oppScore) {
    if (oppScore === undefined) return;
    this.props.onUpdateResult({
      ...this.props.result,
      oppScore,
      oppHtScore: Math.min(this.props.result.oppHtScore, oppScore),
    });
  }

  onChangeOurHtScore(ourHtScore) {
    if (ourHtScore === undefined) return;
    this.props.onUpdateResult({
      ...this.props.result,
      ourHtScore,
      ourScore: Math.max(this.props.result.ourScore, ourHtScore),
    });
  }

  onChangeOppHtScore(oppHtScore) {
    if (oppHtScore === undefined) return;
    this.props.onUpdateResult({
      ...this.props.result,
      oppHtScore,
      oppScore: Math.max(this.props.result.oppScore, oppHtScore),
    });
  }

  render() {
    const { ourTeam, oppTeam, result: { ourScore, ourHtScore, oppScore, oppHtScore } } = this.props;
    const { matchOutcome } = this.state;
    const scoreDisplayClass = classnames('d-flex text-center', styles.score, {});
    const altOutcomeOptions = keys(MatchOutcomeUtil).map(key => ({
      value: key,
      label: MatchOutcomeUtil[key].label,
    }));
    const disableScores = matchOutcome && matchOutcome !== MatchOutcome.Abandoned;
    return (
      <div className="card-block">
        <div className="d-flex flex-column align-items-center">
          <div className="d-flex justify-content-center align-items-center g-font-size-18 g-font-size-24--md g-font-size-35--lg">
            <div
              className={`${styles.teamName} d-flex justify-content-end align-items-center text-right g-pr-4`}
            >
              <div className="text-center">{ourTeam}</div>
            </div>
            <div className={scoreDisplayClass}>
              <NumberInput
                value={ourScore}
                disabled={disableScores}
                valueClass="g-bg-primary g-color-white"
                onChangeValue={this.onChangeOurScore}
              />
              <NumberInput
                value={oppScore}
                disabled={disableScores}
                valueClass="g-bg-primary g-color-white"
                onChangeValue={this.onChangeOppScore}
              />
            </div>
            <div
              className={`${styles.teamName} d-flex justify-content-start align-items-center text-right g-pl-4`}
            >
              <div className="text-center">{oppTeam}</div>
            </div>
          </div>
          <div className="g-font-weight-600">Half-time:</div>
          <div className="d-flex justify-content-center align-items-center g-font-size-18 g-font-size-24--md g-font-size-35--lg">
            <div className={scoreDisplayClass}>
              <NumberInput
                value={ourHtScore}
                disabled={disableScores}
                valueClass="g-bg-gray-dark-v5 g-color-white"
                onChangeValue={this.onChangeOurHtScore}
              />
              <NumberInput
                value={oppHtScore}
                disabled={disableScores}
                valueClass="g-bg-gray-dark-v5 g-color-white"
                onChangeValue={this.onChangeOppHtScore}
              />
            </div>
          </div>
        </div>
        <div className="g-my-20 row justify-content-center">
          {matchOutcome ? (
            <div className="col-12 col-md-3">
              <Select
                menuContainerStyle={{ zIndex: 999 }}
                className={`${styles.altOutcomeSelect} g-width-100x`}
                options={altOutcomeOptions}
                simpleValue
                clearable
                pageSize={altOutcomeOptions.length}
                name="alt-outcome-select"
                value={matchOutcome}
                onChange={this.onChangeAltOutcome}
              />
            </div>
          ) : (
            <button
              className="btn btn-link"
              onClick={() => {
                this.onChangeAltOutcome(MatchOutcome.Cancelled);
              }}
            >
              No result?
            </button>
          )}
        </div>
      </div>
    );
  }
}

Result.propTypes = {
  ourTeam: PropTypes.string.isRequired,
  oppTeam: PropTypes.string.isRequired,
  result: ResultPropType.isRequired,
  onUpdateResult: PropTypes.func.isRequired,
};

export default Result;
