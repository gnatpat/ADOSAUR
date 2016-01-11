var adosaur = angular.module('adosaur');

adosaur.config(function ($stateProvider, $urlRouterProvider) {
  'use strict';
  $urlRouterProvider.otherwise('/home');

  $stateProvider
    .state('home', {
      url: "/home",
      templateUrl: "components/home/home.html",
      controller: "homeCtrl"
    })

    .state('upload', {
      url: "/upload",
      templateUrl: "components/upload/upload.html",
      controller: "uploadCtrl"
    })

    .state('login', {
      url: "/login?err",
      templateUrl: "components/login/login.html",
      controller: "loginCtrl"
    })

    .state('logout', {
      url: "/logout",
      controller: "logoutCtrl"
    })

    .state('test', {
      url: "/test/:token",
      templateUrl: "components/test/test.html",
      controller: "testCtrl"
    })

    .state('doctor', {
      url: "/doctor/{uid}",
      templateUrl: "components/doctor/doctor.html",
      controller: "doctorCtrl"
    })

    .state('doctor.patients', {
      url: "patients/{uid}",
      templateUrl: "components/doctor/patientsPART.html",
      controller: "doctorCtrl"
    })

    .state('doctor.texts', {
      url: "texts/{uid}",
      templateUrl: "components/doctor/textsPART.html",
      controller: "doctorCtrl"
    });
});
