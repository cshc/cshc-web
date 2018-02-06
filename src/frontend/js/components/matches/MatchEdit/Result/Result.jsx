import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Select from 'react-select';
import keys from 'lodash/keys';
import AccordionCard from 'components/common/Accordion/AccordionCard';
import NumberInput from 'components/common/NumberInput';
import { AccordionId } from '../util';
import StatusIcon from '../StatusIcon';
import Errors from '../Errors';
import { AltOutcome } from 'util/constants';
import styles from './style.scss';

const areScoresEnabled = altOutcome =>
  !altOutcome || altOutcome === AltOutcome.Abandoned || altOutcome === AltOutcome.Walkover;

class Result extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      ftDisplay: false,
    };
    this.onChangeScore = this.onChangeScore.bind(this);
    this.onChangeAltOutcome = this.onChangeAltOutcome.bind(this);
  }

  onChangeAltOutcome(altOutcome) {
    const altOutcomeResult = {
      altOutcome,
    };
    // Clear scores if they are not relevant
    if (!areScoresEnabled(altOutcome)) {
      altOutcomeResult.ourScore = undefined;
      altOutcomeResult.oppScore = undefined;
      altOutcomeResult.ourHtScore = undefined;
      altOutcomeResult.oppHtScore = undefined;
    } else {
      // Set default score values to something sensible if they are relevant
      altOutcomeResult.ourScore = altOutcomeResult.ourScore || 0;
      altOutcomeResult.oppScore = altOutcomeResult.oppScore || 0;
      altOutcomeResult.ourHtScore =
        altOutcome === AltOutcome.Walkover ? undefined : altOutcomeResult.ourHtScore || 0;
      altOutcomeResult.oppHtScore =
        altOutcome === AltOutcome.Walkover ? undefined : altOutcomeResult.oppHtScore || 0;
    }
    this.props.onUpdateResult({
      ...this.props.result,
      ...altOutcomeResult,
    });
  }

  onChangeScore(score, isOurs) {
    const scoreResult = {};
    // Update the appropriate score value
    if (this.state.ftDisplay) {
      if (isOurs) {
        scoreResult.ourScore = score;
      } else {
        scoreResult.oppScore = score;
      }
    } else if (isOurs) {
      scoreResult.ourHtScore = score;
    } else {
      scoreResult.oppHtScore = score;
    }
    this.props.onUpdateResult({
      ...this.props.result,
      ...scoreResult,
    });
  }

  render() {
    const {
      ourTeam,
      oppTeam,
      result: { ourScore, ourHtScore, oppScore, oppHtScore, altOutcome, errors },
    } = this.props;
    const { ftDisplay } = this.state;
    const scoresEnabled = areScoresEnabled(altOutcome);
    const btnClassnames = 'btn rounded-0 g-py-2 g-px-4 g-mx-2';
    const topDivClass = classnames('d-flex justify-content-center g-pb-10', {
      'g-opacity-0_3': !scoresEnabled,
    });
    const htClass = classnames(btnClassnames, {
      'btn-secondary': !ftDisplay,
      'u-btn-outline-lightgray': ftDisplay,
    });
    const ftClass = classnames(btnClassnames, {
      'u-btn-primary': ftDisplay,
      'u-btn-outline-lightgray': !ftDisplay,
    });
    const scoreDisplayClass = classnames('d-flex text-center', styles.score, {
      'g-opacity-0_3': !scoresEnabled,
    });
    const scoreValueClass = ftDisplay
      ? 'g-bg-primary g-color-white'
      : 'g-bg-gray-dark-v5 g-color-white';
    const altOutcomeOptions = keys(AltOutcome).map(i => ({
      value: i,
      label: i,
    }));
    return (
      <AccordionCard
        className={styles.resultCard}
        cardId="result"
        isOpen
        title="Result"
        accordionId={AccordionId}
        rightIcon={<StatusIcon error={errors.length > 0} />}
      >
        <div className={topDivClass}>
          <button
            className={htClass}
            onClick={() => {
              this.setState({ ftDisplay: false });
            }}
          >
            H/T
          </button>
          <button
            className={ftClass}
            onClick={() => {
              this.setState({ ftDisplay: true });
            }}
          >
            F/T
          </button>
        </div>
        <div className="d-flex justify-content-center align-items-center g-font-size-18 g-font-size-24--md g-font-size-35--lg">
          <div
            className={`${styles.teamName} d-flex justify-content-end align-items-center text-right g-pr-4`}
          >
            <div className="text-center">{ourTeam}</div>
          </div>
          <div className={scoreDisplayClass}>
            <NumberInput
              disabled={!scoresEnabled}
              value={ftDisplay ? ourScore : ourHtScore}
              valueClass={scoreValueClass}
              onChangeValue={(value) => {
                this.onChangeScore(value, true);
              }}
            />
            <NumberInput
              disabled={!scoresEnabled}
              value={ftDisplay ? oppScore : oppHtScore}
              valueClass={scoreValueClass}
              onChangeValue={(value) => {
                this.onChangeScore(value, false);
              }}
            />
          </div>
          <div
            className={`${styles.teamName} d-flex justify-content-start align-items-center text-right g-pl-4`}
          >
            <div className="text-center">{oppTeam}</div>
          </div>
        </div>
        <div className="d-flex justify-content-center g-py-10">
          <Select
            menuContainerStyle={{ zIndex: 999 }}
            className="g-width-130"
            placeholder="No result?"
            options={altOutcomeOptions}
            simpleValue
            clearable
            name="alt-outcome-select"
            value={altOutcome}
            onChange={this.onChangeAltOutcome}
          />
        </div>
        <Errors errors={errors} />
      </AccordionCard>
    );
  }
}

Result.propTypes = {
  ourTeam: PropTypes.string.isRequired,
  oppTeam: PropTypes.string.isRequired,
  result: PropTypes.shape({
    errors: PropTypes.array,
    ourScore: PropTypes.number,
    oppScore: PropTypes.number,
    ourHtScore: PropTypes.number,
    oppHtScore: PropTypes.number,
    altOutcome: PropTypes.string,
  }).isRequired,
  onUpdateResult: PropTypes.func.isRequired,
};

export default Result;
