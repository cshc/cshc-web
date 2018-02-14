import { connect } from 'react-redux';
import { compose } from 'react-apollo';
import deepEqual from 'deep-equal';
import { saveFormState } from 'redux/actions/formActions';
import UpdateMatchMutation from './updateMatchMutation';
import MatchEdit from './MatchEdit';

const mapStateToProps = state => ({
  matchState: state.matchState,
  isDirty: !deepEqual(state.matchState, state.form.matchState),
});

const mapDispatchToProps = dispatch => ({
  onMatchDetailsSaved: (matchState) => {
    dispatch(saveFormState('matchState', matchState));
  },
});

export default compose(connect(mapStateToProps, mapDispatchToProps), UpdateMatchMutation)(
  MatchEdit,
);
