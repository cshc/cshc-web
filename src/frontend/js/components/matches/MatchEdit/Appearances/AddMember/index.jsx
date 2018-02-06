import { connect } from 'react-redux';
import { compose } from 'react-apollo';
import { addPlayerOption } from 'redux/actions/matchEditActions';
import AddMemberMutation from './addMemberMutation';
import AddMember from './AddMember';

const mapDispatchToProps = dispatch => ({
  onNewMemberAdded: (memberId, memberName) => {
    dispatch(addPlayerOption(memberId, memberName));
  },
});

export default compose(connect(undefined, mapDispatchToProps), AddMemberMutation)(AddMember);
