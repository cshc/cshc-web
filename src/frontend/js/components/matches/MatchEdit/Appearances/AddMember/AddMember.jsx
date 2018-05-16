import React from 'react';
import PropTypes from 'prop-types';
import { Gender } from 'util/constants';

/**
 * Sub-form for adding a new member. 
 * 
 * Note: the gender radio buttons are only displayed if the optional 
 * 'ourTeamGender' prop is provided and has a value 'Mixed'.
 */
class AddMember extends React.PureComponent {
  constructor(props) {
    super(props);
    // We only show the gender radio buttons if its a mixed match. Otherwise we
    // set the gender to the gender of the team.
    let gender;
    if (props.ourTeamGender === Gender.Ladies) gender = Gender.Female;
    else if (props.ourTeamGender === Gender.Mens) gender = Gender.Male;
    this.state = {
      updating: false,
      firstName: '',
      lastName: '',
      showGender: props.ourTeamGender === Gender.Mixed,
      gender,
    };
    this.updateGender = this.updateGender.bind(this);
    this.addMember = this.addMember.bind(this);
  }

  componentDidMount() {
    window.jQuery.HSCore.helpers.HSFocusState.init();
  }

  updateGender(ev) {
    this.setState({
      gender: ev.target.value,
    });
  }

  addMember() {
    // Prevent a duplicate addition
    if (this.state.updating) {
      return;
    }

    this.setState(
      {
        updating: true,
      },
      () => {
        this.props
          .onAddMember(this.state.firstName, this.state.lastName, this.state.gender)
          .then(({ data }) => {
            this.props.onNewMemberAdded(
              data.addMember.newMember.id,
              data.addMember.newMember.fullName,
            );
            this.props.onCancel();
          })
          .catch((error) => {
            this.setState({ updating: false });
          });
      },
    );
  }

  render() {
    const { onCancel } = this.props;
    const { firstName, lastName, showGender, gender, updating } = this.state;
    return (
      <div>
        <div className="d-flex g-bg-red g-color-white g-pa-10 g-mb-20">
          <i className="flex-0-auto fas fa-lg fa-exclamation-circle g-mr-10 g-mt-5" />
          <div className="flex-1">
            <div>
              Only add a new member if you&#39;re sure they aren&#39;t already in the list of
              members.
            </div>
            <div className="text-center g-pt-10">
              <button
                className="btn g-brd-white-opacity-0_8 g-brd-white--hover g-color-white-opacity-0_8 g-bg-red g-color-white--hover"
                onClick={onCancel}
              >
                I&#39;m not 100% sure...<br />I&#39;ll check again!
              </button>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-12 col-md-6 form-group g-mb-20">
            <label htmlFor="new-player-first-name" className="g-mb-10">
              First name
            </label>
            <div className="input-group g-brd-primary--focus">
              <div className="input-group-addon d-flex align-items-center g-bg-white g-color-gray-light-v1 rounded-0">
                <i className="icon-user" />
              </div>
              <input
                id="new-player-first-name"
                className="form-control form-control-md border-left-0 rounded-0 pl-0"
                type="text"
                value={firstName}
                onChange={(ev) => {
                  this.setState({ firstName: ev.target.value });
                }}
              />
            </div>
          </div>
          <div className="col-12 col-md-6 form-group g-mb-20">
            <label htmlFor="new-player-last-name" className="g-mb-10">
              Last name
            </label>
            <div className="input-group g-brd-primary--focus">
              <div className="input-group-addon d-flex align-items-center g-bg-white g-color-gray-light-v1 rounded-0">
                <i className="icon-user" />
              </div>
              <input
                id="new-player-last-name"
                className="form-control form-control-md border-left-0 rounded-0 pl-0"
                type="text"
                value={lastName}
                onChange={(ev) => {
                  this.setState({ lastName: ev.target.value });
                }}
              />
            </div>
          </div>
        </div>
        {showGender ? (
          <div className="d-flex">
            <label
              htmlFor="rb-male"
              className="form-check-inline u-check g-pl-25 ml-0 g-mr-25 g-mb-20"
            >
              <input
                id="rb-male"
                className="g-hidden-xs-up g-pos-abs g-top-0 g-left-0"
                name="rb-male"
                type="radio"
                value={Gender.Male}
                checked={gender === Gender.Male}
                onChange={this.updateGender}
              />
              <div className="u-check-icon-radio-v4 g-absolute-centered--y g-left-0 g-width-18 g-height-18">
                <i className="g-absolute-centered d-block g-width-10 g-height-10 g-bg-primary--checked" />
              </div>
              Male
            </label>
            <label
              htmlFor="rb-female"
              className="form-check-inline u-check g-pl-25 ml-0 g-mr-25 g-mb-20"
            >
              <input
                id="rb-female"
                className="g-hidden-xs-up g-pos-abs g-top-0 g-left-0"
                name="rb-female"
                type="radio"
                value={Gender.Female}
                checked={gender === Gender.Female}
                onChange={this.updateGender}
              />
              <div className="u-check-icon-radio-v4 g-absolute-centered--y g-left-0 g-width-18 g-height-18">
                <i className="g-absolute-centered d-block g-width-10 g-height-10 g-bg-primary--checked" />
              </div>
              Female
            </label>
          </div>
        ) : null}
        <button
          className="btn u-btn-outline-primary"
          title="Add a new member"
          disabled={updating || !firstName || !lastName || !gender}
          onClick={this.addMember}
        >
          <i className="fas fa-plus g-mr-5" />Add new member
        </button>
      </div>
    );
  }
}

AddMember.propTypes = {
  onAddMember: PropTypes.func.isRequired,
  onNewMemberAdded: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
  ourTeamGender: PropTypes.string.isRequired,
};

export default AddMember;
