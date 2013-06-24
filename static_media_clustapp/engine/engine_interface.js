$(document).ready(function(){
	
	// handle first appearence of the selection tab
	$('#default_tab').addClass('graph_tabs_top_menu_options_selected');	
	$('.graph_content').css('display','none');
	$('#Original_Dataset').css('display','block');
	
});

/*******************************************************
**			Hover Effects
**				Algorithm Selectors
**				Graph Display Option
********************************************************/

// buttons
$('.ok_button_outter_start').mouseenter(function () {
	$(this).css('background-color', '#aff0cb');	
	
});
$('.ok_button_outter_start').mouseleave(function () {
	$(this).css('background-color', 'white');
});

$('.ok_button_outter_stop').mouseenter(function () {
	$(this).css('background-color', '#f0c0af');	
	
});
$('.ok_button_outter_stop').mouseleave(function () {
	$(this).css('background-color', 'white');
});

$('.ok_button_outter_download').mouseenter(function () {
	$(this).css('background-color', '#f0d7af');	
	
});
$('.ok_button_outter_download').mouseleave(function () {
	$(this).css('background-color', 'white');
});

$('.ok_button_outter_share').mouseenter(function () {
	$(this).css('background-color', '#f0d7af');	
	
});
$('.ok_button_outter_share').mouseleave(function () {
	$(this).css('background-color', 'white');
});

// algorithm drowndown title
$('.dropdown_title').mouseenter(function () {
	$(this).css('background-color', '#fcae14');
});
$('.dropdown_title').mouseleave(function () {
	$(this).css('background-color', 'white');
});

// algorithm dropdown option
$('.dropdown_option_outter').mouseenter(function () {
	$(this).css('background-color', '#fcae14');	
});
$('.dropdown_option_outter').mouseleave(function () {
	$(this).css('background-color', '#f0d7af');
});

// graph display selector
$('.dataset_display_method_option').mouseenter(function () {
	$(this).css('background-color', '#f0d7af');	
});
$('.dataset_display_method_option').mouseleave(function () {
	$(this).css('background-color', 'white');
});


/*******************************************************
**			Select Effects
**				Algorithm Selectors
**				Data Selectors
** 			Also do a lot of height adjusting, so the site will look nice
********************************************************/

// quick hack, change if find better way to do this toggl
var global_state_dropdown_algo = 1;
var global_state_dropdown_data = 1;

//select an algorithm or dataset from all the options
$('.dropdown_option_outter').click(function () {
	$(this).closest('.dropdown_frame').children('.dropdown_container').fadeOut();
	global_state_dropdown_algo=1;
		
	var name = $(this).text();
	$(this).closest('.dropdown_frame').children('.dropdown_title').children('.dropdown_title_inner').text(name);		
	
	var category = $(this).parent().parent().find('.dropdown_label').text()
	
	if(category=="Dataset:"){
	    $.get("/engine/get_parameter_given_algorithm_or_dataset_name/", {'algo':name.replace(/^\s*|\s*$/g,'')}, function(data)
	    {
			// count graph tab distance to top
			var para_count = 0;
		
			// remove whatever it is in parameter container
			$('.parameters_options_text_box').each(function () {
				var para_type = $(this).parent().attr('id');
				if (para_type=='data_para_container'){
					$(this).remove();
				}
				// do the count on the other category: in this case -> Algorithm
				else if(para_type=='algo_para_container'){
					para_count++;
				}
			});	
			
			
			// plug in all the parameter
			var paras = JSON.parse(data);
			for (para in paras)
			{
				para_count++;								
				var para_name = para;
				var para_default = paras[para];
				var para_block = 
					"<div id='data_para_box' class='parameters_options_text_box'>" +
						"<div class='parameters_options_label_box'>" + para_name + "</div>" +
						"<input class='parameters_options_input_box' type='text' name='" + para_name + "' value='" + para_default +"' />" +						
					"</div>";
				var param_frame = $('#data_para_container');
		        $(para_block).prependTo(param_frame);								
			}
			
			// change graph margin top, so the graph will be at the correct place
			$('.graph_tabs').css('margin-top', String(340+40*para_count));
			
		});
		
		

	}
	
	else if(category=="Algorithm:"){

		// update parameters
		// send a "GET" to server
	    $.get("/engine/get_parameter_given_algorithm_or_dataset_name/", {'algo':name.replace(/^\s*|\s*$/g,'')}, function(data)
	    {
			// count graph tab distance to top
			var para_count = 0;
		
			// remove whatever it is in parameter container
			$('.parameters_options_text_box').each(function () {
				var para_type = $(this).parent().attr('id');
				if (para_type=='algo_para_container'){
					$(this).remove();
				}
				// do the count on the other category: in this case -> Dataset
				else if(para_type=='data_para_container'){
					para_count++;
				}
			});	
			
			
			// plug in all the parameter
			var paras = JSON.parse(data);
			for (para in paras)
			{
				para_count++;
			
				var para_name = para;
				var para_default = paras[para];
				var para_block = 
					"<div class='parameters_options_text_box'>" +
						"<div class='parameters_options_label_box'>" + para_name + "</div>" +
						"<input class='parameters_options_input_box' type='text name='" + para_name + "' value='" + para_default +"' />" +
					"</div>";
				var param_frame = $('#algo_para_container');
		        $(para_block).prependTo(param_frame);								
			}
			
			// change graph margin top, so the graph will be at the correct place
			$('.graph_tabs').css('margin-top', String(340+40*para_count));
			
		});

	}


	
});

