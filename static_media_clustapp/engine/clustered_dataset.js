$(document).ready(function(){	
	var plot1 = $.jqplot('clus_data', [[[2,2],[3,3]]], 
    { 
      series:[ 
          {
            showLine:false, 
            markerOptions: { style:'x' }
          }
      ]
    });
});
