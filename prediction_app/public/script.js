$(document).ready(function() {

    promise = $.ajax({
        type:"GET",
        dataType:"text",
        url:"predictionData.csv",
        cache:false
    });

    promise.done(function(data){

        //Parse CSV File
        //split on new line
        var dataArr = data.split("\n");
        var recentArr = dataArr.slice(0, 100);
        //for each line in array
        $.each(recentArr,function(){
            if (this != "") {
                count = 0;
                //split files and create row
                var row = new String("");
                valArr = this.split(",");
                    row += "<tr>"
                
                $.each(valArr, function(){
                    count += 1;
                    newString = this.replace('"', '');
                    finalString = newString.replace('"', '');
                    row += "<td class='cell100 column" + count.toString() + "'>" + finalString +"</td>"
                });     

                    row += "</tr>"

                    //Add row to table
                    $('tbody').append(row);

            }

        });

    });
    // Run script if request fails
    promise.fail(function() {
       console.log('A failure ocurred');
    });

});