// clicking for algorithm/dataset dropdown
$('.dropdown_title').click(function () {
	if (global_state_dropdown_algo==1){
		$(this).closest('.dropdown_frame').children('.dropdown_container').fadeIn();		
		global_state_dropdown_algo=1-global_state_dropdown_algo;
	}
	else{
		$(this).closest('.dropdown_frame').children('.dropdown_container').fadeOut();
		global_state_dropdown_algo=1-global_state_dropdown_algo;		
	}
});


/*******************************************************
**			Graph Tabs 
**				Tabs Selection
********************************************************/
$('.graph_tabs_top_menu_options').click(function () {

	// dealing tabs switching
	var str = $(this).text().split(" ");
	var div_name = str[2]+'_'+str[3];
	$('.graph_content').css('display','none');
	$('#'+div_name).css('display','block');
	
	// dealing with menu option selection effects
	$(this).closest('.graph_tabs_top_menu').children('.graph_tabs_top_menu_options_selected').addClass('graph_tabs_top_menu_options');
	$(this).closest('.graph_tabs_top_menu').children('.graph_tabs_top_menu_options_selected').removeClass('graph_tabs_top_menu_options_selected');
	$(this).addClass('graph_tabs_top_menu_options_selected');
	$(this).removeClass('graph_tabs_top_menu_options');
});


