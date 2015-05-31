$(function() {
	String.prototype.decodeHTML = function() { return $("<div>", {html: "" + this}).html(); };

	var $page = $("#page"), $preloader = $("#preloader"), $counter = 0;

	checkUrl = function(slug) {
		var url = location.href;
		var regex = '^(http[s]?\:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-\_\:]+(\/)?' + slug + '(\#)?(\/)?$';
		if (url.match(new RegExp(regex))) { return true; } else { return false; };
	},

	engineSideMenu = function() {

	},

	engineFormValidations = function() {
	},

	engineGraphs = function(graph, resource, title) {

	},

	enginePage = function() {

		if (checkUrl("simulated_tests/new")) {
			console.log('[INFO] enginePage called at: simulated_tests/new.');

			var engineDatepickers = function() {
				$('#page .input-group.date').datepicker({
					todayBtn: "linked",
					keyboardNavigation: false,
					forceParse: false,
					calendarWeeks: true,
					autoclose: true,
					format: 'dd/mm/yyyy',
				});
			}

			var engineSelects = function() {
				$('#page .chosen-select').chosen({width: 'inherit'});
			}

			var engineIChecks = function() {
				$('#page .i-checks').iCheck({
					checkboxClass: 'icheckbox_square-green',
					radioClass: 'iradio_square-green',
				});
			}

			engineDatepickers();
			engineIChecks();
			engineSelects();

			$('#dates').on('cocoon:after-insert', function() {
				console.log("dasd")
				engineDatepickers();
			});

			$('#questions').on('cocoon:after-insert', function() {
				engineSelects();
				engineIChecks();
			});

			$('.add-question').trigger('click');
		} else {
					console.log('[INFO] enginePage called at generic page.');

					if ($('table#dashboard-simulated-test-graph-resource').length > 0) {
						var resource = $('table#dashboard-simulated-test-graph-resource tr').get().map(function(row) {
							return $(row).find('td').get().map(function(cell) {
								return $(cell).html();
							});
						});

						categories = [];
						for (i = 2; i < resource.length; ++i) {
							categories.push(resource[i][0]);
						}
						data = [];
						for (j = 1; j < resource[0].length; ++j) {
							data[j-1] = {};
							data[j-1]["data"] = [];
							data[j-1]["name"] = resource[0][j];
							data[j-1]["color"] = resource[1][j];

							for (k = 2; k < resource.length; ++k) {
								data[j-1]["data"].push(parseFloat(resource[k][j]));
							}
						}

						$('#dashboard-simulated-test-graph').highcharts({
							chart: {
								type: 'column',
								height: 220,
							},
							title: { text: ' '  },
							legend: {
								layout: 'horizontal',
								align: 'center',
								verticalAlign: 'top',
							},
							credits: false,
							xAxis: {
								categories: categories,
								crosshair: true
							},
							yAxis: {
								min: 0,
								max: 100,
								tickInterval: 20,
								title: {
									text: 'Porcentagem de acertos'
								}
							},
							tooltip: {
								headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
								pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
								'<td style="padding:0"><b>{point.y:.1f} %</b></td></tr>',
								footerFormat: '</table>',
								shared: true,
								useHTML: true
							},
							plotOptions: {
								column: {
									pointPadding: 0.2,
									borderWidth: 0
								}
							},
							series: data
						});
					}

					if ($('#flot-chart1').length > 0) {
						var d1 = [[1262304000000, 6], [1264982400000, 3057], [1267401600000, 20434], [1270080000000, 31982], [1272672000000, 26602], [1275350400000, 27826], [1277942400000, 24302], [1280620800000, 24237], [1283299200000, 21004], [1285891200000, 12144], [1288569600000, 10577], [1291161600000, 10295]];
						var d2 = [[1262304000000, 5], [1264982400000, 200], [1267401600000, 1605], [1270080000000, 6129], [1272672000000, 11643], [1275350400000, 19055], [1277942400000, 30062], [1280620800000, 39197], [1283299200000, 37000], [1285891200000, 27000], [1288569600000, 21000], [1291161600000, 17000]];

						var data1 = [
						{ label: "Data 1", data: d1, color: '#17a084'},
						{ label: "Data 2", data: d2, color: '#127e68' }
						];
						$.plot($("#flot-chart1"), data1, {
							xaxis: {
								tickDecimals: 0
							},
							series: {
								lines: {
									show: true,
									fill: true,
									fillColor: {
										colors: [{
											opacity: 1
										}, {
											opacity: 1
										}]
									},
								},
								points: {
									width: 0.1,
									show: false
								},
							},
							grid: {
								show: false,
								borderWidth: 0
							},
							legend: {
								show: false,
							}
						});
					}
		}
	},

	init = function() {
		engineSideMenu();
		enginePage();
		engineFormValidations();
	},

	ajaxLoad = function(html, status, xhr) {
		$counter++;
		console.log("- -- --- ---- ----- " + $counter + "º ajax call ----- ---- --- -- -");
		console.log("[INFO] Ajax Request Status: " + status);
		console.log("[INFO] Ajax Request XHR: " + xhr);
		if ( status == "error" ) {
			var msg = "Sorry but there was an error: ";
			alert(msg + xhr.status + " " + xhr.statusText);
		} else {
			// $preloader.hide( 500 );
			document.title = html
			.match(/<title>(.*?)<\/title>/)[1]
			.trim()
			.decodeHTML();
			init();
		}
	},

	loadPage = function(href) {
		$page.load(href + ' #page>*', ajaxLoad);
	};

	init();

	$(window).on("popstate", function(e) {
		if (e.originalEvent.state !== null) {
			loadPage(location.href);
		}
	});

	$(document).on("click", "a, [data-href]", function(ev) {
		var href = $(this).attr("href");
		var dataAjax = $(this).attr("data-ajax");

		if (dataAjax == "false" || href == undefined || href == '#') { return; }

		ev.preventDefault();

		if (href.indexOf(document.domain) > -1 || href.indexOf(':') === -1) {
			// $preloader.show( 500 );
			history.pushState({}, '', href);
			loadPage(href);
			return false;
		} else {
			console.log('[INFO] At: click.data-ajax');
		}
	});
});
