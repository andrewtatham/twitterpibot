
var app = angular.module( 'myApp', [] );

// hack to make angular and flask play nice
app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.controller( 'MainCtrl', function($scope, $http) {
    $scope.success = "";
    $scope.info = "";
    $scope.warning = "";
    $scope.error = "";

    $scope.actions = [];
    $scope.identities =  [];



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
    $scope.getIdentity = function(id_str){
        $http.get('identity/' + id_str).then(function(response) {
            $scope.identities.forEach(function(identity, index){
                if (identity.id_str == id_str){
                    $scope.identities[index] = response.data.identity;
                };
            });
        });
    };



    $scope.init = function(){
        $scope.getActions()
        $scope.getIdentities()
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
