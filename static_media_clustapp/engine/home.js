$(document).ready(function(){
	
  	var plot1 = $.jqplot ('ori_data', [[[1,1],[2,7]],[1,2,3,4,5]]);
	var plot1 = $.jqplot ('clus_data', [[[2,2],[2,7]],[2,7],[9,9,9,9,9,9,9]]);
  	var plot1 = $.jqplot ('obj_func', [[[3,3],[2,7]],[2,7],[1,3,4,6,8,2,5]]);

	// handle first appearence of the selection tab
	$('#default_tab').addClass('graph_tabs_top_menu_options_selected');	
	$('.graph_content').css('display','none');
	$('#Original_Dataset').css('display','block');
	
	// handle the margin top of the whole all the tabs
	var graph_tabs_height = $('.parameters_container').height()+220;
	$('.graph_tabs').css('margin-top', graph_tabs_height+'px');

});


/*******************************************************
**			Hover Effects
**				Top Menu
**				Algorithm Selectors
**				Graph Display Option
********************************************************/

// Top Menu
$('.top_menu_frame_menu_options').mouseenter(function () {
	$(this).css('color', '#fcae14');
});
$('.top_menu_frame_menu_options').mouseleave(function () {
	$(this).css('color', 'white');
});

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










