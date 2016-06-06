(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('doctorCtrl', ['$scope', '$stateParams', '$http', 'util', '$state',
    function ($scope, $stateParams, $http, util, $state) {
      $scope.test = {};
      // jQuery modal plugin initialisation
      $(document).ready(function () {
        $('.modal-trigger').leanModal();
      });
      // jQuery datepicker initialisation
      $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 100 // Creates a dropdown of 15 years to control year
      });
      // get current user and retrieve his patients and texts
      util.getCurrentUser(function (user) {
        $scope.user = user;
        $scope.uid  = user.user.uid;
        // get current doctor's patients
        util.getUserPatients(user.user.patients, function (patients) {
          $scope.patients = patients.patients;
        });
        // get current doctor's texts
        util.getUserTexts(user.user.texts, function (texts) {
          $scope.texts = texts.texts;
        });
      }, null);

      /* finds the index of the object who's property KEY has value VALUE
       * in the array ARRAY */
      var findIndex = function (array, key, value) {
        var l = array.length,
          i   = 0;
        for (i; i < l; i += 1) {
          if (array[i][key] === value) { return i; }
        }
        return -1;
      };

      // go to patient with _id ID's profile page
      $scope.goToProfile = function (id) {
        $state.go('^.patientProfile', {pid: id});
      };

      // adds patient to current doctor
      $scope.addPatient = function () {
        var response = $http({
          method: 'PUT',
          url: '/api/add/user/' + $scope.user.user._id,
          data: {patient: $scope.newUser}
        });
        response.success(function (data, status, headers, config) {
          $scope.patients.push(data.patient);
        });
        response.error(function (data, status, headers, config) {
          console.log('Failed to add new patient');
        });
      };
      // add text to current doctor
      $scope.addText = function () {
        var response = $http({
          method: 'PUT',
          url: '/api/add/text/' + $scope.user.user._id,
          data: {text: $scope.newText}
        });
        response.success(function (data, status, headers, config) {
          $scope.texts.push(data.text);
        });
        response.error(function (data, status, headers, config) {
          console.log('Failed to add new text to doctor');
        });
      };

      // opens the modal containing the form to fill to send a test
      $scope.openSendTest = function (patient) {
        $scope.patient = patient;
        $('#send_test_modal').openModal();
      };

      // sends a test and closes the modal
      $scope.sendTest = function () {
        console.log("Sending test");
        console.log($scope.test);
        var response = $http({
          method: 'PUT',
          url: '/api/test/send',
          data: {
            test   : $scope.test,
            patient: $scope.patient._id,
            to     : $scope.patient.email,
            doctor : $scope.user.user._id
          }
        });
        response.error(function (data, status, headers, config) {
          console.log('Failed to send test to patient');
        });
      };

      // delete a user/text (from database)
      $scope.delete = function (array, key, id, type) {
        console.log('Deleting : ', id);
        var rp;
        if (type === 'patient') {
          rp = $http.get('/api/user/delete/' + $scope.user.user._id + '/' + id);
        } else {
          rp = $http.get('/api/delete/text/' + $scope.user.user._id + '/' + id);
        }
        // if patient/text successfully deleted from database
        rp.success(function (data, status, headers, config) {
          // remove patient/texet from current patients/texts
          array.splice(findIndex(array, key, id), 1);
        });
      };

      // edit patient information
      /* TODO: implement */
      $scope.edit = function (item) {
        console.log('Editing: ', item);
      };
      // sets the selected text in the send test form
      $scope.selectText = function (textID) {
        console.log('Selected text: ', textID);
        $scope.test.textID = textID;
      };
    }]);
}());
