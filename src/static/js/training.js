// Client-side logic for handling bulk addition of training sessions

$(() => {
  let repeatOptionInputs = $('input[type=radio][name=repeat_option]'),
    repeatCountWeeklyInput = $('#id_repeat_count_weekly'),
    repeatUntilWeeklyInput = $('#id_repeat_until_weekly'),
    repeatCountWeeklyGroup = $('#repeat-count-weekly-input-group'),
    repeatUntilWeeklyGroup = $('#repeat-until-weekly-input-group');
    repeatCountBiweeklyInput = $('#id_repeat_count_biweekly'),
    repeatUntilBiweeklyInput = $('#id_repeat_until_biweekly'),
    repeatCountBiweeklyGroup = $('#repeat-count-biweekly-input-group'),
    repeatUntilBiweeklyGroup = $('#repeat-until-biweekly-input-group');

  // Disable the repeat inputs based on which type of repeat is selected
  repeatOptionInputs.change(function () {
    repeatCountWeeklyInput.prop('disabled', this.value != 'MW');
    repeatUntilWeeklyInput.prop('disabled', this.value != 'UW');
    repeatCountBiweeklyInput.prop('disabled', this.value != 'MB');
    repeatUntilBiweeklyInput.prop('disabled', this.value != 'UB');

    if (this.value == 'N') {
      repeatCountWeeklyGroup.addClass('u-has-disabled-v1');
      repeatUntilWeeklyGroup.addClass('u-has-disabled-v1');
    } else if (this.value == 'MW') {
      repeatUntilWeeklyGroup.addClass('u-has-disabled-v1');
      repeatCountWeeklyGroup.removeClass('u-has-disabled-v1');
    } else if (this.value == 'UW') {
      repeatUntilWeeklyGroup.removeClass('u-has-disabled-v1');
      repeatCountWeeklyGroup.addClass('u-has-disabled-v1');
    } else if (this.value == 'MB') {
      repeatUntilBiweeklyGroup.addClass('u-has-disabled-v1');
      repeatCountBiweeklyGroup.removeClass('u-has-disabled-v1');
    } else if (this.value == 'UB') {
      repeatUntilBiweeklyGroup.removeClass('u-has-disabled-v1');
      repeatCountBiweeklyGroup.addClass('u-has-disabled-v1');
    }
  });
});
