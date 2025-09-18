$(document).ready(function () {
	$(".filter-checkbox").on('click', function () {
		var filter_object = {};
		$(".filter-checkbox").each(function (index, ele) {
			var filter_value = $(this).val();
			var filter_key = $(this).data('filter');
			console.log(filter_key, filter_value);
			filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (el) {
				return el.value;
			});
		});
		$.ajax({
			url: '/landProject/filter-data/',
			data: filter_object,
			dataType: 'json',
			success: function (res) {
				$("#filteredProject").html(res.data);
			}
		});
	});
});

$(document).ready(function (){
	$(".filter-checkbox").on('click', function () {
		var filter_object = {};
		$(".filter-checkbox").each(function (index, ele) {
			var filter_value = $(this).val();
			var filter_key = $(this).data('filter');
			console.log(filter_key, filter_value);
			filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (el) {
				return el.value;
			});
		});
		$.ajax({
			url: '/apnartmentProject/apmntp_filter/',
			data: filter_object,
			dataType: 'json',
			success: function (res) {
				$("#apartmentProject").html(res.data);
			}
		});
	});
});

$("#id_division").change(function () {
	var url = $("#areaForm").attr("/ajax/load_districts/");
	var divisionId = $(this).val();

	$.ajax({
		url: '/ajax/load_districts/',
		data: {
			'division': divisionId,
		},
		success: function (data) {
			$("#id_district").html(data);
		}
	});
});

$("#id_district").change(function () {
	var url = $("#areaForm").attr("/ajax/load_subdistricts/");
	var districtId = $(this).val();

	$.ajax({
		url: '/ajax/load_subdistricts/',
		data: {
			'district': districtId,
		},
		success: function (data) {
			$("#id_sub_district").html(data);
		}
	});
});

//end load division and district


// start filtering division, district, sub_district for land property
$(document).ready(function () {
	$("#id_division").change(function () {
		var url = $("#areaForm").attr("/landProject/filter-data/");
		var division = $(this).val();

		$.ajax({
			url: '/landProject/filter-data/',
			dataType: 'json',
			data: {
				'division': division,
			},
			success: function (res) {
				$("#filteredProject").html(res.data);
			}
		});
	});

	$("#id_district").change(function () {
		var url = $("#areaForm").attr("/landProject/filter-data/");
		var district = $(this).val();
		$.ajax({
			url: '/landProject/filter-data/',
			dataType: 'json',
			data: {
				'district': district,
			},
			success: function (res) {
				$("#filteredProject").html(res.data);
			}
		});
	});

	$("#id_sub_district").change(function () {
		var url = $("#areaForm").attr("/landProject/filter-data/");
		var sub_district = $(this).val();
		$.ajax({
			url: '/landProject/filter-data/',
			dataType: 'json',
			data: {
				'sub_district': sub_district,
			},
			success: function (res) {
				$("#filteredProject").html(res.data);
			}
		});
	});
});

// start filtering division, district, sub_district for apartment property
$(document).ready(function () {
	$("#id_division").change(function () {
		var url = $("#areaForm").attr("/apnartmentProject/apmntp_filter/");
		var division = $(this).val();

		$.ajax({
			url: '/apnartmentProject/apmntp_filter/',
			dataType: 'json',
			data: {
				'division': division,
			},
			success: function (res) {
				$("#apartmentProject").html(res.data);
			}
		});
	});

	$("#id_district").change(function () {
		var url = $("#areaForm").attr("/apnartmentProject/apmntp_filter/");
		var district = $(this).val();
		$.ajax({
			url: '/apnartmentProject/apmntp_filter/',
			dataType: 'json',
			data: {
				'district': district,
			},
			success: function (res) {
				$("#apartmentProject").html(res.data);
			}
		});
	});

	$("#id_sub_district").change(function () {
		var url = $("#areaForm").attr("/apnartmentProject/apmntp_filter/");
		var sub_district = $(this).val();
		$.ajax({
			url: '/apnartmentProject/apmntp_filter/',
			dataType: 'json',
			data: {
				'sub_district': sub_district,
			},
			success: function (res) {
				$("#apartmentProject").html(res.data);
			}
		});
	});
});