/*******************************************************
**			Start Button
********************************************************/
$('.ok_button_outter_start').click(function () {
	var algo_name = $('#selected_algorithm').text().replace(/^\s*|\s*$/g,'');
	var data_name = $('#selected_dataset').text().replace(/^\s*|\s*$/g,'');

    /*
    document.write("here\n");
	// colect parameter from algorithm
	var algorithm_parameters = document.getElementById('parameter').value
    document.write(algorithm_parameters);
    document.write("here\n");
    */
    var paras = [];

	
	var data_para = ""; 
	var algo_para = ""; 
    
	$('.parameters_options_text_box').each(function () {
		var para_type = $(this).parent().attr('id');
		
		if (para_type=='algo_para_container'){
			var para_val = $(this).find('.parameters_options_input_box').val();
			algo_para = algo_para + para_val +", ";
            
		}
		else if(para_type=='data_para_container'){
			var para_val = $(this).find('.parameters_options_input_box').val();
			data_para = data_para + para_val +", ";			
			
		}
	});	
	
	alert(data_para);
	alert(algo_para);
	
	matcheck = data_name.substr(data_name.length - 3);
	
	if (matcheck == 'mat' || matcheck == 'MAT')
	{
	    $.get("/engine/user_uploaded_dataset/", {'algo':algo_name, 'data':data_name, 'data_para':data_para, 'algo_para':algo_para}, function(data)
	    {
			alert('cluster completed!');
			window.location = data;
		    
			/*
			// parse json into an array
			var paras = JSON.parse(data);

			// decide sample size
			var data_sample_size = 0;
			*/
		});
	}
	
	else
	{
		// send a "GET" to server
	    $.get("/engine/get_machine_learning_result_given_algorithm_and_dataset/", {'algo':algo_name, 'data':data_name, 'data_para':data_para, 'algo_para':algo_para}, function(data)
	    {
		
			// parse json into an array
			var paras = JSON.parse(data);
		
			// decide sample size
			var data_sample_size = 0;
		
		
			// Plot Original Data
			//---------------------------------------------------------------------------------
			// get all data and store them into format acceptable for the plotter
			// expected cordinates_sets looks like this: [[1,1],[2,2]]
			var cordinates_sets = [];
		
			for (cor in paras['original_data_points']){
				var parsed_cor = String(paras['original_data_points'][cor]).split(",");
				var single_set_cordinates=new Array(parseFloat(parsed_cor[0]), parseFloat(parsed_cor[1]));
				cordinates_sets.push(single_set_cordinates);			
				data_sample_size++;
			}
		
		
			// expected result_set look like this: [ [[1,1],[2,2]] ]		
			var result_set = []
			result_set.push(cordinates_sets);
		
			// remove default graph
			$('#ori_data').remove();		
			var plot_block = "<div class='data_graph' id='ori_data' style='height:500px; width:800px;'></div>";		
			var plot_frame = $('#plot_container_original');
	        $(plot_block).prependTo(plot_frame);										
		
			// plot it
			var plot1 = $.jqplot('ori_data', result_set, 
		    { 
		      series:[ 
		          {
		            showLine:false, 
		            markerOptions: { style:'x' }
		          }
		      ]
		    });
		  	//---------------------------------------------------------------------------------
		
			// Plot Clustered Data - More Complicated
		
			//---------------------------------------------------------------------------------
			// get all data and store them into format acceptable for the plotter
			// expected cordinates_sets looks like this: [[1,1],[2,2]]
		
			// loop Through Clustered Group - paras['clustered_data_unique_label']
			clustered_data = [];
			for (cor in paras['clustered_data_unique_label']){
				clustered_data[paras['clustered_data_unique_label'][cor]] = [];
			}
		
			// put coordinates into the coressponding array
			for (cor in paras['clustered_data_label']){			
				var group_id = paras['clustered_data_label'][cor];
			
				var parsed_cor = String(paras['original_data_points'][cor]).split(",");
				var single_set_cordinates=new Array(parseFloat(parsed_cor[0]), parseFloat(parsed_cor[1]));
						
				clustered_data[group_id].push(single_set_cordinates);						
			}
		
			// now the color and shape combination supports upto 40 combination
			var color_array = [ "#4bb2c5", "#c5b47f", "#EAA228", "#579575", "#839557", "#958c12", "#953579", "#4b5de4", "#d8b83f", "#ff5800", "#0085cc"];
			var shape_array = [ "x", "diamond", "circle", "filledSquare"];
		
			var shape_count = 0;
			var color_count = 0;
			var characteristic_array = [];
				
			for (cor in clustered_data){
			
				characteristic = {
			      showLine:false,
			 	  color:color_array[color_count],
			      markerOptions: { style:shape_array[shape_count] }
			    };
					
				characteristic_array.push(characteristic);						
						
				if(color_count >= color_array.length-1){
					color_count=0;
					if (shape_array >= shape_array.length-1){
						shape_array=0;
					}
					else{
						shape_array++;
					}
				}
				else{
					color_count++;
				}	
			}
				
			// remove default graph
			// need to show div tag in order to operate on it
			$('#Clustered_Dataset').css('display','block');
		
			$('#clus_data').remove();		
			var cluster_plot_block = "<div class='data_graph' id='clus_data' style='height:500px; width:800px;'>";
			var cluster_plot_frame = $('#plot_container_clustered');
	        $(cluster_plot_block).prependTo(cluster_plot_frame);										
		
			alert(clustered_data.length);

			// plot it
			//cluster_result_set
			var plot1 = $.jqplot('clus_data', clustered_data, 
		    { 
		      series:characteristic_array
		    });
			$('#Clustered_Dataset').css('display','none');
		
			//---------------------------------------------------------------------------------
		
		});	
	}
});





