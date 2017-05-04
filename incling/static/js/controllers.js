app.controller('controller', [
    '$scope', '$q', '$resource',
    function($scope, $q, $resource) {

        var school_resource = $resource("/api/v0/school/:uuid").query();
        $scope.schools = school_resource;
        $scope.classrooms = {};
        $q.all([school_resource.$promise]).then(
            function([schools]){
                for (var i=0; i<schools.length; i++){
                    var school = schools[i].name
                    $scope.classrooms[school] = {};
                    $scope.classrooms[school]['school'] = school;
                    $scope.classrooms[school]['classrooms_selected'] = {}
                    $scope.classrooms[school]['class_data'] = {}
                    $scope.classrooms[school]['classroom_data'] = $resource(
                        "/api/v0/classroom/:uuid?school__name=" + school
                    ).query()
                };
            }, $scope
        );
        $scope.select = function(school, classroom) {
            // toggle selected:
            if ((angular.isUndefined($scope.classrooms[school]['classrooms_selected'][classroom])) ||
                ($scope.classrooms[school]['classrooms_selected'][classroom] === false)) {
                    $scope.classrooms[school]['classrooms_selected'][classroom] = true;
            } else {
                $scope.classrooms[school]['classrooms_selected'][classroom] = false;
            };
        };
    }
]);
