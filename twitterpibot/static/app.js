
var app = angular.module( 'myApp', [] );

// hack to make angular and flask play nice
app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.controller( 'MainCtrl', function($scope, $http) {
    $scope.success = ""
    $scope.info = ""
    $scope.warning = ""
    $scope.error = ""

    $scope.actions = []
    $scope.identities = []
//    $scope.following = []
//    $scope.followinggraph = null

    $scope.getActions = function(){
      $http.get('actions').then(function(response) {
        $scope.actions = response.data.actions;
        });
    };
    $scope.getIdentities = function(){
      $http.get('identities').then(function(response) {
        $scope.identities = response.data.identities;

        });

    };
//    $scope.getFollowing = function(){
//      $http.get('following').then(function(response) {
//        $scope.following = response.data.following;
//        });
//    };
//    $scope.getExceptions = function(){
//      $http.get('exceptions').then(function(response) {
//        $scope.exceptions = response.data.exceptions;
//        });
//    };
//    $scope.getExceptionSummary = function(){
//      $http.get('exceptionsummary').then(function(response) {
//        $scope.exceptionsummary = response.data.exceptionsummary;
//        });
//    };
//    $scope.getFollowingGraph = function(){
//      $http.get('followinggraph').then(function(response) {
//        g = response.data.followinggraph;
//        $scope.followinggraph = g;
//        sys.graft(g);
//      });
//    };
//    $scope.getLists = function(){
//
//    };
//    $scope.getUser = function(){
//
//    };

    $scope.init = function(){
        $scope.getActions()
        $scope.getIdentities()
//        $scope.getExceptionSummary()
//        $scope.getExceptions()
//        $scope.getFollowing()
//        $scope.getFollowingGraph()


    };

    $scope.follow=function(identity_id, user_id){
        data = {
            "identity_id":identity_id,
            "user_id":user_id
        };
        $http.post('follow', data).then(function(response) {
            $scope.success = "follow " + identity_id + " " + user_id
        },function(response) {
            $scope.error = "follow " + identity_id + " " + user_id
        });
    };

    $scope.unfollow=function(identity_id, user_id){
        data = {
            "identity_id":identity_id,
            "user_id":user_id
        };
        $http.post('unfollow', data).then(function(response) {
            $scope.success = "unfollow " + identity_id + " " + user_id
        },function(response) {
            $scope.error = "unfollow " + identity_id + " " + user_id
        });
    };

    $scope.block=function(identity_id, user_id){
        data = {
            "identity_id":identity_id,
            "user_id":user_id
        };
        $http.post('block', data).then(function(response) {
            $scope.success = "block " + identity_id + " " + user_id
        },function(response) {
            $scope.error = "block " + identity_id + " " + user_id
        });
    };

    $scope.report=function(identity_id, user_id){
        data = {
            "identity_id":identity_id,
            "user_id":user_id
        };
        $http.post('report', data).then(function(response) {
            $scope.success = "report " + identity_id + " " + user_id
        },function(response) {
            $scope.error = "report " + identity_id + " " + user_id
        });
    };

    $scope.init()


});
