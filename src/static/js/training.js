// Client-side logic for handling bulk addition of training sessions

$(() => {
  let repeatOptionInputs = $('input[type=radio][name=repeat_option]'),
    repeatCountInput = $('#id_repeat_count'),
    repeatUntilInput = $('#id_repeat_until'),
    repeatCountGroup = $('#repeat-count-input-group'),
    repeatUntilGroup = $('#repeat-until-input-group');

  // Disable the repeat inputs based on which type of repeat is selected
  repeatOptionInputs.change(function () {
    repeatCountInput.prop('disabled', this.value != 'M');
    repeatUntilInput.prop('disabled', this.value != 'U');

    if (this.value == 'N') {
      repeatCountGroup.addClass('u-has-disabled-v1');
      repeatUntilGroup.addClass('u-has-disabled-v1');
    } else if (this.value == 'M') {
      repeatUntilGroup.addClass('u-has-disabled-v1');
      repeatCountGroup.removeClass('u-has-disabled-v1');
    } else if (this.value == 'U') {
      repeatUntilGroup.removeClass('u-has-disabled-v1');
      repeatCountGroup.addClass('u-has-disabled-v1');
    }
  });
});
