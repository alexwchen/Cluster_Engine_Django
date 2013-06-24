$(document).ready(function(){
	
	// plot original data
	var plot1 = $.jqplot('ori_data', [[[2,2]]], 
    { 
      series:[ 
          {
            showLine:false, 
            markerOptions: { style:'x' }
          }
      ]
    });

	// Here Below is for documentation purpose
	//------------------------------------------------------

	/*
  	//var plot1 = $.jqplot ('ori_data', [[[1,1],[2,7]],[1,2,3,4,5]]);

	//var plot1 = $.jqplot ('clus_data', [[[2,2],[2,7]],[2,7],[9,9,9,9,9,9,9]]);
	
  	//var plot1 = $.jqplot ('obj_func', [[[3,3],[2,7]],[2,7],[1,3,4,6,8,2,5]]);
	a = {
      // Change our line width and use a diamond shaped marker.
      showLine:false, 
      markerOptions: { style:'dimaond' }
    };

    fuck=[ 
		a,
        {
          // Don't show a line, just show markers.
          // Make the markers 7 pixels with an 'x' style
          showLine:false, 
          markerOptions: { size: 7, style:"x" }
        },
        { 
          // Use (open) circlular markers.
          showLine:false, 

          markerOptions: { style:"circle" }
        }, 
        {
          // Use a thicker, 5 pixel line and 10 pixel
          // filled square markers.
          lineWidth:0, 
          markerOptions: { style:"filledSquare", size:10 }
        }
    ];
	
	
	
	  var plot1 = $.jqplot('ori_data', [ [[1,1],[2,2]], [[3,3],[4,4]], [[5,2],[5,4]], [[7,2],[7,4]] ], 
	    { 
	      title:'Line Style Options', 
	      // Series options are specified as an array of objects, one object
	      // for each series.
	      series:fuck
	    }
	  );
	*/
	
	//------------------------------------------------------
	
});
