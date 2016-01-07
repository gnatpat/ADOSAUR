var adosaur = angular.module('adosaur');

adosaur.config(function($stateProvider, $urlRouterProvider){

  $urlRouterProvider.otherwise('/home');

  $stateProvider
    .state('home', {
      url: "/home",
      templateUrl: "components/home/home.html",
      controller: "homeCtrl"
    })
    .state('doctorLogin', {
        url: "/doctorLogin",
        templateUrl: "components/realTime/realTime.html",
        controller: "realTimeCtrl"
    })
    .state('upload', {
        url: "/upload",
        templateUrl: "components/upload/upload.html",
        controller: "uploadCtrl"
    })

    .state('login', {
        url: "/login",
        templateUrl: "components/login/login.html",
        controller: "loginCtrl"
    })
})
