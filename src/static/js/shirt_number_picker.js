$(document).ready(function() {
  var selectedShirtNumber = null;
  var csrfToken = CSHC_CONFIG.csrfToken;
  var maxShirtNumber = CSHC_CONFIG.maxShirtNumber || 199; // Default to 199 if not set or invalid

  // Function to show a generic feedback modal
  function showFeedbackModal(type, message) {
    var modalId = (type === 'success') ? '#feedbackSuccessModal' : '#feedbackErrorModal';
    var modalBodyId = (type === 'success') ? '#feedbackSuccessModalBody' : '#feedbackErrorModalBody';
    $(modalBodyId).text(message);
    $(modalId).modal('show');
  }

  // Helper function to reset the assign button and selected number display
  function resetAssignState() {
    selectedShirtNumber = null;
    $('#selectedNumberDisplay').text('None');
    $('#assignShirtNumberBtn').prop('disabled', true);
  }

  // Helper function to reset the manual check button to its default state
  function resetCheckButtonState() {
    var $checkBtn = $('#checkManualShirtNumberBtn');
    var $checkIcon = $('#checkIcon');
    var $checkText = $('#checkText');
    var $inputGroup = $('#manualShirtNumberInputGroup');

    $checkBtn.removeClass('u-btn-success u-btn-danger').addClass('u-btn-outline-primary');
    $checkIcon.removeClass('fa-check fa-times fa-spinner fa-spin').addClass('fa-search');
    $checkText.text('Check');
    $inputGroup.removeClass('border border-success border-danger'); // Remove border feedback
  }

  // Event listener for when the modal is about to be shown
  $('#requestShirtNumberModal').on('show.bs.modal', function (e) {
    // Reset modal state
    var $container = $('#availableShirtNumbersContainer');
    $container.html('<div class="col-12 text-center"><p class="text-muted" id="loadingNumbers">Loading available numbers...</p></div>');
    $('#manualShirtNumberInput').val(''); // Clear manual input
    resetCheckButtonState(); // Reset check button and input group
    resetAssignState();

    // Fetch available numbers via AJAX
    $.ajax({
      url: CSHC_CONFIG.urls.availableShirtNumbers,
      method: 'GET',
      dataType: 'json',
      success: function(data) {
        var $container = $('#availableShirtNumbersContainer');
        $container.empty(); // Clear loading message

        if (data.available_numbers && data.available_numbers.length > 0) {
          $.each(data.available_numbers, function(index, number) {
            var numberOptionHtml = `
              <div class="col-sm-2 col-4 g-mb-10 text-center">
                <span class="u-label u-label--sm u-label--rounded g-px-15 g-py-10 g-cursor-pointer g-bg-gray-light-v4 g-color-gray-dark-v4 shirt-number-option" data-number="${number}">${number}</span>
              </div>
            `;
            $container.append(numberOptionHtml);
          });
        } else {
          $container.html('<div class="col-12 text-center"><p class="text-muted">No available shirt numbers found at this time for your gender.</p></div>');
        }
      },
      error: function(xhr, status, error) {
        var $container = $('#availableShirtNumbersContainer');
        $container.empty();
        var errorMessage = 'Error loading numbers. Please try again later.';
        if (xhr.responseJSON && xhr.responseJSON.error) {
          errorMessage = xhr.responseJSON.error;
        }
        $container.html(`<div class="col-12 text-center"><p class="text-danger">${errorMessage}</p></div>`);
        console.error("Error fetching available shirt numbers:", error, xhr.responseText);
      }
    });
  });

  // Handle selection of a shirt number from the list
  $('#availableShirtNumbersContainer').on('click', '.shirt-number-option', function() {
    // Clear manual input and reset its button state
    $('#manualShirtNumberInput').val('');
    resetCheckButtonState(); // Reset check button and input group

    // Remove selection styling from all options
    $('.shirt-number-option').removeClass('g-bg-primary g-color-white').addClass('g-bg-gray-light-v4 g-color-gray-dark-v4');
    // Apply selection styling to the clicked option
    $(this).removeClass('g-bg-gray-light-v4 g-color-gray-dark-v4').addClass('g-bg-primary g-color-white');

    selectedShirtNumber = $(this).data('number');
    $('#selectedNumberDisplay').text(selectedShirtNumber);
    $('#assignShirtNumberBtn').prop('disabled', false); // Enable the assign button
  });

  // Handle input in the manual text field
  $('#manualShirtNumberInput').on('keyup', function() {
    // Clear selection from the list
    $('.shirt-number-option').removeClass('g-bg-primary g-color-white').addClass('g-bg-gray-light-v4 g-color-gray-dark-v4');
    resetCheckButtonState(); // Reset check button to "Check" visual state and remove border
    resetAssignState(); // Disable assign button until checked
  });

  // Handle "Check" button click for manual input
  $('#checkManualShirtNumberBtn').on('click', function() {
    var manualInput = $('#manualShirtNumberInput').val().trim();
    resetAssignState(); // Reset assign state
    resetCheckButtonState(); // Reset visual state before starting new check

    if (!manualInput) {
      showFeedbackModal('error', 'Please enter a number to check.');
      return;
    }

    var num = parseInt(manualInput);
    if (isNaN(num) || num <= 0 || num > maxShirtNumber) {
      showFeedbackModal('error', `Please enter a valid number between 1 and ${maxShirtNumber}.`);
      return;
    }

    var $checkBtn = $('#checkManualShirtNumberBtn');
    var $checkIcon = $('#checkIcon');
    var $checkText = $('#checkText');
    var $inputGroup = $('#manualShirtNumberInputGroup');

    // Do NOT disable the button, just change its appearance to indicate checking
    $checkIcon.removeClass('fa-search fa-check fa-times').addClass('fa-spinner fa-spin'); // Show spinner
    $checkText.text('Checking...');
    $checkBtn.removeClass('u-btn-outline-primary u-btn-success u-btn-danger'); // Remove all color classes

    // Make AJAX call to check specific number availability
    $.ajax({
      url: CSHC_CONFIG.urls.checkShirtNumberAvailability,
      method: 'GET',
      data: { 'shirt_number': num },
      dataType: 'json',
      success: function(data) {
        $checkIcon.removeClass('fa-spinner fa-spin'); // Remove spinner

        if (data.is_available) {
          $checkBtn.addClass('u-btn-success');
          $checkIcon.addClass('fa-check');
          $checkText.text('Available');
          $inputGroup.addClass('border border-success'); // Green border
          selectedShirtNumber = num;
          $('#selectedNumberDisplay').text(selectedShirtNumber);
          $('#assignShirtNumberBtn').prop('disabled', false); // Enable assign button
        } else {
          $checkBtn.addClass('u-btn-danger');
          $checkIcon.addClass('fa-times');
          $checkText.text('Taken');
          $inputGroup.addClass('border border-danger'); // Red border
        }
      },
      error: function(xhr, status, error) {
        $checkIcon.removeClass('fa-spinner fa-spin').addClass('fa-times'); // Show error icon
        $checkBtn.addClass('u-btn-danger');
        $checkText.text('Error');
        $inputGroup.addClass('border border-danger'); // Red border

        var errorMessage = 'Error checking availability. Please try again.';
        if (xhr.responseJSON && xhr.responseJSON.error) {
          errorMessage = xhr.responseJSON.error;
        }
        showFeedbackModal('error', errorMessage);
        console.error("Error checking manual shirt number:", error, xhr.responseText);
      }
    });
  });

  // Handle assignment of the selected shirt number
  $('#assignShirtNumberBtn').on('click', function() {
    if (selectedShirtNumber === null) {
      showFeedbackModal('error', 'Please select or check an available shirt number first.');
      return;
    }

    var $btn = $(this);
    $btn.prop('disabled', true).text('Assigning...'); // Disable button and show loading text

    $.ajax({
      url: CSHC_CONFIG.urls.assignShirtNumber,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ 'shirt_number': selectedShirtNumber }),
      headers: {
        'X-CSRFToken': csrfToken
      },
      success: function(data) {
        $('#requestShirtNumberModal').modal('hide'); // Close the selection modal
        showFeedbackModal('success', data.message); // Show success modal

        // Reload the page after the success modal is hidden
        $('#feedbackSuccessModal').on('hidden.bs.modal', function (e) {
          location.reload();
        });
      },
      error: function(xhr, status, error) {
        var errorMessage = 'An unknown error occurred.';
        if (xhr.responseJSON && xhr.responseJSON.error) {
          errorMessage = xhr.responseJSON.error;
        } else if (error) {
          errorMessage = error;
        }
        showFeedbackModal('error', 'Error assigning shirt number: ' + errorMessage); // Show error modal
        console.error("Error assigning shirt number:", error, xhr.responseText);
        $btn.prop('disabled', false).text('Assign Selected Number'); // Re-enable button
      }
    });
  });
});
