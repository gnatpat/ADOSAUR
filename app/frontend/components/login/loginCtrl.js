(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('loginCtrl', ['$scope', 'util', '$location', 'Flash', '$state',
    function ($scope, util, $location, Flash, $state) {
      // if user already has a current session then redirect him to his home page
      util.getCurrentUser(function (user) {
        if (user.found) {
          $state.go('doctor', {uid: user.user.uid});
        }
      }, function (data) {
        console.log('Ajax request failed');
      });

      var err = $location.search().err,
        errMsg = "";
      if (err === "1") {
        errMsg = "This username does not exist, please try again";
        Flash.create('danger', errMsg);
      }
      if (err === "2") {
        errMsg = "<strong>Wrong</strong> password, please try again";
        Flash.create('danger', errMsg);
      }
    }]);
}());
