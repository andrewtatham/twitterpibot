.factory("talksService", function(Restangular){
    return {
        getTalks: function(){
            return Restangular.all("talks").getList();
        },
    };
})