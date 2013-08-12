//-------------------------------------
// Author: Muneeb Ali - http://muneeb.org
// Modified from examples at http://stripe.com/docs/
//-------------------------------------

var stripeResponseHandler = function(status, response) {
  var $form = $('#payment-form');

  if (response.error) {
    // Show the errors on the form
    $form.find('.payment-errors').text(response.error.message);
    $form.find('button').prop('disabled', false);
  } 
  else {
    // Token contains id, last4, and card type
    var token = response.id;
    
    // Insert the token into the form so it gets submitted to the server
    $form.append($('<input type="hidden" name="stripeToken" />').val(token));
    // And submit
    $form.get(0).submit();
  }
};

//-------------------------------------
jQuery(function($) {
  $('#payment-form').submit(function(event) {
    var $form = $(this);

    // Disable the submit button to prevent repeated clicks
    $form.find('button').prop('disabled', true);

    Stripe.createToken($form, stripeResponseHandler);

    // Prevent the form from submitting with the default action
    return false;
  });
});

//-------------------------------------
// Popualte the forms with test data
var test_data = {

  //-----------------------------------------
  load: function() {

    $('#payment-form').find('input[name="email"]').val('customer@domain.com');
    $('#payment-form').find('input[data-stripe="number"]').val('4242424242424242');
    $('#payment-form').find('input[data-stripe="cvc"]').val('111');
    $('#payment-form').find('input[data-stripe="exp-month"]').val('12');
    $('#payment-form').find('input[data-stripe="exp-year"]').val('2015');

    $('#recurring-form').find('input[name="email"]').val('customer@domain.com');
  }
};